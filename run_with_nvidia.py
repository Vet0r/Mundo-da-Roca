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

# Configurações NVIDIA
print("Configurando GPU NVIDIA...")

os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ['CUDA_FORCE_PTX_JIT'] = '1'
os.environ['CUDNN_ENABLED'] = '1'

# Configurações específicas por SO
system = platform.system()

if system == "Linux":
    print("Sistema: Linux")
    os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/lib64:/opt/cuda/lib64:' + \
                                    os.environ.get('LD_LIBRARY_PATH', '')
    os.environ['PATH'] = '/usr/local/cuda/bin:' + os.environ.get('PATH', '')

elif system == "Windows":
    print("Sistema: Windows")
    # Windows já tem drivers integrados
    pass

elif system == "Darwin":
    print("Sistema: macOS")
    # macOS não suporta NVIDIA (use Metal)
    print("⚠️  Nota: macOS não suporta NVIDIA. Usando Metal.")

print("\nVariáveis de Ambiente CUDA:")
print(f"  CUDA_DEVICE_ORDER: {os.environ.get('CUDA_DEVICE_ORDER')}")
print(f"  CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
print(f"  CUDA_LAUNCH_BLOCKING: {os.environ.get('CUDA_LAUNCH_BLOCKING')}")
print(f"  CUDA_FORCE_PTX_JIT: {os.environ.get('CUDA_FORCE_PTX_JIT')}")
print()

# Verificar nvidia-smi
print("Verificando drivers NVIDIA...")
try:
    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("✓ NVIDIA drivers detectados")
        # Mostrar primeira linha do output
        first_line = result.stdout.split('\n')[0]
        print(f"  {first_line}")
    else:
        print("⚠️  nvidia-smi retornou erro")
except FileNotFoundError:
    print("⚠️  nvidia-smi não encontrado - drivers podem não estar instalados")
except subprocess.TimeoutExpired:
    print("⚠️  nvidia-smi timeout")

print("\n" + "="*70)
print("Iniciando Mundo-da-Roca...")
print("="*70 + "\n")

# Importar e executar main
try:
    # Importar os módulos necessários
    import pygame
    from menu import mostrar_menu
    from save_system import SaveSystem
    from config import LARGURA, ALTURA, FPS, carregar_sprites
    from player import Player
    from farm_system import FarmSystem
    from water_system import WaterSystem
    from worker_system import WorkerSystem
    from shop import Shop
    from ui import UI
    from game_controller import GameController
    from camera import Camera
    from hybrid_renderer import check_opengl_support, RENDERER_TYPE, GPU_TYPE, GPU_NAME
    
    # Mostrar informações de GPU
    print(f"Renderizador: {RENDERER_TYPE}")
    print(f"GPU Vendor: {GPU_TYPE}")
    print(f"GPU Name: {GPU_NAME}")
    
    if 'NVIDIA' in GPU_NAME:
        print("✅ GPU NVIDIA DETECTADA!")
        if '3050' in GPU_NAME:
            print("✅ RTX 3050 DETECTADA!")
    else:
        print("⚠️  GPU NVIDIA não foi detectada via OpenGL")
        print("   Pode estar usando GPU integrada")
    
    print("\n" + "="*70 + "\n")
    
    # Importar e executar main
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
