"""
Renderizador híbrido - OpenGL com fallback para Pygame
Detecta automaticamente disponibilidade de OpenGL
"""

import pygame
import sys
import os

# Flag de disponibilidade
OPENGL_AVAILABLE = False
RENDERER_TYPE = "PYGAME"  # Padrão

def check_opengl_support():
    """Verificar se OpenGL está disponível no sistema"""
    global OPENGL_AVAILABLE, RENDERER_TYPE
    
    try:
        from OpenGL.GL import glGetString, GL_VERSION
        import numpy
        import glm
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
    
    def cleanup(self):
        """Limpar recursos"""
        self.sprites_data.clear()
        if self.use_opengl:
            pass  # Limpar recursos OpenGL se necessário
        pygame.quit()


# Verificar disponibilidade ao importar
check_opengl_support()
