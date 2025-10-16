import pygame
import sys
import time
from menu import mostrar_menu
from save_system import SaveSystem

escolha_menu = mostrar_menu()

if escolha_menu == "sair":
    pygame.quit()
    sys.exit()

pygame.init()

fonte = pygame.font.Font(None, 24)
fonte_titulo = pygame.font.Font(None, 32)

LARGURA, ALTURA = 1256, 768
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fazenda Virtual")

char_img = pygame.image.load("char.png")
char_img = pygame.transform.scale(char_img, (40, 75))

grama_img = pygame.image.load("grama.png")

x, y = 100, 100
velocidade = 5

TIPOS_SEMENTE = {
    'milho': {'cor': (255, 255, 0), 'preco': 10, 'valor_colheita': 25, 'tempo_crescimento': 5},
    'tomate': {'cor': (255, 0, 0), 'preco': 15, 'valor_colheita': 40, 'tempo_crescimento': 8},
    'alface': {'cor': (0, 255, 0), 'preco': 8, 'valor_colheita': 20, 'tempo_crescimento': 3}
}

TAMANHO_CELULA = 40

terra_img = pygame.image.load("terra.png")
terra_img = pygame.transform.scale(terra_img, (TAMANHO_CELULA, TAMANHO_CELULA))

terra_adubada = set()

if escolha_menu == "continuar":
    dados_carregados = SaveSystem.load_game()
    if dados_carregados:
        dinheiro = dados_carregados['dinheiro']
        sementes = dados_carregados['sementes']
        fazenda = dados_carregados['fazenda']
        terra_adubada = set(tuple(pos) for pos in dados_carregados.get('terra_adubada', []))
        print(f"Jogo carregado! Data: {dados_carregados['data_save']}")
    else:
        print("Erro ao carregar jogo, iniciando novo jogo...")
        dinheiro = 100
        sementes = {'milho': 5, 'tomate': 3, 'alface': 2}
        fazenda = {}
else:
    dinheiro = 100
    sementes = {'milho': 5, 'tomate': 3, 'alface': 2}
    fazenda = {}

semente_selecionada = 'milho'
loja_aberta = False
item_selecionado_loja = 0
espaco_pressionado = False
modo_adubar = False

