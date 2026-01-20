import streamlit as st
import time
import pandas as pd
from datetime import datetime
import sys
import os

# Asegurar que podemos importar los módulos core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.connection import seleccionar_puerto
from src.interface import ChameleonInterface
from src.translator import ISO14443ATranslator
from virtualization.mock_hardware import ChameleonMock

# Configuración de la página
st.set_page_config(
    page_title="Chameleon Ultra Dashboard",
    page_icon="🦎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para un look Hacker/Cybersec
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ff00;
    }
    .stButton>button {
        background-color: #262730;
        color: #00ff41;
        border: 1px solid #00ff41;
    }
    .stButton>button:hover {
        background-color: #00ff41;
        color: #000000;
    }
    .stat-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #00ff41;
    }
</style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO (SESSION STATE) ---
if 'device_connected' not in st.session_state:
    st.session_state.device_connected = False
if 'port' not in st.session_state:
    st.session_state.port = None
if 'use_mock' not in st.session_state:
    st.session_state.use_mock = False
if 'sniffing_data' not in st.session_state:
    st.session_state.sniffing_data = []

# --- FUNCIONES HELPER ---
def get_device():
    """Retorna una instancia fresca de la interfaz basada en el estado actual."""
    if st.session_state.use_mock:
        return ChameleonInterface(mock_device=ChameleonMock())
    elif st.session_state.port:
        return ChameleonInterface(port=st.session_state.port)
    return None

# --- SIDEBAR: CONEXIÓN ---
with st.sidebar:
    st.title("🔌 Conectividad")
    
    st.write("Selecciona el modo de operación:")
    mode = st.radio("Modo", ["Hardware Real", "Simulador (Mock)"])
    
    if mode == "Simulador (Mock)":
        st.session_state.use_mock = True
        st.success("Modo Simulación Activo")
    else:
        st.session_state.use_mock = False
        if st.button("Escanear Puerto"):
            p = seleccionar_puerto()
            if p:
                st.session_state.port = p
                st.success(f"Detectado: {p}")
            else:
                st.error("No se encontró dispositivo")
    
    status_color = "green" if st.session_state.port or st.session_state.use_mock else "red"
    st.markdown(f"Estado: <span style='color:{status_color}'>{'LISTO' if status_color=='green' else 'DESCONECTADO'}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Autor: José Picón")
    st.caption("Suite de Auditoría RFID v1.0")

# --- PANEL PRINCIPAL ---
st.title("🦎 Chameleon Mini: Cybersec Dashboard")

# Tabs para separar funcionalidades
tab1, tab2, tab3 = st.tabs(["🚀 Control & Config", "📡 Live Sniffer", "📊 Análisis"])

with tab1:
    col1, col2 = st.columns(2)
    device = None
    
    try:
        # Intentamos conectar brevemente para leer estado
        if st.session_state.port or st.session_state.use_mock:
            device = get_device()
            
            with col1:
                st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                st.subheader("Información del Dispositivo")
                ver = device.version_get()
                st.code(f"Firmware: {ver}")
                
                config_act = device.config_get()
                st.metric("Modo Actual", config_act)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                st.subheader("Gestión de Identidad (UID)")
                current_uid = device.get_uid()
                st.metric("UID Actual", current_uid)
                
                new_uid = st.text_input("Nuevo UID (Hex)", value="DE AD BE EF")
                if st.button("Escribir UID"):
                    if device.enviar_comando(f"UID={new_uid}")['success']:
                        st.success("¡UID Cambiado con éxito!")
                        device.enviar_comando("STORE")
                    else:
                        st.error("Fallo al escribir UID")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("Gestión de Slots")
            
            # Selector de Slot
            cols = st.columns(8)
            for i in range(1, 9):
                if cols[i-1].button(f"Slot {i}"):
                    device.enviar_comando(f"SETTING={i}")
                    st.toast(f"Cambiado a Slot {i}")
                    time.sleep(0.5)
                    st.experimental_rerun()
            
            device.close()
        else:
            st.info("👈 Por favor configure la conexión en la barra lateral.")

    except Exception as e:
        st.error(f"Error de conexión: {e}")

