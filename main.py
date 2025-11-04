import pygame
import sys
from menu import mostrar_menu
from save_system import SaveSystem
from config import LARGURA, ALTURA, FPS, carregar_sprites
from player import Player
from farm_system import FarmSystem
from water_system import WaterSystem
from shop import Shop
from ui import UI
from game_controller import GameController

def inicializar_jogo():
    escolha_menu = mostrar_menu()
    
    if escolha_menu == "sair":
        pygame.quit()
        sys.exit()
    
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Fazenda Virtual")
    
    sprites = carregar_sprites()
    player = Player()
    farm_system = FarmSystem()
    water_system = WaterSystem()
    shop = Shop(LARGURA, ALTURA)
    ui = UI()
    controller = GameController(player, farm_system, water_system)
    
    if escolha_menu == "continuar":
        carregar_jogo(player, farm_system, water_system)
    
    return tela, sprites, player, farm_system, water_system, shop, ui, controller

def carregar_jogo(player, farm_system, water_system):
    dados_carregados = SaveSystem.load_game()
    if dados_carregados:
        player.carregar_dados(dados_carregados['dinheiro'], dados_carregados['sementes'])
        farm_system.carregar_dados(dados_carregados['fazenda'], dados_carregados.get('terra_adubada', []))
        water_system.carregar_dados(dados_carregados.get('buracos_com_agua', []), 
                                    dados_carregados.get('terra_aguada', []))
        print(f"Jogo carregado! Data: {dados_carregados['data_save']}")
    else:
        print("Erro ao carregar jogo, iniciando novo jogo...")

def processar_eventos(controller, shop, player, ui, farm_system, water_system):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            if SaveSystem.save_game(player, farm_system, water_system):
                print("Jogo salvo automaticamente!")
            return False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_l or (evento.key == pygame.K_ESCAPE and shop.aberta):
                shop.toggle()
            
            elif shop.aberta:
                processar_eventos_loja(evento, shop, player)
            
            elif not shop.aberta:
                processar_eventos_jogo(evento, controller, player, ui, farm_system, water_system)
    
    return True

def processar_eventos_loja(evento, shop, player):
    if evento.key == pygame.K_UP:
        shop.navegar('cima')
    elif evento.key == pygame.K_DOWN:
        shop.navegar('baixo')
    elif evento.key == pygame.K_RETURN:
        mods = pygame.key.get_mods()
        quantidade = 5 if mods & pygame.KMOD_SHIFT else 1
        if shop.comprar(player, quantidade):
            print(f"Comprou {quantidade} semente(s)!")
        else:
            print("Dinheiro insuficiente!")

def processar_eventos_jogo(evento, controller, player, ui, farm_system, water_system):
    if evento.key == pygame.K_a:
        modo = controller.alternar_modo('adubar')
        print(f"Modo: {modo}")
    elif evento.key == pygame.K_w:
        modo = controller.alternar_modo('agua')
        print(f"Modo: {modo}")
    elif evento.key == pygame.K_r:
        modo = controller.alternar_modo('limpar')
        print(f"Modo: {modo}")
    elif evento.key == pygame.K_1:
        player.selecionar_semente(0)
    elif evento.key == pygame.K_2:
        player.selecionar_semente(1)
    elif evento.key == pygame.K_3:
        player.selecionar_semente(2)
    elif evento.key == pygame.K_SPACE:
        controller.executar_acao()
    elif evento.key == pygame.K_s:
        if SaveSystem.save_game(player, farm_system, water_system):
            ui.mostrar_mensagem_save("Jogo salvo com sucesso!")
            print("Jogo salvo!")
        else:
            ui.mostrar_mensagem_save("Erro ao salvar jogo!")
            print("Erro ao salvar!")

def atualizar_jogo(controller, farm_system, water_system, shop, sprites):
    if not shop.aberta:
        teclas = pygame.key.get_pressed()
        controller.processar_movimento(teclas, LARGURA, ALTURA)
        
        if teclas[pygame.K_SPACE]:
            controller.executar_acao()
    
    water_system.atualizar_terra_aguada()
    farm_system.atualizar_plantas(water_system)

def desenhar_jogo(tela, sprites, player, farm_system, water_system, shop, ui, controller):
    ui.desenhar_cenario(tela, sprites, water_system, farm_system, LARGURA, ALTURA)
    
    if not shop.aberta:
        ui.desenhar_cursor(tela, player)
    
    tela.blit(sprites['char'], (player.x, player.y))
    ui.desenhar_interface(tela, player, water_system, controller.get_modo_atual())
    
    if shop.aberta:
        shop.desenhar(tela)
    
    pygame.display.update()

def main():
    tela, sprites, player, farm_system, water_system, shop, ui, controller = inicializar_jogo()
    relogio = pygame.time.Clock()
    rodando = True
    
    while rodando:
        rodando = processar_eventos(controller, shop, player, ui, farm_system, water_system)
        atualizar_jogo(controller, farm_system, water_system, shop, sprites)
        desenhar_jogo(tela, sprites, player, farm_system, water_system, shop, ui, controller)
        relogio.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
