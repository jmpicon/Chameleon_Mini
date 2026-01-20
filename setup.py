from setuptools import setup, find_packages

setup(
    name="chameleon-lib",
    version="1.0.0",
    author="José Picón",
    author_email="jose.picon@example.com",
    description="Librería avanzada para auditoría RFID con Chameleon Mini",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jmpicon/ChameleonLib",
    packages=find_packages(),
    install_requires=[
        "pyserial>=3.5",
        "colorama>=0.4.4",
        "xmodem>=0.4.7",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'chameleon-cli=src.cli:main',
        ],
    },
)
