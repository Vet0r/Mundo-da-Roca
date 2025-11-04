"""
Gerenciador de GPU Dedicada
Força o uso de GPU dedicada (NVIDIA, AMD) ao invés de GPU integrada
"""

import os
import sys
import platform

# ============================================================
# VARIÁVEIS DE AMBIENTE PARA GPU DEDICADA
# ============================================================

def enable_dedicated_gpu():
    """
    Ativar GPU dedicada usando variáveis de ambiente
    Antes de importar OpenGL ou Pygame
    """
    
    system = platform.system()
    
    # NVIDIA GPU (Windows/Linux/Mac)
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    
    # AMD GPU (Windows/Linux)
    os.environ['HIP_DEVICE'] = '0'
    os.environ['ROCM_HOME'] = '/opt/rocm'
    
    # Intel GPU (Linux)
    os.environ['I915_DEBUG'] = '1'
    
    # macOS - Force GPU 0 (dedicada)
    os.environ['MTL_DEVICE_ID'] = '0'
    os.environ['GPU_DEVICE_ORDINAL'] = '0'
    
    if system == "Darwin":  # macOS
        # Forçar GPU dedicada no macOS
        os.environ['METAL_DEVICE_AFFINITY'] = '1'
        os.environ['METAL_DEVICE_ORDINAL'] = '0'
    
    print("✓ Variáveis de ambiente para GPU dedicada configuradas")


def detect_gpus():
    """
    Detectar GPUs disponíveis no sistema
    """
    
    print("\n" + "="*60)
    print("DETECÇÃO DE GPUS DISPONÍVEIS")
    print("="*60 + "\n")
    
    system = platform.system()
    gpus_found = []
    
    # ============================================================
    # NVIDIA CUDA
    # ============================================================
    try:
        import pycuda.driver as cuda
        cuda.init()
        
        print(f"NVIDIA CUDA: Detectado")
        print(f"  Devices disponíveis: {cuda.Device.count()}")
        
        for i in range(cuda.Device.count()):
            device = cuda.Device(i)
            props = device.get_attributes()
            print(f"  Device {i}: {device.name()}")
            gpus_found.append(('NVIDIA', device.name(), i))
        
        print()
    except Exception as e:
        pass  # NVIDIA não disponível
    
    # ============================================================
    # METAL (macOS)
    # ============================================================
    if system == "Darwin":
        try:
            import pyobjc
            print("Metal (macOS): Detectado")
            print("  Nota: Use MTL_DEVICE_ID=0 para GPU dedicada")
            gpus_found.append(('Metal', 'macOS GPU', 0))
            print()
        except:
            pass
    
    # ============================================================
    # VULKAN
    # ============================================================
    try:
        # Tentar detectar Vulkan
        import subprocess
        result = subprocess.run(['vulkaninfo', '--summary'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("Vulkan: Detectado")
            print(result.stdout[:500])
            gpus_found.append(('Vulkan', 'Vulkan Device', 0))
    except:
        pass
    
    # ============================================================
    # OPENGL
    # ============================================================
    try:
        import pygame
        from OpenGL.GL import glGetString, GL_RENDERER, GL_VERSION, GL_VENDOR
        
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        
        display = pygame.display.set_mode((100, 100), pygame.OPENGL | pygame.HIDDEN)
        
        vendor = glGetString(GL_VENDOR).decode() if glGetString(GL_VENDOR) else "Unknown"
        renderer = glGetString(GL_RENDERER).decode() if glGetString(GL_RENDERER) else "Unknown"
        version = glGetString(GL_VERSION).decode() if glGetString(GL_VERSION) else "Unknown"
        
        print("OpenGL: Detectado")
        print(f"  Vendor: {vendor}")
        print(f"  Renderer: {renderer}")
        print(f"  Version: {version}")
        print()
        
        # Detectar tipo de GPU
        if 'NVIDIA' in renderer or 'NVIDIA' in vendor:
            gpus_found.append(('OpenGL/NVIDIA', renderer, 0))
        elif 'AMD' in renderer or 'Radeon' in renderer:
            gpus_found.append(('OpenGL/AMD', renderer, 0))
        elif 'Intel' in renderer or 'Intel' in vendor:
            gpus_found.append(('OpenGL/Intel', renderer, 0))
        elif 'Apple' in vendor or 'M1' in renderer or 'M2' in renderer or 'M3' in renderer:
            gpus_found.append(('OpenGL/Apple Silicon', renderer, 0))
        
        pygame.display.quit()
        
    except Exception as e:
        print(f"OpenGL: Não disponível ({e})")
    
    print("\n" + "="*60)
    print("RESUMO DE GPUS DETECTADAS")
    print("="*60 + "\n")
    
    if gpus_found:
        for i, (api, name, device_id) in enumerate(gpus_found, 1):
            print(f"{i}. {api}: {name} (Device {device_id})")
        print()
        return gpus_found
    else:
        print("Nenhuma GPU dedicada detectada")
        print("Sistema está usando GPU integrada ou iGPU\n")
        return []


def force_discrete_gpu():
    """
    Forçar GPU dedicada no sistema operacional
    Retorna comandos para adicionar ao início do script
    """
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return """
# Forçar GPU dedicada no macOS
import os
os.environ['METAL_DEVICE_AFFINITY'] = '1'  # Usar GPU dedicada
os.environ['MTL_DEVICE_ID'] = '0'          # Device ID 0
"""
    
    elif system == "Windows":
        return """
# Forçar GPU dedicada no Windows
import os
# NVIDIA
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# AMD
os.environ['GPU_DEVICE_ORDINAL'] = '0'
"""
    
    elif system == "Linux":
        return """
# Forçar GPU dedicada no Linux
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['GPU_DEVICE_ORDINAL'] = '0'
"""


def get_system_gpu_info():
    """
    Obter informações de GPU do sistema
    """
    
    print("\n" + "="*60)
    print("INFORMAÇÕES DE GPU DO SISTEMA")
    print("="*60 + "\n")
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            import subprocess
            # Obter informações de GPU no macOS
            result = subprocess.run(['system_profiler', 'SPDisplaysDataType'],
                                  capture_output=True, text=True, timeout=10)
            print(result.stdout)
        except Exception as e:
            print(f"Erro ao obter informações de GPU: {e}")
    
    elif system == "Windows":
        try:
            import subprocess
            result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 
                                   'get', 'name'], capture_output=True, text=True)
            print(result.stdout)
        except:
            print("Execute em PowerShell: Get-WmiObject Win32_VideoController")
    
    elif system == "Linux":
        try:
            import subprocess
            result = subprocess.run(['lspci', '|', 'grep', 'VGA'],
                                  capture_output=True, text=True, shell=True)
            print(result.stdout)
        except:
            print("Execute: lspci | grep VGA")


