import pygame
import os


class SoundSystem:
    """Sistema centralizado de sons para o jogo"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundSystem, cls).__new__(cls)
            cls._instance._inicializado = False
        return cls._instance
    
    def __init__(self):
        if self._inicializado:
            return
        
        pygame.mixer.init()
        self._inicializado = True
        
        self.sfx = {}
        self.musicas = {}
        self.musica_atual = None
        self.volume_sfx = 0.7
        self.volume_musica = 0.5
        
        self._carregar_sons()
    
    def _carregar_sons(self):
        """Carrega todos os sons do jogo"""
        caminho_sons = "assets/sounds"
        
        sfx_files = {
            'arrow': 'arrow.mp3',
            'select': 'select.mp3',
            'select_erro': 'select_erro.mp3',
        }
        
        musica_files = {
            'game': 'game_musica.mp3',
            'menu': 'menu_musica.mp3',
        }
        
        for nome, arquivo in sfx_files.items():
            caminho_completo = os.path.join(caminho_sons, arquivo)
            try:
                self.sfx[nome] = pygame.mixer.Sound(caminho_completo)
                self.sfx[nome].set_volume(self.volume_sfx)
                print(f"SFX carregado: {nome}")
            except Exception as e:
                print(f"Erro ao carregar SFX '{nome}': {e}")
        
        for nome, arquivo in musica_files.items():
            caminho_completo = os.path.join(caminho_sons, arquivo)
            if os.path.exists(caminho_completo):
                try:
                    self.musicas[nome] = caminho_completo
                    print(f"Música carregada: {nome}")
                except Exception as e:
                    print(f"Erro ao carregar música '{nome}': {e}")
    
    def tocar_sfx(self, nome):
        """Toca um efeito sonoro"""
        if nome in self.sfx:
            try:
                self.sfx[nome].play()
            except Exception as e:
                print(f"Erro ao tocar SFX '{nome}': {e}")
        else:
            print(f"SFX '{nome}' não encontrado")
    
    def tocar_musica(self, nome, loops=-1):
        """
        Toca uma música em loop
        loops=-1 significa loop infinito
        """
        if nome in self.musicas:
            try:
                if self.musica_atual == nome and pygame.mixer.music.get_busy():
                    return
                
                pygame.mixer.music.stop()
                
                pygame.mixer.music.load(self.musicas[nome])
                pygame.mixer.music.set_volume(self.volume_musica)
                pygame.mixer.music.play(loops)
                self.musica_atual = nome
                print(f"Tocando música: {nome}")
            except Exception as e:
                print(f"Erro ao tocar música '{nome}': {e}")
        else:
            print(f"Música '{nome}' não encontrada")
    
    def parar_musica(self):
        """Para a música que está tocando"""
        try:
            pygame.mixer.music.stop()
            self.musica_atual = None
        except Exception as e:
            print(f"Erro ao parar música: {e}")
    
    def set_volume_sfx(self, volume):
        """Define o volume dos efeitos sonoros (0.0 a 1.0)"""
        self.volume_sfx = max(0.0, min(1.0, volume))
        for sfx in self.sfx.values():
            sfx.set_volume(self.volume_sfx)
    
    def set_volume_musica(self, volume):
        """Define o volume da música (0.0 a 1.0)"""
        self.volume_musica = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume_musica)
