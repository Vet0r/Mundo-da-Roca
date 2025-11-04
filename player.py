from config import TAMANHO_CELULA

class Player:
    def __init__(self, x=100, y=100, velocidade=5):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.dinheiro = 100
        self.sementes = {'milho': 5, 'tomate': 3, 'alface': 2}
        self.semente_selecionada = 'milho'
    
    def mover(self, teclas, largura, altura):
        if teclas[0] and self.x > 0:
            self.x -= self.velocidade
        if teclas[1] and self.x < largura - 40:
            self.x += self.velocidade
        if teclas[2] and self.y > 0:
            self.y -= self.velocidade
        if teclas[3] and self.y < altura - 75:
            self.y += self.velocidade
    
    def get_grid_position(self):
        grid_x = (self.x + 20) // TAMANHO_CELULA
        grid_y = (self.y + 37) // TAMANHO_CELULA
        return grid_x, grid_y
    
    def get_pixel_position_center(self):
        return self.x + 20, self.y + 37
    
    def selecionar_semente(self, numero):
        sementes_list = ['milho', 'tomate', 'alface']
        if 0 <= numero < len(sementes_list):
            self.semente_selecionada = sementes_list[numero]
    
    def adicionar_dinheiro(self, valor):
        self.dinheiro += valor
    
    def gastar_dinheiro(self, valor):
        if self.dinheiro >= valor:
            self.dinheiro -= valor
            return True
        return False
    
    def adicionar_sementes(self, tipo, quantidade):
        self.sementes[tipo] += quantidade
    
    def carregar_dados(self, dinheiro, sementes):
        self.dinheiro = dinheiro
        self.sementes = sementes
