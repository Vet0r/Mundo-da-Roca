"""
Renderizador OpenGL para o jogo
Implementa renderização via GPU usando PyOpenGL
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import os
from pathlib import Path

class Shader:
    """Gerenciador de shaders OpenGL"""
    
    def __init__(self, vertex_src, fragment_src):
        self.program = glCreateProgram()
        
        # Compilar vertex shader
        vertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex, vertex_src)
        glCompileShader(vertex)
        self._check_compile_errors(vertex, "VERTEX")
        
        # Compilar fragment shader
        fragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment, fragment_src)
        glCompileShader(fragment)
        self._check_compile_errors(fragment, "FRAGMENT")
        
        # Linkar programa
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)
        glLinkProgram(self.program)
        self._check_compile_errors(self.program, "PROGRAM")
        
        glDeleteShader(vertex)
        glDeleteShader(fragment)
    
    def _check_compile_errors(self, shader, type_):
        """Verificar erros de compilação"""
        if type_ != "PROGRAM":
            success = glGetShaderiv(shader, GL_COMPILE_STATUS)
            if not success:
                info_log = glGetShaderInfoLog(shader)
                print(f"Erro de compilação do {type_}: {info_log.decode()}")
        else:
            success = glGetProgramiv(shader, GL_LINK_STATUS)
            if not success:
                info_log = glGetProgramInfoLog(shader)
                print(f"Erro de link do programa: {info_log.decode()}")
    
    def use(self):
        """Usar este shader"""
        glUseProgram(self.program)
    
    def set_mat4(self, name, mat):
        """Setar uniform de matriz 4x4"""
        loc = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat)
    
    def set_vec3(self, name, x, y=None, z=None):
        """Setar uniform de vetor 3D"""
        if y is None and z is None:
            x, y, z = x[0], x[1], x[2]
        loc = glGetUniformLocation(self.program, name)
        glUniform3f(loc, x, y, z)
    
    def set_vec2(self, name, x, y=None):
        """Setar uniform de vetor 2D"""
        if y is None:
            x, y = x[0], x[1]
        loc = glGetUniformLocation(self.program, name)
        glUniform2f(loc, x, y)
    
    def set_int(self, name, value):
        """Setar uniform inteiro"""
        loc = glGetUniformLocation(self.program, name)
        glUniform1i(loc, value)
    
    def set_float(self, name, value):
        """Setar uniform float"""
        loc = glGetUniformLocation(self.program, name)
        glUniform1f(loc, value)


class Texture:
    """Gerenciador de texturas OpenGL"""
    
    def __init__(self, image_path):
        self.id = glGenTextures(1)
        self.load(image_path)
    
    def load(self, image_path):
        """Carregar imagem como textura"""
        if not os.path.exists(image_path):
            print(f"Arquivo de textura não encontrado: {image_path}")
            return
        
        # Carregar imagem com pygame
        image = pygame.image.load(image_path)
        image = pygame.transform.flip(image, False, True)  # Flip para OpenGL
        image_data = pygame.image.tostring(image, "RGBA", True)
        
        width, height = image.get_size()
        
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    
    def bind(self):
        """Usar esta textura"""
        glBindTexture(GL_TEXTURE_2D, self.id)
    
    def delete(self):
        """Deletar textura"""
        glDeleteTextures([self.id])


class Sprite:
    """Sprite renderizável via OpenGL"""
    
    def __init__(self, texture_path, x=0, y=0, width=40, height=40):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        
        try:
            self.texture = Texture(texture_path)
        except:
            self.texture = None
        
        self._setup_vertices()
    
    def _setup_vertices(self):
        """Configurar vértices do sprite"""
        vertices = np.array([
            # posição          # coordenada de textura
            0.0, 0.0,          0.0, 0.0,  # Canto inferior-esquerdo
            self.width, 0.0,   1.0, 0.0,  # Canto inferior-direito
            self.width, self.height, 1.0, 1.0,  # Canto superior-direito
            0.0, self.height,  0.0, 1.0,  # Canto superior-esquerdo
        ], dtype=np.float32)
        
        indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
        
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        
        glBindVertexArray(self.VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        # Atributo de posição
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Atributo de coordenada de textura
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
    
    def render(self, shader, projection_matrix):
        """Renderizar sprite"""
        if self.texture is None:
            return
        
        import glm
        
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(self.x, self.y, 0.0))
        model = glm.scale(model, glm.vec3(self.scale_x, self.scale_y, 1.0))
        
        shader.use()
        shader.set_mat4("projection", projection_matrix)
        shader.set_mat4("model", model)
        
        self.texture.bind()
        
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    
    def update_position(self, x, y):
        """Atualizar posição"""
        self.x = x
        self.y = y
    
    def cleanup(self):
        """Limpar recursos"""
        if self.texture:
            self.texture.delete()
        glDeleteBuffers(1, [self.VBO])
        glDeleteBuffers(1, [self.EBO])
        glDeleteVertexArrays(1, [self.VAO])


class OpenGLRenderer:
    """Renderizador principal com OpenGL"""
    
    # Shaders padrão
    VERTEX_SHADER = """
    #version 330 core
    layout (location = 0) in vec2 position;
    layout (location = 1) in vec2 texCoord;
    
    out vec2 TexCoord;
    
    uniform mat4 projection;
    uniform mat4 model;
    
    void main()
    {
        gl_Position = projection * model * vec4(position, 0.0, 1.0);
        TexCoord = texCoord;
    }
    """
    
    FRAGMENT_SHADER = """
    #version 330 core
    in vec2 TexCoord;
    out vec4 FragColor;
    
    uniform sampler2D texture1;
    
    void main()
    {
        FragColor = texture(texture1, TexCoord);
    }
    """
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sprites = []
        
        # Inicializar OpenGL
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        
        # Criar shader
        self.shader = Shader(self.VERTEX_SHADER, self.FRAGMENT_SHADER)
        
        # Matriz de projeção ortográfica
        import glm
        self.projection = glm.ortho(0.0, float(width), 0.0, float(height), -1.0, 1.0)
    
    def add_sprite(self, sprite):
        """Adicionar sprite à cena"""
        self.sprites.append(sprite)
    
    def render_frame(self):
        """Renderizar frame"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        for sprite in self.sprites:
            sprite.render(self.shader, self.projection)
    
    def cleanup(self):
        """Limpar todos os recursos"""
        for sprite in self.sprites:
            sprite.cleanup()
        self.sprites.clear()


# Detectar disponibilidade de OpenGL
def is_opengl_available():
    """Verificar se OpenGL está disponível"""
    try:
        import ctypes
        from OpenGL.GL import glGetString, GL_VERSION
        # Tentar obter versão do OpenGL
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        
        test_display = pygame.display.set_mode((100, 100), pygame.OPENGL | pygame.HIDDEN)
        version = glGetString(GL_VERSION)
        pygame.display.quit()
        print(f"✓ OpenGL disponível: {version}")
        return True
    except Exception as e:
        print(f"✗ OpenGL não disponível: {e}")
        return False
