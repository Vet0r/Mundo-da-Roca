from config import TAMANHO_CELULA

class Player:
    def __init__(self, x=100, y=100, velocidade=5):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.dinheiro = 100
        self.sementes = {'milho': 20, 'tomate': 10, 'alface': 30}
        self.semente_selecionada = 'milho'
        self.tem_poco = False  # Indica se o jogador comprou um poço para posicionar
    
    def mover(self, teclas, largura=None, altura=None):
        # Mapa infinito - sem restrições de borda
        if teclas[0]:
            self.x -= self.velocidade
        if teclas[1]:
            self.x += self.velocidade
        if teclas[2]:
            self.y -= self.velocidade
        if teclas[3]:
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
