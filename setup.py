from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name="clipllm",  # Changed from clip-llm to clipllm (no hyphen)
    version="0.1.0",  # Adding explicit version
    author="GlitchcrafterOfficial",
    author_email="jcrispis57@example.com",
    description="Es una herramienta que te permite utilizar un llm con el clipboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/clipLLM",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "clip-llm=clipllm.clipllm:main",  # Command name can still have hyphen
        ],
    },
    python_requires=">=3.7",
)