def desenhar_planta(superficie, x, y, tipo_semente, estagio):
    cor = TIPOS_SEMENTE[tipo_semente]['cor']
    tamanho = min(estagio * 4, 30)
    
    if estagio == 7:
        cor = (139, 69, 19)
    elif estagio >= 6:
        tamanho = 30
    
    pygame.draw.circle(superficie, cor, (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2), tamanho // 2)
    
    if estagio > 1:
        pygame.draw.line(superficie, (0, 100, 0), 
                        (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2), 
                        (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA - 5), 3)

def atualizar_plantas():
    tempo_atual = time.time()
    plantas_para_remover = []
    
    for posicao, planta in fazenda.items():
        tempo_decorrido = tempo_atual - planta['tempo_plantio']
        tipo = planta['tipo']
        tempo_crescimento = TIPOS_SEMENTE[tipo]['tempo_crescimento']
        
        novo_estagio = min(int(tempo_decorrido / tempo_crescimento) + 1, 7)
        planta['estagio'] = novo_estagio
        
        if novo_estagio == 7 and tempo_decorrido > tempo_crescimento * 10:
            plantas_para_remover.append(posicao)
    
    for posicao in plantas_para_remover:
        del fazenda[posicao]

def adubar_terra(grid_x, grid_y):
    """Aduba uma célula de terra"""
    posicao = (grid_x, grid_y)
    if posicao not in fazenda and posicao not in terra_adubada:
        terra_adubada.add(posicao)
        return True
    return False

def plantar_semente(grid_x, grid_y, tipo):
    """Planta uma semente (requer terra adubada)"""
    global dinheiro
    
    posicao = (grid_x, grid_y)
    if posicao not in fazenda and sementes[tipo] > 0 and posicao in terra_adubada:
        fazenda[posicao] = {
            'tipo': tipo,
            'estagio': 1,
            'tempo_plantio': time.time()
        }
        sementes[tipo] -= 1
        return True
    return False

def colher_planta(grid_x, grid_y):
    """Colhe uma planta madura e remove a terra adubada"""
    global dinheiro
    
    posicao = (grid_x, grid_y)
    if posicao in fazenda:
        planta = fazenda[posicao]
        if planta['estagio'] == 6:
            valor = TIPOS_SEMENTE[planta['tipo']]['valor_colheita']
            dinheiro += valor
            del fazenda[posicao]
            if posicao in terra_adubada:
                terra_adubada.discard(posicao)
            return True
    return False

def desenhar_interface():
    pygame.draw.rect(tela, (50, 50, 50), (10, 10, 300, 150))
    pygame.draw.rect(tela, (255, 255, 255), (10, 10, 300, 150), 2)
    
    texto_dinheiro = fonte.render(f"Dinheiro: ${dinheiro}", True, (255, 255, 255))
    tela.blit(texto_dinheiro, (20, 25))
    
    y_offset = 50
    for tipo, quantidade in sementes.items():
        cor = TIPOS_SEMENTE[tipo]['cor']
        texto = f"{tipo.capitalize()}: {quantidade}"
        if tipo == semente_selecionada:
            texto += " ◄"
        texto_semente = fonte.render(texto, True, cor)
        tela.blit(texto_semente, (20, y_offset))
        y_offset += 25
    
    modo_texto = "MODO: ADUBAR" if modo_adubar else "MODO: PLANTAR"
    cor_modo = (255, 200, 0) if modo_adubar else (0, 255, 100)
    texto_modo = fonte_titulo.render(modo_texto, True, cor_modo)
    tela.blit(texto_modo, (20, 130))
    
    instrucoes = [
        "A: Alternar Modo Adubar/Plantar",
        "ESPAÇO: Ação (adubar ou plantar/colher)",
        "Segurar ESPAÇO: Ação contínua",
        "1,2,3: Selecionar semente",
        "L: Abrir/Fechar Loja",
        "S: Salvar jogo",
    ]
    
    y_offset = 360
    for instrucao in instrucoes:
        texto = fonte.render(instrucao, True, (255, 255, 255))
        tela.blit(texto, (20, y_offset))
        y_offset += 20
    
    global tempo_mensagem
    if mensagem_save and (time.time() - tempo_mensagem < 3):
        cor_mensagem = (0, 255, 0) if "sucesso" in mensagem_save else (255, 0, 0)
        texto_save = fonte.render(mensagem_save, True, cor_mensagem)
        tela.blit(texto_save, (LARGURA // 2 - texto_save.get_width() // 2, 30))

def desenhar_loja():
    largura_loja = 400
    altura_loja = 300
    x_loja = (LARGURA - largura_loja) // 2
    y_loja = (ALTURA - altura_loja) // 2
    
    pygame.draw.rect(tela, (40, 40, 40), (x_loja, y_loja, largura_loja, altura_loja))
    pygame.draw.rect(tela, (255, 255, 255), (x_loja, y_loja, largura_loja, altura_loja), 3)
    
    titulo = fonte_titulo.render("🏪 LOJA DE SEMENTES", True, (255, 255, 255))
    titulo_rect = titulo.get_rect(center=(LARGURA // 2, y_loja + 30))
    tela.blit(titulo, titulo_rect)
    
    texto_dinheiro = fonte.render(f"Dinheiro disponível: ${dinheiro}", True, (255, 255, 0))
    tela.blit(texto_dinheiro, (x_loja + 20, y_loja + 60))
    
    y_offset = y_loja + 90
    tipos_ordenados = list(TIPOS_SEMENTE.keys())
    
    for i, tipo in enumerate(tipos_ordenados):
        info = TIPOS_SEMENTE[tipo]
        cor = info['cor']
        preco = info['preco']
        
        if i == item_selecionado_loja:
            pygame.draw.rect(tela, (80, 80, 80), (x_loja + 10, y_offset - 5, largura_loja - 20, 30))
        
        texto_item = fonte.render(f"{tipo.capitalize()}: ${preco} cada", True, cor)
        tela.blit(texto_item, (x_loja + 20, y_offset))
        
        if i == item_selecionado_loja:
            seta = fonte.render("◄", True, (255, 255, 255))
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
        texto = fonte.render(instrucao, True, (200, 200, 200))
        tela.blit(texto, (x_loja + 20, y_offset))
        y_offset += 18

def tentar_acao_na_posicao(pos_x, pos_y):
    """Executa ação baseada no modo atual"""
    grid_x = pos_x // TAMANHO_CELULA
    grid_y = pos_y // TAMANHO_CELULA
    
    if modo_adubar:
        adubar_terra(grid_x, grid_y)
    else:
        if not colher_planta(grid_x, grid_y):
            plantar_semente(grid_x, grid_y, semente_selecionada)

def comprar_semente(tipo, quantidade=1):
    global dinheiro
    
    preco_total = TIPOS_SEMENTE[tipo]['preco'] * quantidade
    
    if dinheiro >= preco_total:
        dinheiro -= preco_total
        sementes[tipo] += quantidade
        return True
    return False

rodando = True
relogio = pygame.time.Clock()
mensagem_save = ""
tempo_mensagem = 0

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            if SaveSystem.save_game(dinheiro, sementes, fazenda, terra_adubada):
                print("Jogo salvo automaticamente!")
            rodando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_l or (evento.key == pygame.K_ESCAPE and loja_aberta):
                loja_aberta = not loja_aberta
            
            elif loja_aberta:
                if evento.key == pygame.K_UP:
                    item_selecionado_loja = (item_selecionado_loja - 1) % 3
                elif evento.key == pygame.K_DOWN:
                    item_selecionado_loja = (item_selecionado_loja + 1) % 3
                elif evento.key == pygame.K_RETURN:
                    tipos_ordenados = list(TIPOS_SEMENTE.keys())
                    tipo_selecionado = tipos_ordenados[item_selecionado_loja]
                    
                    mods = pygame.key.get_mods()
                    quantidade = 5 if mods & pygame.KMOD_SHIFT else 1
                    
                    if comprar_semente(tipo_selecionado, quantidade):
                        print(f"Comprou {quantidade} semente(s) de {tipo_selecionado}!")
                    else:
                        print("Dinheiro insuficiente!")
            
            elif not loja_aberta:
                if evento.key == pygame.K_a:
                    modo_adubar = not modo_adubar
                    print(f"Modo: {'ADUBAR' if modo_adubar else 'PLANTAR'}")
                
                elif evento.key == pygame.K_1:
                    semente_selecionada = 'milho'
                elif evento.key == pygame.K_2:
                    semente_selecionada = 'tomate'
                elif evento.key == pygame.K_3:
                    semente_selecionada = 'alface'
                
                elif evento.key == pygame.K_SPACE:
                    tentar_acao_na_posicao(x + 20, y + 37)
                
                elif evento.key == pygame.K_s:
                    if SaveSystem.save_game(dinheiro, sementes, fazenda, terra_adubada):
                        mensagem_save = "Jogo salvo com sucesso!"
                        tempo_mensagem = time.time()
                        print("Jogo salvo!")
                    else:
                        mensagem_save = "Erro ao salvar jogo!"
                        tempo_mensagem = time.time()
                        print("Erro ao salvar!")

    if not loja_aberta:
        teclas = pygame.key.get_pressed()
        
        espaco_pressionado = teclas[pygame.K_SPACE]
        
        if teclas[pygame.K_LEFT] and x > 0:
            x -= velocidade
        if teclas[pygame.K_RIGHT] and x < LARGURA - 40:
            x += velocidade
        if teclas[pygame.K_UP] and y > 0:
            y -= velocidade
        if teclas[pygame.K_DOWN] and y < ALTURA - 75:
            y += velocidade
        
        if espaco_pressionado:
            tentar_acao_na_posicao(x + 20, y + 37)

    atualizar_plantas()

    for i in range(0, LARGURA, grama_img.get_width()):
        for j in range(0, ALTURA, grama_img.get_height()):
            tela.blit(grama_img, (i, j))
    
    for i in range(0, LARGURA, TAMANHO_CELULA):
        pygame.draw.line(tela, (100, 100, 100), (i, 0), (i, ALTURA), 1)
    for j in range(0, ALTURA, TAMANHO_CELULA):
        pygame.draw.line(tela, (100, 100, 100), (0, j), (LARGURA, j), 1)
    
    for (grid_x, grid_y) in terra_adubada:
        x_pos = grid_x * TAMANHO_CELULA
        y_pos = grid_y * TAMANHO_CELULA
        tela.blit(terra_img, (x_pos, y_pos))
    
    for (grid_x, grid_y), planta in fazenda.items():
        x_pos = grid_x * TAMANHO_CELULA
        y_pos = grid_y * TAMANHO_CELULA
        desenhar_planta(tela, x_pos, y_pos, planta['tipo'], planta['estagio'])
    
    if not loja_aberta:
        grid_x = (x + 20) // TAMANHO_CELULA * TAMANHO_CELULA
        grid_y = (y + 37) // TAMANHO_CELULA * TAMANHO_CELULA
        pygame.draw.rect(tela, (255, 255, 255), (grid_x, grid_y, TAMANHO_CELULA, TAMANHO_CELULA), 2)
    
    tela.blit(char_img, (x, y))
    
    desenhar_interface()
    
    if loja_aberta:
        desenhar_loja()
    
    pygame.display.update()
    relogio.tick(60)

pygame.quit()
sys.exit()
