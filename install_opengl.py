#!/usr/bin/env python3
"""
Script de instalação de dependências para suporte a OpenGL
Execute: python3 install_opengl.py
"""

import subprocess
import sys
import platform

def install_packages():
    """Instalar dependências OpenGL"""
    
    print("=" * 60)
    print("Instalador de Dependências OpenGL para Mundo-da-Roca")
    print("=" * 60)
    print()
    
    packages = [
        "PyOpenGL",
        "PyOpenGL-accelerate",
        "numpy",
        "PyGLM",
    ]
    
    print("Pacotes a instalar:")
    for pkg in packages:
        print(f"  • {pkg}")
    print()
    
    system = platform.system()
    print(f"Sistema detectado: {system}")
    print()
    
    for package in packages:
        print(f"Instalando {package}...", end=" ")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print("✓")
        except subprocess.CalledProcessError:
            print("✗")
            print(f"  Erro ao instalar {package}")
    
    print()
    print("=" * 60)
    print("Verificando instalação...")
    print("=" * 60)
    print()
    
    # Verificar OpenGL
    try:
        from OpenGL.GL import GL_VERSION
        print("✓ PyOpenGL instalado com sucesso")
    except ImportError:
        print("✗ Erro ao verificar PyOpenGL")
    
    # Verificar numpy
    try:
        import numpy
        print(f"✓ NumPy {numpy.__version__} instalado")
    except ImportError:
        print("✗ Erro ao verificar NumPy")
    
    # Verificar glm
    try:
        import glm
        print(f"✓ PyGLM instalado")
    except ImportError:
        print("✗ Erro ao verificar PyGLM")
    
    print()
    print("=" * 60)
    print("Instalação concluída!")
    print("Execute 'python3 main.py' para iniciar o jogo com GPU")
    print("=" * 60)


if __name__ == "__main__":
    try:
        install_packages()
    except KeyboardInterrupt:
        print("\nInstalação cancelada pelo usuário")
        sys.exit(1)
