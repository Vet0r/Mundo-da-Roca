#!/usr/bin/env python3
"""
Ferramenta de diagnóstico avançado para GPU NVIDIA
Detecta e força uso de GPU NVIDIA 3050 (ou qualquer NVIDIA)
"""

import subprocess
import os
import sys
import platform

def run_command(cmd):
    """Executar comando e retornar output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Erro: {e}"

def check_nvidia_smi():
    """Verificar nvidia-smi (ferramenta NVIDIA)"""
    print("\n" + "="*70)
    print("NVIDIA-SMI (Ferramenta NVIDIA Oficial)")
    print("="*70)
    
    output = run_command("nvidia-smi")
    
    if "not found" in output.lower() or "não encontrado" in output.lower():
        print("❌ nvidia-smi não encontrado - drivers NVIDIA podem não estar instalados")
        print("\nInstale drivers NVIDIA:")
        print("  Windows: https://www.nvidia.com/Download/driverDetails.aspx")
        print("  Linux: sudo apt install nvidia-driver-XXX")
        print("  macOS: Não suportado (use Metal)")
        return False
    
    print(output)
    return True

def check_cuda():
    """Verificar CUDA"""
    print("\n" + "="*70)
    print("NVIDIA CUDA")
    print("="*70)
    
    # Verificar nvcc (CUDA compiler)
    nvcc_output = run_command("nvcc --version")
    
    if "nvcc" in nvcc_output.lower() or "release" in nvcc_output.lower():
        print("✓ CUDA Detectado:")
        print(nvcc_output)
    else:
        print("⚠ CUDA não detectado (opcional)")
    
    # Verificar variáveis de ambiente
    print("\nVariáveis de ambiente CUDA:")
    print(f"  CUDA_HOME: {os.environ.get('CUDA_HOME', 'Não definida')}")
    print(f"  CUDA_PATH: {os.environ.get('CUDA_PATH', 'Não definida')}")
    print(f"  LD_LIBRARY_PATH: {os.environ.get('LD_LIBRARY_PATH', 'Não definida')[:50]}...")

def check_opengl_detailed():
    """Verificar OpenGL em detalhe"""
    print("\n" + "="*70)
    print("OpenGL - Detecção Detalhada")
    print("="*70)
    
    try:
        # Importar Pygame e OpenGL
        import pygame
        from OpenGL.GL import glGetString, GL_VENDOR, GL_RENDERER, GL_VERSION, GL_EXTENSIONS
        
        pygame.init()
        
        # Configurar para preferir GPU NVIDIA
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        
        # Tentar criar contexto OpenGL
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 6)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        
        display = pygame.display.set_mode((100, 100), pygame.OPENGL | pygame.HIDDEN)
        
        vendor = glGetString(GL_VENDOR).decode() if glGetString(GL_VENDOR) else "Unknown"
        renderer = glGetString(GL_RENDERER).decode() if glGetString(GL_RENDERER) else "Unknown"
        version = glGetString(GL_VERSION).decode() if glGetString(GL_VERSION) else "Unknown"
        
        print(f"✓ OpenGL Detectado:")
        print(f"  Vendor: {vendor}")
        print(f"  Renderer: {renderer}")
        print(f"  Version: {version}")
        
        # Verificar se é NVIDIA
        if "NVIDIA" in vendor or "NVIDIA" in renderer:
            print(f"\n✅ GPU NVIDIA DETECTADA!")
            if "3050" in renderer:
                print(f"✅ NVIDIA GeForce RTX 3050 DETECTADA!")
        else:
            print(f"\n⚠️ GPU não é NVIDIA (pode ser integrada)")
        
        # Listar extensões OpenGL importantes
        try:
            extensions_str = glGetString(GL_EXTENSIONS).decode()
            extensions = extensions_str.split()
            
            print(f"\nExtensões OpenGL importantes:")
            important_exts = [
                'GL_ARB_shading_language_include',
                'GL_ARB_bindless_texture',
                'GL_ARB_shader_storage_buffer_object',
                'GL_ARB_compute_shader'
            ]
            
            for ext in important_exts:
                if ext in extensions:
                    print(f"  ✓ {ext}")
        except:
            pass
        
        pygame.display.quit()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao detectar OpenGL: {e}")
        return False

def force_nvidia_gpu():
    """Mostrar como forçar GPU NVIDIA"""
    print("\n" + "="*70)
    print("FORÇAR GPU NVIDIA 3050")
    print("="*70)
    
    print("\nAdicione estas linhas NO INÍCIO de main.py (antes de qualquer import):\n")
    
    code = '''import os

# ============================================================
# FORÇAR GPU NVIDIA DEDICADA
# ============================================================

# Usar NVIDIA GPU 0 (sua 3050)
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# Forçar compilação de CUDA
os.environ['CUDA_FORCE_PTX_JIT'] = '1'

# Variáveis de inicialização
os.environ['CUDNN_ENABLED'] = '1'

# Para NVIDIA em Linux
os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/lib64:' + os.environ.get('LD_LIBRARY_PATH', '')

print("✓ GPU NVIDIA forçada (Device 0)")

# ============================================================
# Resto do código...
# ============================================================
'''
    
    print(code)

def check_pycuda():
    """Verificar se PyCUDA está instalado"""
    print("\n" + "="*70)
    print("PyCUDA (Para acesso direto a CUDA)")
    print("="*70)
    
    try:
        import pycuda.driver as cuda
        cuda.init()
        
        print(f"✓ PyCUDA Instalado")
        print(f"  GPUs detectadas: {cuda.Device.count()}")
        
        for i in range(cuda.Device.count()):
            device = cuda.Device(i)
            print(f"\n  Device {i}:")
            print(f"    Nome: {device.name()}")
            
            try:
                props = device.get_attributes()
                print(f"    Compute Capability: {device.compute_capability()}")
                print(f"    Memory Total: {device.total_memory() / 1024**3:.2f} GB")
            except:
                pass
    
    except ImportError:
        print("⚠️ PyCUDA não instalado")
        print("   Instale com: pip install pycuda")
    except Exception as e:
        print(f"❌ Erro: {e}")

def check_environment_variables():
    """Verificar variáveis de ambiente NVIDIA"""
    print("\n" + "="*70)
    print("Variáveis de Ambiente NVIDIA")
    print("="*70)
    
    nvidia_vars = [
        'CUDA_HOME',
        'CUDA_PATH',
        'CUDA_VISIBLE_DEVICES',
        'CUDA_DEVICE_ORDER',
        'CUDA_LAUNCH_BLOCKING',
        'CUDA_FORCE_PTX_JIT',
        'LD_LIBRARY_PATH',
        'PATH',
    ]
    
    for var in nvidia_vars:
        value = os.environ.get(var, 'Não definida')
        if var == 'LD_LIBRARY_PATH' and len(value) > 50:
            value = value[:50] + "..."
        print(f"  {var}: {value}")

def install_pycuda():
    """Instruções para instalar PyCUDA"""
    print("\n" + "="*70)
    print("Instalar PyCUDA (Recomendado)")
    print("="*70)
    
    print("""
