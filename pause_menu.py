import pygame
from save_system import SaveSystem
from sound_system import SoundSystem


class PauseMenu:
    """Menu de pausa com opções de volume, save e exit"""
    
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.aberto = False
        self.sound_system = SoundSystem()
        
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte_opcao = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 24)
        
        self.cor_fundo = (0, 0, 0, 180)
        self.cor_texto = (255, 255, 255)
        self.cor_selecionada = (255, 255, 0)
        self.cor_slider_fundo = (100, 100, 100)
        self.cor_slider_barra = (50, 150, 255)
        
        self.opcoes = [
            {"texto": "Volume SFX", "tipo": "slider", "valor": 0.7},
            {"texto": "Volume Música", "tipo": "slider", "valor": 0.5},
            {"texto": "Salvar Jogo", "tipo": "botao"},
            {"texto": "Voltar ao Menu", "tipo": "botao"},
        ]
        
        self.opcao_selecionada = 0
        self.slider_selecionado = None
        self.atualizar_valores_sliders()
    
    def atualizar_valores_sliders(self):
        """Atualiza os valores dos sliders com base no sistema de som"""
        self.opcoes[0]["valor"] = self.sound_system.volume_sfx
        self.opcoes[1]["valor"] = self.sound_system.volume_musica
    
    def atualizar_dimensoes(self, largura, altura):
        """Atualiza as dimensões quando a janela é redimensionada"""
        self.largura = largura
        self.altura = altura
    
    def abrir(self):
        """Abre o menu de pausa"""
        self.aberto = True
        self.opcao_selecionada = 0
        self.slider_selecionado = None
        self.atualizar_valores_sliders()
    
    def fechar(self):
        """Fecha o menu de pausa"""
        self.aberto = False
    
    def navegar_cima(self):
        """Navega para cima no menu"""
        self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
        self.slider_selecionado = None
        self.sound_system.tocar_sfx('arrow')
    
    def navegar_baixo(self):
        """Navega para baixo no menu"""
        self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
        self.slider_selecionado = None
        self.sound_system.tocar_sfx('arrow')
    
    def navegar_esquerda(self):
        """Move o slider para a esquerda"""
        opcao_atual = self.opcoes[self.opcao_selecionada]
        if opcao_atual["tipo"] == "slider":
            opcao_atual["valor"] = max(0.0, opcao_atual["valor"] - 0.05)
            self._aplicar_volume()
            self.sound_system.tocar_sfx('arrow')
    
    def navegar_direita(self):
        """Move o slider para a direita"""
        opcao_atual = self.opcoes[self.opcao_selecionada]
        if opcao_atual["tipo"] == "slider":
            opcao_atual["valor"] = min(1.0, opcao_atual["valor"] + 0.05)
            self._aplicar_volume()
            self.sound_system.tocar_sfx('arrow')
    
    def _aplicar_volume(self):
        """Aplica os valores dos sliders ao sistema de som"""
        self.sound_system.set_volume_sfx(self.opcoes[0]["valor"])
        self.sound_system.set_volume_musica(self.opcoes[1]["valor"])
    
    def selecionar_opcao(self):
        """Seleciona a opção atual"""
        opcao_atual = self.opcoes[self.opcao_selecionada]
        
        if opcao_atual["tipo"] == "slider":
            return None
        elif opcao_atual["tipo"] == "botao":
            self.sound_system.tocar_sfx('select')
            if opcao_atual["texto"] == "Salvar Jogo":
                return "salvar"
            elif opcao_atual["texto"] == "Voltar ao Menu":
                return "menu"
        
        return None
    
    def desenhar(self, tela):
        """Desenha o menu de pausa"""
        if not self.aberto:
            return
        
        superficie_fundo = pygame.Surface((self.largura, self.altura))
        superficie_fundo.set_alpha(180)
        superficie_fundo.fill((0, 0, 0))
        tela.blit(superficie_fundo, (0, 0))
        
        largura_menu = 600
        altura_menu = 450
        x_menu = (self.largura - largura_menu) // 2
        y_menu = (self.altura - altura_menu) // 2
        
        pygame.draw.rect(tela, (50, 50, 50), (x_menu, y_menu, largura_menu, altura_menu))
        pygame.draw.rect(tela, (200, 200, 200), (x_menu, y_menu, largura_menu, altura_menu), 3)
        
        titulo = self.fonte_titulo.render("PAUSA", True, self.cor_texto)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, y_menu + 30))
        tela.blit(titulo, titulo_rect)
        
        y_offset = y_menu + 100
        for i, opcao in enumerate(self.opcoes):
            cor = self.cor_selecionada if i == self.opcao_selecionada else self.cor_texto
            
            if opcao["tipo"] == "slider":
                self._desenhar_slider(tela, opcao, i, x_menu, y_offset, largura_menu, cor)
            else:
                texto = self.fonte_opcao.render(opcao["texto"], True, cor)
                texto_rect = texto.get_rect(center=(self.largura // 2, y_offset))
                tela.blit(texto, texto_rect)
                
                if i == self.opcao_selecionada:
                    pygame.draw.rect(tela, cor, 
                                   (texto_rect.left - 20, texto_rect.top - 5,
                                    texto_rect.width + 40, texto_rect.height + 10), 2)
            
            y_offset += 80
        
        instrucoes = "↑↓: Navegar | ←→: Volume | ENTER: Selecionar | ESC: Continuar"
        texto_inst = self.fonte_pequena.render(instrucoes, True, (150, 150, 150))
        texto_inst_rect = texto_inst.get_rect(center=(self.largura // 2, self.altura - 40))
        tela.blit(texto_inst, texto_inst_rect)
    
    def _desenhar_slider(self, tela, opcao, indice, x_menu, y_offset, largura_menu, cor):
        """Desenha um slider para controle de volume"""
        label = self.fonte_opcao.render(opcao["texto"], True, cor)
        label_rect = label.get_rect(topleft=(x_menu + 50, y_offset))
        tela.blit(label, label_rect)
        
        slider_x = x_menu + 50
        slider_y = y_offset + 40
        slider_largura = largura_menu - 100
        slider_altura = 20
        
        pygame.draw.rect(tela, self.cor_slider_fundo, (slider_x, slider_y, slider_largura, slider_altura))
        pygame.draw.rect(tela, cor, (slider_x, slider_y, slider_largura, slider_altura), 2)
        
        valor_preenchido = int(slider_largura * opcao["valor"])
        pygame.draw.rect(tela, self.cor_slider_barra, (slider_x, slider_y, valor_preenchido, slider_altura))
        
        percentual = int(opcao["valor"] * 100)
        texto_valor = self.fonte_pequena.render(f"{percentual}%", True, cor)
        texto_valor_rect = texto_valor.get_rect(topleft=(slider_x + slider_largura + 20, slider_y + 2))
        tela.blit(texto_valor, texto_valor_rect)
