import pygame
import sys
from save_system import SaveSystem

class Menu:
    
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Fazenda Virtual - Menu")
        
        self.fonte_titulo = pygame.font.Font(None, 72)
        self.fonte_opcao = pygame.font.Font(None, 40)
        self.fonte_info = pygame.font.Font(None, 24)
        
        self.cor_fundo = (34, 139, 34)
        self.cor_titulo = (255, 255, 255)
        self.cor_opcao = (255, 255, 255)
        self.cor_opcao_selecionada = (255, 255, 0)
        self.cor_info = (200, 200, 200)
        self.cor_destaque = (255, 215, 0)
        
        self.opcoes = []
        self.opcao_selecionada = 0
        
        self.save_existe = SaveSystem.save_exists()
        self._configurar_opcoes()
        
        self.save_info = SaveSystem.get_save_info() if self.save_existe else None
    
    def _configurar_opcoes(self):
        if self.save_existe:
            self.opcoes = [
                {"texto": "Continuar Jogo", "acao": "continuar"},
                {"texto": "Novo Jogo", "acao": "novo"},
                {"texto": "Deletar Save", "acao": "deletar"},
                {"texto": "Sair", "acao": "sair"}
            ]
        else:
            self.opcoes = [
                {"texto": "Novo Jogo", "acao": "novo"},
                {"texto": "Sair", "acao": "sair"}
            ]
    
    def desenhar(self):
        self.tela.fill(self.cor_fundo)
        
        titulo = self.fonte_titulo.render("FAZENDA VIRTUAL", True, self.cor_titulo)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 100))
        self.tela.blit(titulo, titulo_rect)
        
        subtitulo = self.fonte_info.render("Simulador Agrícola 2D", True, self.cor_info)
        subtitulo_rect = subtitulo.get_rect(center=(self.largura // 2, 150))
        self.tela.blit(subtitulo, subtitulo_rect)
        
        if self.save_info:
            y_info = 200
            info_texts = [
                f"Ultimo Save: {self.save_info['data_save']}",
                f"Dinheiro: ${self.save_info['dinheiro']}",
                f"Plantas na fazenda: {self.save_info['total_plantas']}"
            ]
            
            for texto in info_texts:
                info_surface = self.fonte_info.render(texto, True, self.cor_destaque)
                info_rect = info_surface.get_rect(center=(self.largura // 2, y_info))
                self.tela.blit(info_surface, info_rect)
                y_info += 25
        
        y_offset = 320 if self.save_info else 250
        
        for i, opcao in enumerate(self.opcoes):
            cor = self.cor_opcao_selecionada if i == self.opcao_selecionada else self.cor_opcao
            texto_surface = self.fonte_opcao.render(opcao["texto"], True, cor)
            texto_rect = texto_surface.get_rect(center=(self.largura // 2, y_offset))
            
            if i == self.opcao_selecionada:
                padding = 20
                rect_destaque = pygame.Rect(
                    texto_rect.left - padding,
                    texto_rect.top - 5,
                    texto_rect.width + padding * 2,
                    texto_rect.height + 10
                )
                pygame.draw.rect(self.tela, self.cor_opcao_selecionada, rect_destaque, 3)
            
            self.tela.blit(texto_surface, texto_rect)
            y_offset += 60
        
        instrucoes = [
            "Use as setas para navegar",
            "Pressione ENTER para selecionar"
        ]
        y_instrucao = self.altura - 80
        for instrucao in instrucoes:
            texto = self.fonte_info.render(instrucao, True, self.cor_info)
            texto_rect = texto.get_rect(center=(self.largura // 2, y_instrucao))
            self.tela.blit(texto, texto_rect)
            y_instrucao += 25
        
        pygame.display.update()
    
    def navegar_cima(self):
        self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
    
    def navegar_baixo(self):
        self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
    
    def selecionar_opcao(self):
        return self.opcoes[self.opcao_selecionada]["acao"]
    
    def confirmar_delecao(self):
        confirmando = True
        opcao_confirmacao = 0
        
        while confirmando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                        opcao_confirmacao = 1 - opcao_confirmacao
                    elif evento.key == pygame.K_RETURN:
                        return opcao_confirmacao == 1
                    elif evento.key == pygame.K_ESCAPE:
                        return False
            
            self.tela.fill(self.cor_fundo)
            
            titulo = self.fonte_opcao.render("Deletar Save?", True, self.cor_titulo)
            titulo_rect = titulo.get_rect(center=(self.largura // 2, 200))
            self.tela.blit(titulo, titulo_rect)
            
            aviso = self.fonte_info.render("Esta ação não pode ser desfeita!", True, (255, 100, 100))
            aviso_rect = aviso.get_rect(center=(self.largura // 2, 250))
            self.tela.blit(aviso, aviso_rect)
            
            opcoes_conf = ["NÃO", "SIM"]
            y_offset = 320
            for i, opcao in enumerate(opcoes_conf):
                cor = self.cor_opcao_selecionada if i == opcao_confirmacao else self.cor_opcao
                texto = self.fonte_opcao.render(opcao, True, cor)
                texto_rect = texto.get_rect(center=(self.largura // 2 - 100 + i * 200, y_offset))
                
                if i == opcao_confirmacao:
                    pygame.draw.rect(self.tela, cor, 
                                   (texto_rect.left - 20, texto_rect.top - 5, 
                                    texto_rect.width + 40, texto_rect.height + 10), 3)
                
                self.tela.blit(texto, texto_rect)
            
            instrucao = self.fonte_info.render("Setas: Navegar | ENTER: Confirmar | ESC: Cancelar", 
                                              True, self.cor_info)
            instrucao_rect = instrucao.get_rect(center=(self.largura // 2, self.altura - 50))
            self.tela.blit(instrucao, instrucao_rect)
            
            pygame.display.update()
        
        return False
    
    def executar(self):
        relogio = pygame.time.Clock()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.navegar_cima()
                    elif evento.key == pygame.K_DOWN:
                        self.navegar_baixo()
                    elif evento.key == pygame.K_RETURN:
                        acao = self.selecionar_opcao()
                        
                        if acao == "deletar":
                            if self.confirmar_delecao():
                                SaveSystem.delete_save()
                                self.save_existe = False
                                self.save_info = None
                                self._configurar_opcoes()
                                self.opcao_selecionada = 0
                        else:
                            return acao
                    elif evento.key == pygame.K_ESCAPE:
                        return "sair"
            
            self.desenhar()
            relogio.tick(60)


def mostrar_menu():
    pygame.init()
    menu = Menu(1256, 768)
    escolha = menu.executar()
    return escolha
