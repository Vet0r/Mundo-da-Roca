import pygame
import time
from config import TIPOS_SEMENTE, CORES, TAMANHO_CELULA, POCO_POS

class UI:
    def __init__(self):
        self.fonte = pygame.font.Font(None, 24)
        self.fonte_titulo = pygame.font.Font(None, 32)
        self.mensagem_save = ""
        self.tempo_mensagem = 0
    
    def desenhar_interface(self, tela, player, water_system, modo_atual):
        pygame.draw.rect(tela, CORES['fundo_interface'], (10, 10, 300, 180))
        pygame.draw.rect(tela, CORES['borda_interface'], (10, 10, 300, 180), 2)
        
        texto_dinheiro = self.fonte.render(f"Dinheiro: ${player.dinheiro}", True, CORES['texto'])
        tela.blit(texto_dinheiro, (20, 25))
        
        y_offset = 50
        for tipo, quantidade in player.sementes.items():
            cor = TIPOS_SEMENTE[tipo]['cor']
            texto = f"{tipo.capitalize()}: {quantidade}"
            if tipo == player.semente_selecionada:
                texto += " ◄"
            texto_semente = self.fonte.render(texto, True, cor)
            tela.blit(texto_semente, (20, y_offset))
            y_offset += 25
        
        modo_texto, cor_modo = self._get_modo_info(modo_atual)
        texto_modo = self.fonte_titulo.render(modo_texto, True, cor_modo)
        tela.blit(texto_modo, (20, 130))
        
        if water_system.tem_balde_agua:
            texto_balde = self.fonte.render("💧 Carregando água", True, CORES['agua_indicador'])
            tela.blit(texto_balde, (20, 160))
        
        self._desenhar_instrucoes(tela)
        self._desenhar_mensagem_save(tela, tela.get_width())
    
    def _get_modo_info(self, modo_atual):
        modos = {
            'limpar': ("MODO: LIMPAR", CORES['modo_limpar']),
            'agua': ("MODO: ÁGUA", CORES['modo_agua']),
            'adubar': ("MODO: ADUBAR", CORES['modo_adubar']),
            'plantar': ("MODO: PLANTAR", CORES['modo_plantar'])
        }
        return modos.get(modo_atual, modos['plantar'])
    
    def _desenhar_instrucoes(self, tela):
        instrucoes = [
            "A: Adubar | W: Água | R: Limpar",
            "ESPAÇO: Ação nos modos",
            "  - Limpar: Remover plantas podres",
            "  - Adubar: Preparar terra aguada",
            "  - Água: Cavar/Encher/Pegar água",
            "  - Plantar: Plantar/Colher",
            "1,2,3: Selecionar semente",
            "L: Abrir/Fechar Loja",
            "S: Salvar jogo",
        ]
        
        y_offset = 390
        for instrucao in instrucoes:
            texto = self.fonte.render(instrucao, True, CORES['texto'])
            tela.blit(texto, (20, y_offset))
            y_offset += 20
    
    def _desenhar_mensagem_save(self, tela, largura_tela):
        if self.mensagem_save and (time.time() - self.tempo_mensagem < 3):
            cor_mensagem = CORES['verde_sucesso'] if "sucesso" in self.mensagem_save else CORES['vermelho_erro']
            texto_save = self.fonte.render(self.mensagem_save, True, cor_mensagem)
            tela.blit(texto_save, (largura_tela // 2 - texto_save.get_width() // 2, 30))
    
    def mostrar_mensagem_save(self, mensagem):
        self.mensagem_save = mensagem
        self.tempo_mensagem = time.time()
    
    def desenhar_planta(self, tela, x, y, tipo_semente, estagio, sprites):
        if tipo_semente in sprites['plantas'] and estagio in sprites['plantas'][tipo_semente]:
            sprite = sprites['plantas'][tipo_semente][estagio]
            tela.blit(sprite, (x, y))
        else:
            cor = TIPOS_SEMENTE.get(tipo_semente, {}).get('cor', (255, 255, 255))
            tamanho = min(estagio * 4, 30)
            if estagio == 7:
                cor = (139, 69, 19)
            pygame.draw.circle(tela, cor, (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2), tamanho // 2)
    
    def desenhar_cenario(self, tela, sprites, water_system, farm_system, largura, altura):
        for i in range(0, largura, sprites['grama'].get_width()):
            for j in range(0, altura, sprites['grama'].get_height()):
                tela.blit(sprites['grama'], (i, j))
        
        for i in range(0, largura, TAMANHO_CELULA):
            pygame.draw.line(tela, CORES['grade'], (i, 0), (i, altura), 1)
        for j in range(0, altura, TAMANHO_CELULA):
            pygame.draw.line(tela, CORES['grade'], (0, j), (largura, j), 1)
        
        for (grid_x, grid_y) in water_system.terra_aguada:
            x_pos = grid_x * TAMANHO_CELULA
            y_pos = grid_y * TAMANHO_CELULA
            tela.blit(sprites['terra_aguada'], (x_pos, y_pos))
        
        for (grid_x, grid_y) in farm_system.terra_adubada:
            x_pos = grid_x * TAMANHO_CELULA
            y_pos = grid_y * TAMANHO_CELULA
            tela.blit(sprites['terra'], (x_pos, y_pos))
        
        poco_x = POCO_POS[0] * TAMANHO_CELULA
        poco_y = POCO_POS[1] * TAMANHO_CELULA
        tela.blit(sprites['poco'], (poco_x, poco_y))
        
        for (grid_x, grid_y) in water_system.buracos_com_agua:
            x_pos = grid_x * TAMANHO_CELULA
            y_pos = grid_y * TAMANHO_CELULA
            tela.blit(sprites['agua'], (x_pos, y_pos))
        
        for (grid_x, grid_y), planta in farm_system.fazenda.items():
            x_pos = grid_x * TAMANHO_CELULA
            y_pos = grid_y * TAMANHO_CELULA
            self.desenhar_planta(tela, x_pos, y_pos, planta['tipo'], planta['estagio'], sprites)
    
    def desenhar_cursor(self, tela, player):
        grid_x, grid_y = player.get_grid_position()
        x_pos = grid_x * TAMANHO_CELULA
        y_pos = grid_y * TAMANHO_CELULA
        pygame.draw.rect(tela, CORES['texto'], (x_pos, y_pos, TAMANHO_CELULA, TAMANHO_CELULA), 2)
    
    def desenhar_trabalhadores(self, tela, worker_system, sprites):
        cores_trabalhador = {
            'cultivador': (100, 255, 100),
            'coletador': (255, 215, 0),
            'adubador': (139, 69, 19)
        }
        
        for tipo, x, y in worker_system.obter_trabalhadores_ativos():
            cor = cores_trabalhador.get(tipo, (255, 255, 255))
            
            corpo_rect = pygame.Rect(int(x), int(y) + 10, 25, 35)
            pygame.draw.rect(tela, cor, corpo_rect, border_radius=5)
            pygame.draw.rect(tela, (0, 0, 0), corpo_rect, 2, border_radius=5)
            
            pygame.draw.circle(tela, cor, (int(x + 12), int(y + 8)), 8)
            pygame.draw.circle(tela, (0, 0, 0), (int(x + 12), int(y + 8)), 8, 2)
            
            icone_map = {
                'cultivador': '🌱',
                'coletador': '🧺',
                'adubador': '🪴'
            }
            icone = icone_map.get(tipo, '👷')
            texto_icone = self.fonte.render(icone, True, (0, 0, 0))
            tela.blit(texto_icone, (int(x + 2), int(y + 18)))
