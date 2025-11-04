import pygame

pygame.init()

LARGURA, ALTURA = 1256, 768
TAMANHO_CELULA = 40
FPS = 60

# Posição do poço no mundo (coordenadas de grid)
# Jogador inicia próximo ao poço
POCO_POS = (0, 0)

TIPOS_SEMENTE = {
    'milho': {'cor': (255, 255, 0), 'preco': 10, 'valor_colheita': 25, 'tempo_crescimento': 5},
    'tomate': {'cor': (255, 0, 0), 'preco': 15, 'valor_colheita': 40, 'tempo_crescimento': 8},
    'alface': {'cor': (0, 255, 0), 'preco': 8, 'valor_colheita': 20, 'tempo_crescimento': 3}
}

CORES = {
    'fundo_interface': (50, 50, 50),
    'borda_interface': (255, 255, 255),
    'texto': (255, 255, 255),
    'modo_limpar': (255, 100, 100),
    'modo_agua': (0, 150, 255),
    'modo_adubar': (255, 200, 0),
    'modo_plantar': (0, 255, 100),
    'agua_indicador': (0, 200, 255),
    'grade': (100, 100, 100),
    'loja_fundo': (40, 40, 40),
    'loja_destaque': (80, 80, 80),
    'amarelo': (255, 255, 0),
    'verde_sucesso': (0, 255, 0),
    'vermelho_erro': (255, 0, 0),
    'cinza_info': (200, 200, 200)
}

def carregar_sprites():
    sprites = {
        'char': pygame.transform.scale(pygame.image.load("assets/char.png"), (40, 75)),
        'grama': pygame.image.load("assets/grama.png"),
        'terra': pygame.transform.scale(pygame.image.load("assets/terra.png"), (TAMANHO_CELULA, TAMANHO_CELULA)),
        'terra_aguada': pygame.transform.scale(pygame.image.load("assets/terra_aguada.png"), (TAMANHO_CELULA, TAMANHO_CELULA)),
        'poco': pygame.transform.scale(pygame.image.load("assets/poco.png"), (TAMANHO_CELULA * 2, TAMANHO_CELULA * 2)),
        'buraco': pygame.transform.scale(pygame.image.load("assets/buraco.png"), (TAMANHO_CELULA, TAMANHO_CELULA)),
        'agua': pygame.transform.scale(pygame.image.load("assets/agua.png"), (TAMANHO_CELULA, TAMANHO_CELULA)),
        'trabalhador': pygame.transform.scale(pygame.image.load("assets/char.png"), (30, 50))
    }
    
    sprites['plantas'] = {}
    for tipo in ['milho', 'tomate', 'alface']:
        sprites['plantas'][tipo] = {}
        for estagio in range(1, 8):
            caminho = f"assets/{tipo}/{tipo}_{estagio}.png"
            img = pygame.image.load(caminho)
            img = pygame.transform.scale(img, (TAMANHO_CELULA, TAMANHO_CELULA))
            sprites['plantas'][tipo][estagio] = img
    
    return sprites