with tab2:
    st.header("Interceptación de Tráfico ISO14443A")
    st.markdown("Este módulo captura trazas en **Tiempo Real** y aplica el motor de traducción.")

    if 'is_sniffing' not in st.session_state:
        st.session_state.is_sniffing = False

    col_ctrl, col_status = st.columns([1, 4])
    
    with col_ctrl:
        if st.button("🔴 INICIAR SNIFFER" if not st.session_state.is_sniffing else "⏹ DETENER"):
            st.session_state.is_sniffing = not st.session_state.is_sniffing
    
    with col_status:
        if st.session_state.is_sniffing:
            st.warning("⚠️ CAPTURANDO TRÁFICO... (No desconecte el dispositivo)")
        else:
            st.success("Esperando orden.")

    # Área de Logs
    log_container = st.empty()
    
    if st.session_state.is_sniffing and (st.session_state.port or st.session_state.use_mock):
        try:
            dev_sniff = get_device()
            # Configurar para Sniffing
            dev_sniff.enviar_comando("LOGMODE=LIVE")
            
            # Bucle de captura (Streamlit re-run loop trick)
            # Nota: En una app real compleja, esto iría en un hilo aparte, 
            # pero para este demo bloqueamos el renderizado para máxima velocidad de lectura.
            while st.session_state.is_sniffing:
                if dev_sniff.serial.in_waiting > 0:
                    try:
                        line = dev_sniff.serial.readline().decode('ascii', errors='ignore').strip()
                        if line:
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            decoded = ISO14443ATranslator.translate_line(line)
                            
                            entry = {
                                "Time": timestamp,
                                "Raw": line,
                                "Decoded": decoded if decoded else "..."
                            }
                            st.session_state.sniffing_data.append(entry)
                            
                            # Mostrar las últimas 10 líneas
                            df = pd.DataFrame(st.session_state.sniffing_data[-15:])
                            log_container.dataframe(df, use_container_width=True)
                            
                    except Exception: pass
                # Pequeño sleep para no freír la CPU, pero muy corto para RF
                time.sleep(0.001) 
                
        except Exception as e:
            st.error(f"Error en sniffer: {e}")
        finally:
            if 'dev_sniff' in locals():
                dev_sniff.enviar_comando("LOGMODE=OFF")
                dev_sniff.close()
    
    # Mostrar datos estáticos si paramos el sniffer
    if not st.session_state.is_sniffing and st.session_state.sniffing_data:
        st.markdown("### 📥 Historial de Captura")
        df_full = pd.DataFrame(st.session_state.sniffing_data)
        st.dataframe(df_full, use_container_width=True)
        
        csv = df_full.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Descargar CSV",
            csv,
            "chameleon_capture.csv",
            "text/csv",
            key='download-csv'
        )

with tab3:
    st.header("Análisis Estadístico")
    if st.session_state.sniffing_data:
        df = pd.DataFrame(st.session_state.sniffing_data)
        
        # Conteo de comandos
        col_metrics1, col_metrics2 = st.columns(2)
        
        with col_metrics1:
            st.caption("Distribución de Paquetes (Lector vs Tarjeta)")
            # Heurística simple: Raw empieza con '<' o '>'
            df['Source'] = df['Raw'].apply(lambda x: 'Lector' if '<' in x else ('Tarjeta' if '>' in x else 'Sistema'))
            source_counts = df['Source'].value_counts()
            st.bar_chart(source_counts)
            
        with col_metrics2:
            st.caption("Tipos de Comandos Más Frecuentes")
            # Extraer el tipo de comando de la columna decoded
            # "[LECTOR] REQA    | ..." -> "REQA"
            def extract_cmd_type(decoded_str):
                parts = decoded_str.split('|')
                if len(parts) > 1:
                    return parts[1].strip()
                return "Unknown"
            
            df['CommandType'] = df['Decoded'].apply(extract_cmd_type)
            cmd_counts = df['CommandType'].value_counts().head(5)
            st.write(cmd_counts)
    else:
        st.info("Aún no hay datos para analizar. Ejecute el sniffer primero.")
