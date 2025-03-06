from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lee las dependencias de requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name="clipLLM",  # Nombre del paquete (debe ser único en PyPI)
    version="0.1.0",  # Versión semántica (ej: 0.1.0, 1.0.0, 1.2.3)
    author="Tu Nombre",  # Tu nombre
    author_email="tu.correo@example.com",  # Tu correo
    description="Descripción corta de clipLLM", # Descripción corta
    long_description=long_description,  # Descripción larga (desde README.md)
    long_description_content_type="text/markdown", # Tipo de la descripción larga
    url="https://github.com/tu_usuario/clipLLM",  # URL del repositorio (si tienes)
    packages=find_packages(),  # Encuentra automáticamente los paquetes en el directorio src
    package_dir={"": "src"},  # Indica que el código fuente está en el directorio src
    install_requires=required,  # Dependencias del proyecto
    classifiers=[  # Información sobre la licencia, Python versions, etc.
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Reemplaza con la licencia correcta
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "clip-llm=clipllm.clipllm:main",  # Corrección: especifica el módulo dentro del paquete clipllm
        ],
    },
    python_requires=">=3.7",  # Versión mínima de Python soportada
)