import pygame
from config import TIPOS_SEMENTE, CORES

class Shop:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.aberta = False
        self.item_selecionado = 0
        self.fonte_titulo = pygame.font.Font(None, 32)
        self.fonte = pygame.font.Font(None, 24)
    
    def toggle(self):
        self.aberta = not self.aberta
    
    def navegar(self, direcao):
        if direcao == 'cima':
            self.item_selecionado = (self.item_selecionado - 1) % 3
        elif direcao == 'baixo':
            self.item_selecionado = (self.item_selecionado + 1) % 3
    
    def comprar(self, player, quantidade=1):
        tipos_ordenados = list(TIPOS_SEMENTE.keys())
        tipo_selecionado = tipos_ordenados[self.item_selecionado]
        preco_total = TIPOS_SEMENTE[tipo_selecionado]['preco'] * quantidade
        
        if player.gastar_dinheiro(preco_total):
            player.adicionar_sementes(tipo_selecionado, quantidade)
            return True
        return False
    
    def desenhar(self, tela):
        largura_loja = 400
        altura_loja = 300
        x_loja = (self.largura - largura_loja) // 2
        y_loja = (self.altura - altura_loja) // 2
        
        pygame.draw.rect(tela, CORES['loja_fundo'], (x_loja, y_loja, largura_loja, altura_loja))
        pygame.draw.rect(tela, CORES['borda_interface'], (x_loja, y_loja, largura_loja, altura_loja), 3)
        
        titulo = self.fonte_titulo.render("🏪 LOJA DE SEMENTES", True, CORES['texto'])
        titulo_rect = titulo.get_rect(center=(self.largura // 2, y_loja + 30))
        tela.blit(titulo, titulo_rect)
        
        y_offset = y_loja + 90
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
        
        instrucoes_loja = [
            "↑↓: Navegar itens",
            "ENTER: Comprar 1 semente",
            "SHIFT+ENTER: Comprar 5 sementes",
            "L ou ESC: Fechar loja"
        ]
        
        y_offset += 20
        for instrucao in instrucoes_loja:
            texto = self.fonte.render(instrucao, True, CORES['cinza_info'])
            tela.blit(texto, (x_loja + 20, y_offset))
            y_offset += 18
