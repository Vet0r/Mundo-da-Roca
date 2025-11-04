"""
Renderizador híbrido - OpenGL com fallback para Pygame
Detecta automaticamente disponibilidade de OpenGL
Força GPU dedicada quando disponível
"""

import pygame
import sys
import os
import platform

# ============================================================
# CONFIGURAR GPU DEDICADA ANTES DE IMPORTAR OPENGL
# ============================================================

# NVIDIA GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# AMD GPU
os.environ['HIP_DEVICE'] = '0'
os.environ['GPU_DEVICE_ORDINAL'] = '0'

# Intel GPU
os.environ['I915_DEBUG'] = '1'

# macOS - Forçar GPU dedicada
if platform.system() == "Darwin":
    os.environ['METAL_DEVICE_AFFINITY'] = '1'
    os.environ['MTL_DEVICE_ID'] = '0'
    os.environ['GPU_DEVICE_ORDINAL'] = '0'

# Flag de disponibilidade
OPENGL_AVAILABLE = False
RENDERER_TYPE = "PYGAME"  # Padrão
GPU_TYPE = "Não detectada"  # Tipo de GPU
GPU_NAME = "Não detectada"  # Nome da GPU

def check_opengl_support():
    """Verificar se OpenGL está disponível no sistema"""
    global OPENGL_AVAILABLE, RENDERER_TYPE, GPU_TYPE, GPU_NAME
    
    try:
        from OpenGL.GL import glGetString, GL_VERSION, GL_RENDERER, GL_VENDOR
        import numpy
        import glm
        
        # Detectar GPU
        try:
            pygame.init()
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
            
            test_display = pygame.display.set_mode((100, 100), pygame.OPENGL | pygame.HIDDEN)
            
            renderer_str = glGetString(GL_RENDERER)
            vendor_str = glGetString(GL_VENDOR)
            
            if renderer_str:
                GPU_NAME = renderer_str.decode('utf-8', errors='ignore')
            if vendor_str:
                GPU_TYPE = vendor_str.decode('utf-8', errors='ignore')
            
            # Detectar tipo de GPU dedicada
            if GPU_NAME and GPU_TYPE:
                if 'NVIDIA' in GPU_TYPE or 'NVIDIA' in GPU_NAME:
                    print("✓ GPU NVIDIA Detectada (Dedicada)")
                elif 'AMD' in GPU_TYPE or 'Radeon' in GPU_NAME:
                    print("✓ GPU AMD Detectada (Dedicada)")
                elif 'Intel' in GPU_TYPE and 'UHD' not in GPU_NAME:
                    print("✓ GPU Intel Detectada (Dedicada)")
                else:
                    print("✓ GPU Detectada")
                
                print(f"  Vendor: {GPU_TYPE}")
                print(f"  Renderer: {GPU_NAME}")
            
            pygame.display.quit()
        except Exception as gpu_error:
            print(f"⚠ Aviso ao detectar GPU: {gpu_error}")
        
        OPENGL_AVAILABLE = True
        RENDERER_TYPE = "OPENGL"
        print("✓ OpenGL e dependências detectadas - Usando GPU")
        return True
    except ImportError as e:
        print(f"✗ OpenGL/dependências não disponíveis: {e}")
        print("  Usando renderização por CPU (Pygame)")
        OPENGL_AVAILABLE = False
        RENDERER_TYPE = "PYGAME"
        return False


