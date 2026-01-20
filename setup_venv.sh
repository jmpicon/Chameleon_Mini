#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[*] Iniciando configuración del entorno virtual local...${NC}"

# 1. Crear el entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[*] Creando directorio 'venv'...${NC}"
    python3 -m venv venv
else
    echo -e "${GREEN}[OK] El entorno virtual 'venv' ya existe.${NC}"
fi

# 2. Activar el entorno
source venv/bin/activate

# 3. Actualizar pip
echo -e "${BLUE}[*] Actualizando pip...${NC}"
pip install --upgrade pip

# 4. Instalar dependencias
echo -e "${BLUE}[*] Instalando librerías desde requirements.txt...${NC}"
pip install -r requirements.txt

# 5. Instalar el paquete en modo editable
echo -e "${BLUE}[*] Configurando ChameleonLib en modo desarrollo...${NC}"
pip install -e .

echo -e "\n${GREEN}[SUCCESS] ¡Entorno Configurado!${NC}"
echo -e "Para activar el entorno en tu terminal, ejecuta:"
echo -e "${BLUE}    source venv/bin/activate${NC}"
echo -e "Para iniciar el Dashboard:"
echo -e "${BLUE}    streamlit run src/web_dashboard.py${NC}"