PyCUDA permite acesso direto à GPU NVIDIA CUDA.

Instalar:
  pip install pycuda

Depois, você pode usar:
  import pycuda.driver as cuda
  cuda.init()
  print(f"GPUs: {cuda.Device.count()}")
""")

def main():
    """Executar diagnóstico completo"""
    
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "DIAGNÓSTICO AVANÇADO - GPU NVIDIA".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    # Informações do sistema
    print("INFORMAÇÕES DO SISTEMA")
    print("="*70)
    print(f"Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    # Verificações
    check_nvidia_smi()
    check_cuda()
    check_pycuda()
    check_environment_variables()
    check_opengl_detailed()
    
    # Instruções de solução
    force_nvidia_gpu()
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO E PRÓXIMAS AÇÕES")
    print("="*70)
    
    print("""
1. Se nvidia-smi funciona:
   ✓ Drivers NVIDIA estão instalados
   ✓ GPU 3050 deve aparecer no output

2. Se OpenGL detectou GPU NVIDIA:
   ✓ OpenGL está usando GPU dedicada
   ✓ Jogo deve rodar com performance alta

3. Se ainda não funciona:
   a) Atualizar drivers NVIDIA
   b) Adicionar variáveis de ambiente em main.py
   c) Instalar PyCUDA para acesso direto

4. Teste final:
   $ python3 main.py
   $ Pressione G durante o jogo
   $ Deve mostrar "NVIDIA GeForce RTX 3050"
""")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
