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
    
    def desenhar_cenario(self, tela, sprites, water_system, farm_system, largura, altura, camera):
        # Calcular área visível em coordenadas de grid
        min_grid_x = int(camera.offset_x // TAMANHO_CELULA) - 2
        max_grid_x = int((camera.offset_x + largura) // TAMANHO_CELULA) + 2
        min_grid_y = int(camera.offset_y // TAMANHO_CELULA) - 2
        max_grid_y = int((camera.offset_y + altura) // TAMANHO_CELULA) + 2
        
        # Desenhar grama de fundo
        grama_width = sprites['grama'].get_width()
        grama_height = sprites['grama'].get_height()
        
        inicio_x = int((camera.offset_x // grama_width) * grama_width)
        inicio_y = int((camera.offset_y // grama_height) * grama_height)
        
        for i in range(inicio_x, int(camera.offset_x + largura + grama_width), grama_width):
            for j in range(inicio_y, int(camera.offset_y + altura + grama_height), grama_height):
                tela_x, tela_y = camera.aplicar(i, j)
                tela.blit(sprites['grama'], (tela_x, tela_y))
        
        # Desenhar grade
        for i in range(min_grid_x, max_grid_x + 1):
            mundo_x = i * TAMANHO_CELULA
            tela_x, _ = camera.aplicar(mundo_x, 0)
            pygame.draw.line(tela, CORES['grade'], (tela_x, 0), (tela_x, altura), 1)
        
        for j in range(min_grid_y, max_grid_y + 1):
            mundo_y = j * TAMANHO_CELULA
            _, tela_y = camera.aplicar(0, mundo_y)
            pygame.draw.line(tela, CORES['grade'], (0, tela_y), (largura, tela_y), 1)
        
        # Desenhar terra aguada (apenas células visíveis)
        for (grid_x, grid_y) in water_system.terra_aguada:
            if min_grid_x <= grid_x <= max_grid_x and min_grid_y <= grid_y <= max_grid_y:
                tela_x, tela_y = camera.aplicar_grid(grid_x, grid_y, TAMANHO_CELULA)
                tela.blit(sprites['terra_aguada'], (tela_x, tela_y))
        
        # Desenhar terra adubada (apenas células visíveis)
        for (grid_x, grid_y) in farm_system.terra_adubada:
            if min_grid_x <= grid_x <= max_grid_x and min_grid_y <= grid_y <= max_grid_y:
                tela_x, tela_y = camera.aplicar_grid(grid_x, grid_y, TAMANHO_CELULA)
                tela.blit(sprites['terra'], (tela_x, tela_y))
        
        # Desenhar poço
        poco_x = POCO_POS[0] * TAMANHO_CELULA
        poco_y = POCO_POS[1] * TAMANHO_CELULA
        tela_x, tela_y = camera.aplicar(poco_x, poco_y)
        tela.blit(sprites['poco'], (tela_x, tela_y))
        
        # Desenhar buracos com água (apenas células visíveis)
        for (grid_x, grid_y) in water_system.buracos_com_agua:
            if min_grid_x <= grid_x <= max_grid_x and min_grid_y <= grid_y <= max_grid_y:
                tela_x, tela_y = camera.aplicar_grid(grid_x, grid_y, TAMANHO_CELULA)
                tela.blit(sprites['agua'], (tela_x, tela_y))
        
        # Desenhar plantas (apenas células visíveis)
        for (grid_x, grid_y), planta in farm_system.fazenda.items():
            if min_grid_x <= grid_x <= max_grid_x and min_grid_y <= grid_y <= max_grid_y:
                tela_x, tela_y = camera.aplicar_grid(grid_x, grid_y, TAMANHO_CELULA)
                self.desenhar_planta(tela, tela_x, tela_y, planta['tipo'], planta['estagio'], sprites)
    
    def desenhar_cursor(self, tela, player, camera):
        grid_x, grid_y = player.get_grid_position()
        tela_x, tela_y = camera.aplicar_grid(grid_x, grid_y, TAMANHO_CELULA)
        pygame.draw.rect(tela, CORES['texto'], (tela_x, tela_y, TAMANHO_CELULA, TAMANHO_CELULA), 2)
    
    def desenhar_trabalhadores(self, tela, worker_system, sprites, camera):
        cores_trabalhador = {
            'cultivador': (100, 255, 100),
            'coletador': (255, 215, 0),
            'adubador': (139, 69, 19)
        }
        
        for tipo, x, y in worker_system.obter_trabalhadores_ativos():
            # Converter posição do mundo para tela
            tela_x, tela_y = camera.aplicar(x, y)
            
            # Verificar se está visível
            if -50 <= tela_x <= tela.get_width() + 50 and -50 <= tela_y <= tela.get_height() + 50:
                cor = cores_trabalhador.get(tipo, (255, 255, 255))
                
                corpo_rect = pygame.Rect(int(tela_x), int(tela_y) + 10, 25, 35)
                pygame.draw.rect(tela, cor, corpo_rect, border_radius=5)
                pygame.draw.rect(tela, (0, 0, 0), corpo_rect, 2, border_radius=5)
                
                pygame.draw.circle(tela, cor, (int(tela_x + 12), int(tela_y + 8)), 8)
                pygame.draw.circle(tela, (0, 0, 0), (int(tela_x + 12), int(tela_y + 8)), 8, 2)
                
                icone_map = {
                    'cultivador': '🌱',
                    'coletador': '🧺',
                    'adubador': '🪴'
                }
                icone = icone_map.get(tipo, '👷')
                texto_icone = self.fonte.render(icone, True, (0, 0, 0))
                tela.blit(texto_icone, (int(tela_x + 2), int(tela_y + 18)))