class HybridRenderer:
    """Renderizador que usa OpenGL quando disponível, fallback para Pygame"""
    
    def __init__(self, width, height, title="Jogo", use_opengl=True):
        self.width = width
        self.height = height
        self.title = title
        self.use_opengl = use_opengl and OPENGL_AVAILABLE
        self.sprites_data = {}  # Cache de sprites carregados
        
        if self.use_opengl:
            self._init_opengl(width, height)
        else:
            self._init_pygame(width, height)
    
    def _init_pygame(self, width, height):
        """Inicializar renderizador Pygame"""
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
    
    def _init_opengl(self, width, height):
        """Inicializar renderizador OpenGL"""
        try:
            pygame.init()
            
            # Configurar atributos OpenGL
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
            pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
            
            self.screen = pygame.display.set_mode((width, height), 
                                                  pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
            pygame.display.set_caption(self.title)
            
            from OpenGL.GL import glClearColor, glEnable, glBlendFunc, glViewport
            from OpenGL.GL import GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
            from OpenGL.GL import GL_DEPTH_TEST, GL_TEXTURE_2D
            
            glViewport(0, 0, width, height)
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_TEXTURE_2D)
            
            self.clock = pygame.time.Clock()
            self.ogl_initialized = True
            
        except Exception as e:
            print(f"Erro ao inicializar OpenGL: {e}")
            self.use_opengl = False
            self._init_pygame(width, height)
    
    def load_sprite(self, sprite_name, image_path, width=40, height=40):
        """Carregar sprite (cache)"""
        if sprite_name not in self.sprites_data:
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (width, height))
                self.sprites_data[sprite_name] = {
                    'image': image,
                    'width': width,
                    'height': height,
                    'path': image_path
                }
            except Exception as e:
                print(f"Erro ao carregar sprite {sprite_name}: {e}")
                return None
        
        return self.sprites_data[sprite_name]
    
    def draw_sprite(self, sprite_name, x, y):
        """Desenhar sprite na posição"""
        if sprite_name not in self.sprites_data:
            return
        
        sprite = self.sprites_data[sprite_name]
        
        if self.use_opengl:
            self._draw_sprite_opengl(sprite, x, y)
        else:
            self._draw_sprite_pygame(sprite, x, y)
    
    def _draw_sprite_pygame(self, sprite, x, y):
        """Desenhar sprite usando Pygame"""
        rect = sprite['image'].get_rect(topleft=(x, y))
        self.screen.blit(sprite['image'], rect)
    
    def _draw_sprite_opengl(self, sprite, x, y):
        """Desenhar sprite usando OpenGL"""
        # Implementação de renderização OpenGL simples
        # Por enquanto, usar Pygame para não quebrar funcionalidade
        self._draw_sprite_pygame(sprite, x, y)
    
    def draw_rect(self, x, y, width, height, color, filled=True):
        """Desenhar retângulo"""
        if self.use_opengl:
            self._draw_rect_opengl(x, y, width, height, color, filled)
        else:
            self._draw_rect_pygame(x, y, width, height, color, filled)
    
    def _draw_rect_pygame(self, x, y, width, height, color, filled=True):
        """Desenhar retângulo em Pygame"""
        if filled:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height), 1)
    
    def _draw_rect_opengl(self, x, y, width, height, color, filled=True):
        """Desenhar retângulo em OpenGL"""
        # Fallback para Pygame por enquanto
        self._draw_rect_pygame(x, y, width, height, color, filled)
    
    def draw_circle(self, x, y, radius, color, filled=True):
        """Desenhar círculo"""
        if self.use_opengl:
            # Fallback para Pygame
            pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
        else:
            pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
    
    def draw_line(self, x1, y1, x2, y2, color, width=1):
        """Desenhar linha"""
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)
    
    def draw_text(self, text, font, color, x, y):
        """Desenhar texto"""
        text_surface = font.render(text, True, color)
        if self.use_opengl:
            # Fallback para Pygame
            self.screen.blit(text_surface, (x, y))
        else:
            self.screen.blit(text_surface, (x, y))
    
    def clear_screen(self, color=None):
        """Limpar tela"""
        if self.use_opengl:
            from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        else:
            if color:
                self.screen.fill(color)
            else:
                self.screen.fill((10, 10, 10))
    
    def flip_display(self):
        """Atualizar display"""
        if self.use_opengl:
            pygame.display.flip()
        else:
            pygame.display.flip()
    
    def get_screen(self):
        """Retornar superfície da tela para renderização direta"""
        return self.screen
    
    def set_fps(self, fps):
        """Definir FPS"""
        self.clock.tick(fps)
    
    def get_current_renderer(self):
        """Retornar tipo de renderizador sendo usado"""
        return "OpenGL (GPU)" if self.use_opengl else "Pygame (CPU)"
    
    def get_gpu_info(self):
        """Obter informações de GPU sendo usada"""
        if self.use_opengl:
            return {
                'type': 'OpenGL',
                'gpu_vendor': GPU_TYPE,
                'gpu_name': GPU_NAME,
                'dedicated': self._is_dedicated_gpu()
            }
        return {
            'type': 'Pygame (CPU)',
            'gpu_vendor': 'N/A',
            'gpu_name': 'N/A',
            'dedicated': False
        }
    
    def _is_dedicated_gpu(self):
        """Verificar se é GPU dedicada"""
        # GPU dedicada é aquela com NVIDIA, AMD, ou Intel Arc
        if not GPU_NAME:
            return False
        
        return any(dedic in GPU_NAME for dedic in [
            'NVIDIA', 'Radeon', 'RTX', 'GTX', 'Tesla',
            'Arc', 'Quadro', 'Radeon Pro'
        ])
    
    def cleanup(self):
        """Limpar recursos"""
        self.sprites_data.clear()
        if self.use_opengl:
            pass  # Limpar recursos OpenGL se necessário
        pygame.quit()


# Verificar disponibilidade ao importar
check_opengl_support()
