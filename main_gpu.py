"""
Mundo-da-Roca - Jogo de Simulação de Fazenda
Versão com suporte a GPU (OpenGL) e renderização híbrida
"""

import pygame
import sys
from menu import mostrar_menu
from save_system import SaveSystem
from config import LARGURA, ALTURA, FPS, carregar_sprites
from player import Player
from farm_system import FarmSystem
from water_system import WaterSystem
from worker_system import WorkerSystem
from shop import Shop
from ui import UI
from game_controller import GameController
from camera import Camera
from hybrid_renderer import check_opengl_support, RENDERER_TYPE

def inicializar_jogo():
    """Inicializar o jogo com renderizador híbrido"""
    escolha_menu = mostrar_menu()
    
    if escolha_menu == "sair":
        pygame.quit()
        sys.exit()
    
    pygame.init()
    
    # Exibir informações de renderização
    print(f"\n{'='*60}")
    print(f"Renderizador: {RENDERER_TYPE}")
    print(f"{'='*60}\n")
    
    # Tela redimensionável com suporte a tela cheia
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    pygame.display.set_caption("Fazenda Virtual - Mapa Infinito (F11: Tela Cheia) | Modo: " + RENDERER_TYPE)
    
    sprites = carregar_sprites()
    player = Player(x=100, y=100)  # Posição inicial próxima ao poço
    farm_system = FarmSystem()
    water_system = WaterSystem()
    worker_system = WorkerSystem()
    shop = Shop(LARGURA, ALTURA)
    ui = UI()
    controller = GameController(player, farm_system, water_system)
    camera = Camera(player)
    
    # Estado da tela cheia
    estado_tela = {'fullscreen': False, 'largura': LARGURA, 'altura': ALTURA}
    
    if escolha_menu == "continuar":
        carregar_jogo(player, farm_system, water_system, worker_system)
    
    return tela, sprites, player, farm_system, water_system, worker_system, shop, ui, controller, camera, estado_tela

def carregar_jogo(player, farm_system, water_system, worker_system):
    """Carregar jogo salvo"""
    dados_carregados = SaveSystem.load_game()
    if dados_carregados:
        player.carregar_dados(dados_carregados['dinheiro'], dados_carregados['sementes'])
        farm_system.carregar_dados(dados_carregados['fazenda'], dados_carregados.get('terra_adubada', []))
        water_system.carregar_dados(dados_carregados.get('buracos_com_agua', []), 
                                    dados_carregados.get('terra_aguada', []))
        worker_system.carregar_dados(dados_carregados.get('trabalhadores', []))
        print(f"✓ Jogo carregado! Data: {dados_carregados['data_save']}")
    else:
        print("ℹ Novo jogo iniciado")

def processar_eventos(controller, shop, player, ui, farm_system, water_system, worker_system, tela, estado_tela):
    """Processar eventos de input"""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            if SaveSystem.save_game(player, farm_system, water_system, worker_system):
                print("✓ Jogo salvo automaticamente!")
            return False, tela
        
        if evento.type == pygame.VIDEORESIZE:
            # Atualizar dimensões quando a janela é redimensionada
            estado_tela['largura'] = evento.w
            estado_tela['altura'] = evento.h
            shop.atualizar_dimensoes(evento.w, evento.h)
            print(f"ℹ Janela redimensionada para: {evento.w}x{evento.h}")
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_F11:
                # Alternar tela cheia
                estado_tela['fullscreen'] = not estado_tela['fullscreen']
                if estado_tela['fullscreen']:
                    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    estado_tela['largura'] = tela.get_width()
                    estado_tela['altura'] = tela.get_height()
                    print(f"✓ Tela cheia ativada: {estado_tela['largura']}x{estado_tela['altura']}")
                else:
                    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
                    estado_tela['largura'] = LARGURA
                    estado_tela['altura'] = ALTURA
                    print("✓ Modo janela ativado")
                shop.atualizar_dimensoes(estado_tela['largura'], estado_tela['altura'])
                return True, tela
            
            # Renderizador de debug (pressione 'G' para ver stats)
            elif evento.key == pygame.K_g:
                print(f"\n{'='*60}")
                print("INFORMAÇÕES DE GPU")
                print('='*60)
                print(f"Renderizador: {RENDERER_TYPE}")
                print(f"Resolução: {estado_tela['largura']}x{estado_tela['altura']}")
                try:
                    from hybrid_renderer import GPU_TYPE, GPU_NAME
                    print(f"GPU Vendor: {GPU_TYPE}")
                    print(f"GPU Name: {GPU_NAME}")
                    if 'NVIDIA' in GPU_NAME or 'AMD' in GPU_NAME or 'GeForce' in GPU_NAME or 'Radeon' in GPU_NAME:
                        print("✓ GPU Dedicada detectada")
                    elif 'Intel' in GPU_NAME and 'UHD' not in GPU_NAME and 'Iris' not in GPU_NAME:
                        print("✓ GPU Dedicada Intel detectada")
                    else:
                        print("⚠ GPU Integrada ou não identificada")
                except:
                    pass
                print('='*60 + "\n")
            
            elif evento.key == pygame.K_l or (evento.key == pygame.K_ESCAPE and shop.aberta):
                shop.toggle()
            
            elif shop.aberta:
                processar_eventos_loja(evento, shop, player, worker_system)
            
            elif not shop.aberta:
                processar_eventos_jogo(evento, controller, player, ui, farm_system, water_system, worker_system)
    
    return True, tela

