import pygame
from config import TIPOS_SEMENTE, CORES
from sound_system import SoundSystem

class Shop:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.aberta = False
        self.item_selecionado = 0
        self.aba_atual = 'sementes'
        self.fonte_titulo = pygame.font.Font(None, 32)
        self.fonte = pygame.font.Font(None, 24)
        self.sound_system = SoundSystem()
    
    def toggle(self):
        self.aberta = not self.aberta
        if not self.aberta:
            self.item_selecionado = 0
            self.aba_atual = 'sementes'
    
    def trocar_aba(self):
        abas = ['sementes', 'trabalhadores', 'utilidades']
        idx_atual = abas.index(self.aba_atual)
        idx_novo = (idx_atual + 1) % len(abas)
        self.aba_atual = abas[idx_novo]
        self.item_selecionado = 0
        self.sound_system.tocar_sfx('arrow')
    
    def atualizar_dimensoes(self, largura, altura):
        self.largura = largura
        self.altura = altura
    
    def navegar(self, direcao):
        if self.aba_atual == 'sementes':
            max_itens = 3
        elif self.aba_atual == 'trabalhadores':
            max_itens = 3
        else:  # utilidades
            max_itens = 1
        
        if direcao == 'cima':
            self.item_selecionado = (self.item_selecionado - 1) % max_itens
        elif direcao == 'baixo':
            self.item_selecionado = (self.item_selecionado + 1) % max_itens
        self.sound_system.tocar_sfx('arrow')
    
    def comprar_semente(self, player, quantidade=1):
        tipos_ordenados = list(TIPOS_SEMENTE.keys())
        tipo_selecionado = tipos_ordenados[self.item_selecionado]
        preco_total = TIPOS_SEMENTE[tipo_selecionado]['preco'] * quantidade
        
        if player.gastar_dinheiro(preco_total):
            player.adicionar_sementes(tipo_selecionado, quantidade)
            self.sound_system.tocar_sfx('select')
            return True
        else:
            self.sound_system.tocar_sfx('select_erro')
            return False
    
    def contratar_trabalhador(self, player, worker_system, posicao_spawn):
        tipos_trabalhador = ['cultivador', 'coletador', 'adubador']
        tipo_selecionado = tipos_trabalhador[self.item_selecionado]
        
        sucesso = worker_system.contratar_trabalhador(tipo_selecionado, player, posicao_spawn)
        if sucesso:
            self.sound_system.tocar_sfx('select')
        else:
            self.sound_system.tocar_sfx('select_erro')
        return sucesso
    
    def comprar_poco(self, player):
        if player.gastar_dinheiro(1000):
            player.tem_poco = True
            self.sound_system.tocar_sfx('select')
            return True
        else:
            self.sound_system.tocar_sfx('select_erro')
            return False
    
    def desenhar(self, tela, worker_system=None):
        largura_loja = 450
        altura_loja = 500
        x_loja = (self.largura - largura_loja) // 2
        y_loja = (self.altura - altura_loja) // 2
        
        pygame.draw.rect(tela, CORES['loja_fundo'], (x_loja, y_loja, largura_loja, altura_loja))
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja, y_loja, largura_loja, altura_loja), 3)
        
        titulo_map = {
            'sementes': 'SEMENTES',
            'trabalhadores': 'TRABALHADORES',
            'utilidades': 'UTILIDADES'
        }
        titulo_texto = "LOJA - " + titulo_map.get(self.aba_atual, 'SEMENTES')
        titulo = self.fonte_titulo.render(titulo_texto, True, CORES['texto'])
        titulo_rect = titulo.get_rect(center=(self.largura // 2, y_loja + 30))
        tela.blit(titulo, titulo_rect)
        
        self._desenhar_abas(tela, x_loja, y_loja, largura_loja)
        
        y_offset = y_loja + 110
        
        if self.aba_atual == 'sementes':
            self._desenhar_sementes(tela, x_loja, y_loja, y_offset, largura_loja)
        elif self.aba_atual == 'trabalhadores':
            self._desenhar_trabalhadores(tela, x_loja, y_loja, y_offset, largura_loja, worker_system)
        else:  # utilidades
            self._desenhar_utilidades(tela, x_loja, y_loja, y_offset, largura_loja)
        
    def _desenhar_abas(self, tela, x_loja, y_loja, largura_loja):
        aba_largura = largura_loja // 3
        
        cor_aba_sementes = CORES['loja_destaque'] if self.aba_atual == 'sementes' else CORES['loja_fundo']
        cor_aba_trabalhadores = CORES['loja_destaque'] if self.aba_atual == 'trabalhadores' else CORES['loja_fundo']
        cor_aba_utilidades = CORES['loja_destaque'] if self.aba_atual == 'utilidades' else CORES['loja_fundo']
        
        pygame.draw.rect(tela, cor_aba_sementes, (x_loja, y_loja + 60, aba_largura, 35))
        pygame.draw.rect(tela, cor_aba_trabalhadores, (x_loja + aba_largura, y_loja + 60, aba_largura, 35))
        pygame.draw.rect(tela, cor_aba_utilidades, (x_loja + aba_largura * 2, y_loja + 60, aba_largura, 35))
        
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja, y_loja + 60, aba_largura, 35), 2)
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja + aba_largura, y_loja + 60, aba_largura, 35), 2)
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja + aba_largura * 2, y_loja + 60, aba_largura, 35), 2)
        
        fonte_pequena = pygame.font.Font(None, 20)
        texto_sementes = fonte_pequena.render("Sementes", True, CORES['texto'])
        texto_trabalhadores = fonte_pequena.render("Trabalhadores", True, CORES['texto'])
        texto_utilidades = fonte_pequena.render("Utilidades", True, CORES['texto'])
        
        tela.blit(texto_sementes, (x_loja + aba_largura//2 - texto_sementes.get_width()//2, y_loja + 72))
        tela.blit(texto_trabalhadores, (x_loja + aba_largura + aba_largura//2 - texto_trabalhadores.get_width()//2, y_loja + 72))
        tela.blit(texto_utilidades, (x_loja + aba_largura*2 + aba_largura//2 - texto_utilidades.get_width()//2, y_loja + 72))
    
    def _desenhar_sementes(self, tela, x_loja, y_loja, y_offset, largura_loja):
        tipos_ordenados = list(TIPOS_SEMENTE.keys())
        
        for i, tipo in enumerate(tipos_ordenados):
            info = TIPOS_SEMENTE[tipo]
            cor = info['cor']
            preco = info['preco']
            
            if i == self.item_selecionado:
                pygame.draw.rect(tela, CORES['loja_destaque'], (x_loja + 10, y_offset - 5, largura_loja - 20, 30))
            
            texto_item = self.fonte.render(f"{tipo.capitalize()}: ${preco} cada", True, cor)
            tela.blit(texto_item, (x_loja + 20, y_offset))
            
            if i == self.item_selecionado:
                seta = self.fonte.render("[<<]", True, CORES['texto'])
                tela.blit(seta, (x_loja + largura_loja - 50, y_offset))
            
            y_offset += 35
        
        instrucoes = [
            "UP/DOWN: Navegar | TAB: Trocar aba",
            "",
            "Quantidade de sementes:",
            "  1: Comprar 1   |   5: Comprar 5",
            "  0: Comprar 10",
            "  SHIFT+ENTER: Comprar 50",
            "  ALT+ENTER: Comprar 100",
            "",
            "L ou ESC: Fechar loja"
        ]
        
        y_offset += 10
        for instrucao in instrucoes:
            if instrucao == "":
                y_offset += 10
            else:
                texto = self.fonte.render(instrucao, True, CORES['cinza_info'])
                tela.blit(texto, (x_loja + 20, y_offset))
                y_offset += 20
    
    def _desenhar_trabalhadores(self, tela, x_loja, y_loja, y_offset, largura_loja, worker_system):
        tipos_trabalhador = [
            ('cultivador', 'Cultivador - Planta sementes', (100, 255, 100)),
            ('coletador', 'Coletador - Colhe plantas', (255, 215, 0)),
            ('adubador', 'Adubador - Aduba terra', (139, 69, 19))
        ]
        
        contagem_ativos, contagem_total = worker_system.contar_trabalhadores_por_tipo() if worker_system else ({}, {})
        
        for i, (tipo, nome, cor) in enumerate(tipos_trabalhador):
            if i == self.item_selecionado:
                pygame.draw.rect(tela, CORES['loja_destaque'], (x_loja + 10, y_offset - 5, largura_loja - 20, 55))
            
            texto_item = self.fonte.render(f"{nome} - $300", True, cor)
            tela.blit(texto_item, (x_loja + 20, y_offset))
            
            ativos = contagem_ativos.get(tipo, 0)
            total = contagem_total.get(tipo, 0)
            texto_ativos = self.fonte.render(f"Trabalhando: {ativos}/{total} (${total}/20s)", True, CORES['cinza_info'])
            tela.blit(texto_ativos, (x_loja + 20, y_offset + 20))
            
            if i == self.item_selecionado:
                seta = self.fonte.render("[<<]", True, CORES['texto'])
                tela.blit(seta, (x_loja + largura_loja - 50, y_offset))
            
            y_offset += 60
        
        instrucoes = [
            "UP/DOWN: Navegar | TAB: Trocar aba",
            "ENTER: Contratar trabalhador",
            "",
            "[!] Cada trabalhador custa $1 a cada 20s",
            "Trabalhadores param se você ficar sem $",
            "Voltam a trabalhar quando houver dinheiro",
            "",
            "L ou ESC: Fechar loja"
        ]
        
        y_offset += 10
        for instrucao in instrucoes:
            if instrucao == "":
                y_offset += 8
            else:
                texto = self.fonte.render(instrucao, True, CORES['cinza_info'])
                tela.blit(texto, (x_loja + 20, y_offset))
                y_offset += 18
    
    def _desenhar_utilidades(self, tela, x_loja, y_loja, y_offset, largura_loja):
        # Apenas o poço por enquanto
        if self.item_selecionado == 0:
            pygame.draw.rect(tela, CORES['loja_destaque'], (x_loja + 10, y_offset - 5, largura_loja - 20, 55))
        
        texto_item = self.fonte.render("Poço - $1000", True, (50, 150, 255))
        tela.blit(texto_item, (x_loja + 20, y_offset))
        
        texto_descricao = self.fonte.render("Permite pegar água em qualquer lugar", True, CORES['cinza_info'])
        tela.blit(texto_descricao, (x_loja + 20, y_offset + 25))
        
        if self.item_selecionado == 0:
            seta = self.fonte.render("[<<]", True, CORES['texto'])
            tela.blit(seta, (x_loja + largura_loja - 50, y_offset))
        
        y_offset += 80
        
        instrucoes = [
            "UP/DOWN: Navegar | TAB: Trocar aba",
            "ENTER: Comprar poço",
            "",
            "Após comprar, pressione P para posicionar",
            "o poço no local desejado",
            "",
            "L ou ESC: Fechar loja"
        ]
        
        y_offset += 10
        for instrucao in instrucoes:
            if instrucao == "":
                y_offset += 8
            else:
                texto = self.fonte.render(instrucao, True, CORES['cinza_info'])
                tela.blit(texto, (x_loja + 20, y_offset))
                y_offset += 18
