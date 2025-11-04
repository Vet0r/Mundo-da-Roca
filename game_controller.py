import pygame
from config import TAMANHO_CELULA

class GameController:
    def __init__(self, player, farm_system, water_system):
        self.player = player
        self.farm_system = farm_system
        self.water_system = water_system
        self.modo_adubar = False
        self.modo_agua = False
        self.modo_limpar = False
    
    def get_modo_atual(self):
        if self.modo_limpar:
            return 'limpar'
        elif self.modo_agua:
            return 'agua'
        elif self.modo_adubar:
            return 'adubar'
        else:
            return 'plantar'
    
    def alternar_modo(self, modo):
        if modo == 'adubar':
            self.modo_agua = False
            self.modo_limpar = False
            self.modo_adubar = not self.modo_adubar
            return 'ADUBAR' if self.modo_adubar else 'PLANTAR'
        elif modo == 'agua':
            self.modo_adubar = False
            self.modo_limpar = False
            self.modo_agua = not self.modo_agua
            return 'ÁGUA' if self.modo_agua else 'PLANTAR'
        elif modo == 'limpar':
            self.modo_adubar = False
            self.modo_agua = False
            self.modo_limpar = not self.modo_limpar
            return 'LIMPAR' if self.modo_limpar else 'PLANTAR'
    
    def executar_acao(self):
        pos_x, pos_y = self.player.get_pixel_position_center()
        grid_x = pos_x // TAMANHO_CELULA
        grid_y = pos_y // TAMANHO_CELULA
        
        if self.modo_limpar:
            # Tenta remover planta podre primeiro, se não houver, remove água
            if not self.farm_system.remover_planta_podre(grid_x, grid_y):
                self.water_system.remover_agua(grid_x, grid_y)
        elif self.modo_agua:
            if not self.water_system.tem_balde_agua:
                if not self.water_system.pegar_agua_do_poco(pos_x, pos_y, TAMANHO_CELULA):
                    if self.water_system.cavar_buraco(grid_x, grid_y, self.farm_system.fazenda):
                        if (grid_x, grid_y) in self.farm_system.terra_adubada:
                            self.farm_system.terra_adubada.discard((grid_x, grid_y))
            else:
                self.water_system.encher_buraco_com_agua(grid_x, grid_y, self.farm_system.fazenda)
        elif self.modo_adubar:
            self.farm_system.adubar_terra(grid_x, grid_y, self.water_system)
        else:
            colheu, valor = self.farm_system.colher_planta(grid_x, grid_y)
            if colheu:
                self.player.adicionar_dinheiro(valor)
            else:
                self.farm_system.plantar_semente(grid_x, grid_y, self.player.semente_selecionada, 
                                                 self.player.sementes, self.water_system)
    
    def processar_movimento(self, teclas, largura, altura):
        direcoes = [
            teclas[pygame.K_LEFT],
            teclas[pygame.K_RIGHT],
            teclas[pygame.K_UP],
            teclas[pygame.K_DOWN]
        ]
        self.player.mover(direcoes, largura, altura)
