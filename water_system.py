from config import POCO_POS

class WaterSystem:
    def __init__(self):
        self.buracos_com_agua = set()
        self.terra_aguada = set()
        self.tem_balde_agua = False
        self.pocos = [POCO_POS]  # Lista de posições de poços (começa com o poço padrão)
    
    @staticmethod
    def distancia_manhattan(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def adicionar_poco(self, grid_x, grid_y):
        """Adiciona um novo poço na posição especificada"""
        posicao = (grid_x, grid_y)
        # Verificar se não está muito perto de outro poço
        for poco in self.pocos:
            if self.distancia_manhattan(posicao, poco) < 5:
                return False, "muito_proximo"
        
        # Verificar se não tem planta ou água no local
        if posicao in self.buracos_com_agua:
            return False, "tem_agua"
        
        self.pocos.append(posicao)
        return True, "sucesso"
    
    def atualizar_terra_aguada(self):
        self.terra_aguada.clear()
        
        for buraco in self.buracos_com_agua:
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if self.distancia_manhattan((0, 0), (dx, dy)) <= 5:
                        pos_terra = (buraco[0] + dx, buraco[1] + dy)
                        if (pos_terra not in self.buracos_com_agua and 
                            pos_terra != POCO_POS and
                            pos_terra != (POCO_POS[0] + 1, POCO_POS[1]) and
                            pos_terra != (POCO_POS[0], POCO_POS[1] + 1) and
                            pos_terra != (POCO_POS[0] + 1, POCO_POS[1] + 1)):
                            self.terra_aguada.add(pos_terra)
    
    def cavar_buraco(self, grid_x, grid_y, fazenda):
        posicao = (grid_x, grid_y)
        if (posicao != POCO_POS and 
            posicao != (POCO_POS[0] + 1, POCO_POS[1]) and
            posicao != (POCO_POS[0], POCO_POS[1] + 1) and
            posicao != (POCO_POS[0] + 1, POCO_POS[1] + 1) and
            posicao not in fazenda and 
            posicao not in self.buracos_com_agua):
            return True
        return False
    
    def encher_buraco_com_agua(self, grid_x, grid_y, fazenda, player):
        posicao = (grid_x, grid_y)
        if (self.tem_balde_agua and 
            posicao not in self.buracos_com_agua and 
            posicao not in fazenda and
            posicao != POCO_POS and
            posicao != (POCO_POS[0] + 1, POCO_POS[1]) and
            posicao != (POCO_POS[0], POCO_POS[1] + 1) and
            posicao != (POCO_POS[0] + 1, POCO_POS[1] + 1)):
            if player.gastar_dinheiro(5):
                self.buracos_com_agua.add(posicao)
                self.tem_balde_agua = False
                return True, "agua_colocada"
            else:
                return False, "sem_dinheiro"
        return False, "invalido"
    
    def pegar_agua_do_poco(self, pos_jogador_x, pos_jogador_y, tamanho_celula):
        grid_x = pos_jogador_x // tamanho_celula
        grid_y = pos_jogador_y // tamanho_celula
        
        # Verifica se está perto de algum poço
        for poco in self.pocos:
            if self.distancia_manhattan((grid_x, grid_y), poco) <= 2:
                self.tem_balde_agua = True
                return True
        return False
    
    def remover_agua(self, grid_x, grid_y):
        posicao = (grid_x, grid_y)
        if posicao in self.buracos_com_agua:
            self.buracos_com_agua.discard(posicao)
            self.atualizar_terra_aguada()
            return True
        return False
    
    def carregar_dados(self, buracos, terra_aguada, pocos=None):
        self.buracos_com_agua = set(tuple(pos) for pos in buracos)
        self.terra_aguada = set(tuple(pos) for pos in terra_aguada)
        if pocos:
            self.pocos = [tuple(pos) for pos in pocos]
        else:
            self.pocos = [POCO_POS]
    
    def obter_dados_save(self):
        return {
            'buracos_com_agua': [list(pos) for pos in self.buracos_com_agua],
            'terra_aguada': [list(pos) for pos in self.terra_aguada],
            'pocos': [list(pos) for pos in self.pocos]
        }