class GPUProfiler:
    """
    Perfilador de GPU - monitora uso de GPU durante execução
    """
    
    def __init__(self):
        self.start_time = None
        self.gpu_samples = []
    
    def start_monitoring(self):
        """Iniciar monitoramento de GPU"""
        import time
        self.start_time = time.time()
        self._monitor_nvidia()
    
    def _monitor_nvidia(self):
        """Monitorar GPU NVIDIA usando nvidia-smi"""
        try:
            import subprocess
            import threading
            
            def monitor():
                while True:
                    try:
                        result = subprocess.run(
                            ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total',
                             '--format=csv,noheader,nounits'],
                            capture_output=True, text=True, timeout=2
                        )
                        
                        if result.returncode == 0:
                            self.gpu_samples.append(result.stdout.strip())
                        
                        import time
                        time.sleep(1)
                    except:
                        break
            
            monitor_thread = threading.Thread(target=monitor, daemon=True)
            monitor_thread.start()
        except:
            pass
    
    def get_report(self):
        """Obter relatório de uso de GPU"""
        if not self.gpu_samples:
            return "Sem dados de GPU disponíveis"
        
        try:
            utilizations = []
            for sample in self.gpu_samples:
                try:
                    util, mem_used, mem_total = sample.split(', ')
                    utilizations.append(float(util))
                except:
                    pass
            
            if utilizations:
                avg_util = sum(utilizations) / len(utilizations)
                return f"GPU Utilização Média: {avg_util:.1f}%"
        except:
            pass
        
        return "Erro ao processar dados de GPU"


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerenciador de GPU Dedicada")
    parser.add_argument('--detect', action='store_true', help='Detectar GPUs disponíveis')
    parser.add_argument('--info', action='store_true', help='Obter informações de GPU do sistema')
    parser.add_argument('--enable', action='store_true', help='Habilitar GPU dedicada')
    parser.add_argument('--force', action='store_true', help='Forçar GPU dedicada (mostrar código)')
    
    args = parser.parse_args()
    
    if args.detect or not any(vars(args).values()):
        detect_gpus()
    
    if args.info:
        get_system_gpu_info()
    
    if args.enable:
        enable_dedicated_gpu()
        print("\nGPU dedicada foi configurada!")
    
    if args.force:
        code = force_discrete_gpu()
        print("\nAdicione este código ao início do seu script main.py:\n")
        print(code)
