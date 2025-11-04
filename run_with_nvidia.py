#!/usr/bin/env python3
"""
Script para forçar GPU NVIDIA RTX 3050 e iniciar o jogo
Execute: python3 run_with_nvidia.py
"""

import os
import sys
import subprocess
import platform

# ============================================================
# CONFIGURAR GPU NVIDIA AGRESSIVAMENTE
# ============================================================

print("╔" + "="*68 + "╗")
print("║" + " "*68 + "║")
print("║" + "Iniciando jogo com GPU NVIDIA RTX 3050".center(68) + "║")
print("║" + " "*68 + "║")
print("╚" + "="*68 + "╝\n")

system = platform.system()
print(f"Sistema operacional detectado: {system}")

# Configurações NVIDIA (apenas para Linux e Windows)
if system in ["Linux", "Windows"]:
    print("Configurando GPU NVIDIA...")
    
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    os.environ['CUDA_FORCE_PTX_JIT'] = '1'
    os.environ['CUDNN_ENABLED'] = '1'

    if system == "Linux":
        print("Sistema: Linux")
        os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/lib64:/opt/cuda/lib64:' + \
                                        os.environ.get('LD_LIBRARY_PATH', '')
        os.environ['PATH'] = '/usr/local/cuda/bin:' + os.environ.get('PATH', '')

    elif system == "Windows":
        print("Sistema: Windows")
        # Windows - configuração padrão já é suficiente
        # Os drivers NVIDIA são instalados globalmente

    print("\nVariáveis de Ambiente CUDA:")
    print(f"  CUDA_DEVICE_ORDER: {os.environ.get('CUDA_DEVICE_ORDER')}")
    print(f"  CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    print()

    # Verificar nvidia-smi
    print("Verificando drivers NVIDIA...")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ NVIDIA drivers detectados")
            first_line = result.stdout.split('\n')[0]
            print(f"  {first_line}")
        else:
            print("⚠️  nvidia-smi retornou erro")
    except FileNotFoundError:
        print("⚠️  nvidia-smi não encontrado - drivers podem não estar instalados")
    except subprocess.TimeoutExpired:
        print("⚠️  nvidia-smi timeout")

elif system == "Darwin":
    print("Sistema: macOS - Metal será usado (não suporta NVIDIA)")

print("\n" + "="*70)
print("Iniciando Mundo-da-Roca...")
print("="*70 + "\n")

# Importar e executar main
try:
    import pygame
    from hybrid_renderer import check_opengl_support, RENDERER_TYPE, GPU_TYPE, GPU_NAME
    
    print(f"Renderizador: {RENDERER_TYPE}")
    print(f"GPU Vendor: {GPU_TYPE}")
    print(f"GPU Name: {GPU_NAME}")
    
    if system == "Windows" and 'NVIDIA' in GPU_NAME:
        print("✅ GPU NVIDIA DETECTADA!")
        if '3050' in GPU_NAME:
            print("✅ RTX 3050 DETECTADA!")
    elif system == "Darwin":
        print("✅ GPU Metal ativa no macOS")
    else:
        print("⚠️  GPU NVIDIA não foi detectada via OpenGL")
    
    print("\n" + "="*70 + "\n")
    
    from main import main
    main()

except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro ao executar jogo: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)