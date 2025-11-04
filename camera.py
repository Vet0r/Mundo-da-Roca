from config import LARGURA, ALTURA

class Camera:
    def __init__(self, player, largura=LARGURA, altura=ALTURA):
        self.player = player
        self.offset_x = 0
        self.offset_y = 0
        self.largura_tela = largura
        self.altura_tela = altura
    
    def atualizar(self, largura=None, altura=None):
        # Atualizar dimensões da tela se fornecidas
        if largura is not None:
            self.largura_tela = largura
        if altura is not None:
            self.altura_tela = altura
        
        # Centraliza a câmera no jogador usando as dimensões atuais
        self.offset_x = self.player.x - self.largura_tela // 2
        self.offset_y = self.player.y - self.altura_tela // 2
    
    def aplicar(self, x, y):
        """Converte coordenadas do mundo para coordenadas da tela"""
        return x - self.offset_x, y - self.offset_y
    
    def aplicar_grid(self, grid_x, grid_y, tamanho_celula):
        """Converte coordenadas de grid para coordenadas da tela"""
        mundo_x = grid_x * tamanho_celula
        mundo_y = grid_y * tamanho_celula
        return self.aplicar(mundo_x, mundo_y)
    
    def reverter(self, tela_x, tela_y):
        """Converte coordenadas da tela para coordenadas do mundo"""
        return tela_x + self.offset_x, tela_y + self.offset_y
    
    def reverter_para_grid(self, tela_x, tela_y, tamanho_celula):
        """Converte coordenadas da tela para coordenadas de grid"""
        mundo_x, mundo_y = self.reverter(tela_x, tela_y)
        return int(mundo_x // tamanho_celula), int(mundo_y // tamanho_celula)
    
    def esta_visivel(self, mundo_x, mundo_y, largura_obj=0, altura_obj=0):
        """Verifica se um objeto está visível na tela"""
        tela_x, tela_y = self.aplicar(mundo_x, mundo_y)
        margem = 100  # Margem extra para renderizar objetos próximos às bordas
        return (-margem <= tela_x <= self.largura_tela + margem and 
                -margem <= tela_y <= self.altura_tela + margem)
