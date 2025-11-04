import pygame
from config import TIPOS_SEMENTE, CORES

class Shop:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.aberta = False
        self.item_selecionado = 0
        self.aba_atual = 'sementes'
        self.fonte_titulo = pygame.font.Font(None, 32)
        self.fonte = pygame.font.Font(None, 24)
    
    def toggle(self):
        self.aberta = not self.aberta
        if not self.aberta:
            self.item_selecionado = 0
            self.aba_atual = 'sementes'
    
    def trocar_aba(self):
        self.aba_atual = 'trabalhadores' if self.aba_atual == 'sementes' else 'sementes'
        self.item_selecionado = 0
    
    def navegar(self, direcao):
        max_itens = 3 if self.aba_atual == 'sementes' else 3
        if direcao == 'cima':
            self.item_selecionado = (self.item_selecionado - 1) % max_itens
        elif direcao == 'baixo':
            self.item_selecionado = (self.item_selecionado + 1) % max_itens
    
    def comprar_semente(self, player, quantidade=1):
        tipos_ordenados = list(TIPOS_SEMENTE.keys())
        tipo_selecionado = tipos_ordenados[self.item_selecionado]
        preco_total = TIPOS_SEMENTE[tipo_selecionado]['preco'] * quantidade
        
        if player.gastar_dinheiro(preco_total):
            player.adicionar_sementes(tipo_selecionado, quantidade)
            return True
        return False
    
    def contratar_trabalhador(self, player, worker_system, posicao_spawn):
        tipos_trabalhador = ['cultivador', 'coletador', 'adubador']
        tipo_selecionado = tipos_trabalhador[self.item_selecionado]
        
        return worker_system.contratar_trabalhador(tipo_selecionado, player, posicao_spawn)
    
    def desenhar(self, tela, worker_system=None):
        largura_loja = 450
        altura_loja = 400
        x_loja = (self.largura - largura_loja) // 2
        y_loja = (self.altura - altura_loja) // 2
        
        pygame.draw.rect(tela, CORES['loja_fundo'], (x_loja, y_loja, largura_loja, altura_loja))
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja, y_loja, largura_loja, altura_loja), 3)
        
        titulo_texto = "🏪 LOJA - " + ("SEMENTES" if self.aba_atual == 'sementes' else "TRABALHADORES")
        titulo = self.fonte_titulo.render(titulo_texto, True, CORES['texto'])
        titulo_rect = titulo.get_rect(center=(self.largura // 2, y_loja + 30))
        tela.blit(titulo, titulo_rect)
        
        self._desenhar_abas(tela, x_loja, y_loja, largura_loja)
        
        y_offset = y_loja + 110
        
        if self.aba_atual == 'sementes':
            self._desenhar_sementes(tela, x_loja, y_loja, y_offset, largura_loja)
        else:
            self._desenhar_trabalhadores(tela, x_loja, y_loja, y_offset, largura_loja, worker_system)
        
    def _desenhar_abas(self, tela, x_loja, y_loja, largura_loja):
        aba_largura = largura_loja // 2
        
        cor_aba_sementes = CORES['loja_destaque'] if self.aba_atual == 'sementes' else CORES['loja_fundo']
        cor_aba_trabalhadores = CORES['loja_destaque'] if self.aba_atual == 'trabalhadores' else CORES['loja_fundo']
        
        pygame.draw.rect(tela, cor_aba_sementes, (x_loja, y_loja + 60, aba_largura, 35))
        pygame.draw.rect(tela, cor_aba_trabalhadores, (x_loja + aba_largura, y_loja + 60, aba_largura, 35))
        
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja, y_loja + 60, aba_largura, 35), 2)
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja + aba_largura, y_loja + 60, aba_largura, 35), 2)
        
        texto_sementes = self.fonte.render("Sementes (TAB)", True, CORES['texto'])
        texto_trabalhadores = self.fonte.render("Trabalhadores (TAB)", True, CORES['texto'])
        
        tela.blit(texto_sementes, (x_loja + 10, y_loja + 70))
        tela.blit(texto_trabalhadores, (x_loja + aba_largura + 10, y_loja + 70))
    
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
                seta = self.fonte.render("◄", True, CORES['texto'])
                tela.blit(seta, (x_loja + largura_loja - 50, y_offset))
            
            y_offset += 35
        
        instrucoes = [
            "↑↓: Navegar | TAB: Trocar aba",
            "ENTER: Comprar 1 semente",
            "SHIFT+ENTER: Comprar 5 sementes",
            "L ou ESC: Fechar loja"
        ]
        
        y_offset += 20
        for instrucao in instrucoes:
            texto = self.fonte.render(instrucao, True, CORES['cinza_info'])
            tela.blit(texto, (x_loja + 20, y_offset))
            y_offset += 20
    
    def _desenhar_trabalhadores(self, tela, x_loja, y_loja, y_offset, largura_loja, worker_system):
        tipos_trabalhador = [
            ('cultivador', 'Cultivador - Planta sementes', (100, 255, 100)),
            ('coletador', 'Coletador - Colhe plantas', (255, 215, 0)),
            ('adubador', 'Adubador - Aduba terra', (139, 69, 19))
        ]
        
        contagem = worker_system.contar_trabalhadores_por_tipo() if worker_system else {}
        
        for i, (tipo, nome, cor) in enumerate(tipos_trabalhador):
            if i == self.item_selecionado:
                pygame.draw.rect(tela, CORES['loja_destaque'], (x_loja + 10, y_offset - 5, largura_loja - 20, 40))
            
            texto_item = self.fonte.render(f"{nome} - $300", True, cor)
            tela.blit(texto_item, (x_loja + 20, y_offset))
            
            ativos = contagem.get(tipo, 0)
            texto_ativos = self.fonte.render(f"Ativos: {ativos}", True, CORES['cinza_info'])
            tela.blit(texto_ativos, (x_loja + 20, y_offset + 20))
            
            if i == self.item_selecionado:
                seta = self.fonte.render("◄", True, CORES['texto'])
                tela.blit(seta, (x_loja + largura_loja - 50, y_offset))
            
            y_offset += 50
        
        instrucoes = [
            "↑↓: Navegar | TAB: Trocar aba",
            "ENTER: Contratar trabalhador",
            "Trabalhador fica ativo até não",
            "haver mais trabalho disponível",
            "L ou ESC: Fechar loja"
        ]
        
        y_offset += 20
        for instrucao in instrucoes:
            texto = self.fonte.render(instrucao, True, CORES['cinza_info'])
            tela.blit(texto, (x_loja + 20, y_offset))
            y_offset += 18