def processar_eventos_loja(evento, shop, player, worker_system):
    """Processar eventos na loja"""
    if evento.key == pygame.K_UP:
        shop.navegar('cima')
    elif evento.key == pygame.K_DOWN:
        shop.navegar('baixo')
    elif evento.key == pygame.K_TAB:
        shop.trocar_aba()
    elif evento.key == pygame.K_RETURN or evento.key in [pygame.K_1, pygame.K_5, pygame.K_0]:
        if shop.aba_atual == 'sementes':
            # Determinar quantidade baseada na tecla pressionada
            if evento.key == pygame.K_1:
                quantidade = 1
            elif evento.key == pygame.K_5:
                quantidade = 5
            elif evento.key == pygame.K_0:
                quantidade = 10
            elif evento.key == pygame.K_RETURN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_SHIFT:
                    quantidade = 50
                elif mods & pygame.KMOD_ALT:
                    quantidade = 100
                else:
                    quantidade = 1
            
            if shop.comprar_semente(player, quantidade):
                print(f"✓ Comprou {quantidade} semente(s)!")
            else:
                print("✗ Dinheiro insuficiente!")
        else:
            posicao_spawn = (player.x, player.y)
            if shop.contratar_trabalhador(player, worker_system, posicao_spawn):
                print("✓ Trabalhador contratado!")
            else:
                print("✗ Dinheiro insuficiente!")

def processar_eventos_jogo(evento, controller, player, ui, farm_system, water_system, worker_system):
    """Processar eventos no jogo"""
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
        if SaveSystem.save_game(player, farm_system, water_system, worker_system):
            ui.mostrar_mensagem_save("✓ Jogo salvo com sucesso!")
            print("✓ Jogo salvo!")
        else:
            ui.mostrar_mensagem_save("✗ Erro ao salvar jogo!")
            print("✗ Erro ao salvar!")

def atualizar_jogo(controller, farm_system, water_system, worker_system, player, shop, sprites, camera, estado_tela):
    """Atualizar lógica do jogo"""
    if not shop.aberta:
        teclas = pygame.key.get_pressed()
        controller.processar_movimento(teclas, estado_tela['largura'], estado_tela['altura'])
        
        if teclas[pygame.K_SPACE]:
            controller.executar_acao()
    
    camera.atualizar(estado_tela['largura'], estado_tela['altura'])
    water_system.atualizar_terra_aguada()
    farm_system.atualizar_plantas(water_system)
    worker_system.atualizar_trabalhadores(farm_system, water_system, player)

def desenhar_jogo(tela, sprites, player, farm_system, water_system, worker_system, shop, ui, controller, camera, estado_tela):
    """Desenhar frame do jogo"""
    largura_atual = estado_tela['largura']
    altura_atual = estado_tela['altura']
    
    ui.desenhar_cenario(tela, sprites, water_system, farm_system, largura_atual, altura_atual, camera)
    
    ui.desenhar_trabalhadores(tela, worker_system, sprites, camera)
    
    if not shop.aberta:
        ui.desenhar_cursor(tela, player, camera)
    
    # Desenhar jogador no centro da tela
    tela_x = largura_atual // 2 - 20
    tela_y = altura_atual // 2 - 37
    tela.blit(sprites['char'], (tela_x, tela_y))
    
    ui.desenhar_interface(tela, player, water_system, controller.get_modo_atual())
    
    if shop.aberta:
        shop.desenhar(tela, worker_system)
    
    pygame.display.update()

def main():
    """Função principal"""
    # Verificar suporte a OpenGL
    print("\n" + "="*60)
    print("MUNDO-DA-ROCA - Sistema de Renderização com GPU")
    print("="*60)
    check_opengl_support()
    print("\nDica: Pressione 'G' durante o jogo para ver informações")
    print("Pressione 'F11' para alternar tela cheia")
    print("="*60 + "\n")
    
    tela, sprites, player, farm_system, water_system, worker_system, shop, ui, controller, camera, estado_tela = inicializar_jogo()
    relogio = pygame.time.Clock()
    rodando = True
    
    try:
        while rodando:
            rodando, tela = processar_eventos(controller, shop, player, ui, farm_system, water_system, worker_system, tela, estado_tela)
            atualizar_jogo(controller, farm_system, water_system, worker_system, player, shop, sprites, camera, estado_tela)
            desenhar_jogo(tela, sprites, player, farm_system, water_system, worker_system, shop, ui, controller, camera, estado_tela)
            relogio.tick(FPS)
    
    except KeyboardInterrupt:
        print("\n✓ Jogo interrompido pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
