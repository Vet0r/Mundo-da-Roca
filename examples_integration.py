"""
Exemplos de integração do renderizador híbrido com o jogo
Use estes exemplos como referência para expandir funcionalidades
"""

# ============================================================
# EXEMPLO 1: Uso Básico do Renderizador Híbrido
# ============================================================

def exemplo_basico():
    """Exemplo mais simples possível"""
    from hybrid_renderer import HybridRenderer, RENDERER_TYPE
    
    # Criar renderizador
    renderer = HybridRenderer(1256, 768, "Meu Jogo")
    
    # Ver qual renderizador está sendo usado
    print(f"Usando: {RENDERER_TYPE}")
    
    # Carregar sprite
    renderer.load_sprite("player", "assests/char.png", 40, 75)
    
    # Loop de renderização
    running = True
    while running:
        renderer.clear_screen((30, 30, 30))
        renderer.draw_sprite("player", 100, 100)
        renderer.flip_display()
        renderer.set_fps(60)


# ============================================================
# EXEMPLO 2: Integração com GameLoop Existente
# ============================================================

def exemplo_integracao_main():
    """Como integrar com o main.py existente"""
    
    # Importar na parte superior do main.py:
    # from hybrid_renderer import check_opengl_support, RENDERER_TYPE
    
    # No inicializar_jogo():
    check_opengl_support()  # Detecta GPU automaticamente
    print(f"Renderizador: {RENDERER_TYPE}")
    
    # O resto do código funciona normalmente!
    # Não precisa mudar nada


# ============================================================
# EXEMPLO 3: Renderizador com Cache de Sprites
# ============================================================

def exemplo_cache_sprites():
    """Demonstra cache inteligente de sprites"""
    from hybrid_renderer import HybridRenderer
    
    renderer = HybridRenderer(1280, 720)
    
    # Carregar sprites (vai ao disco uma vez)
    sprites = [
        ("char", "assests/char.png", 40, 75),
        ("agua", "assests/agua.png", 40, 40),
        ("planta", "assests/milho/milho_1.png", 40, 40),
    ]
    
    for name, path, w, h in sprites:
        renderer.load_sprite(name, path, w, h)
    
    # Usar sprites múltiplas vezes (rápido - vem do cache)
    for i in range(100):
        renderer.draw_sprite("char", i * 10, 100)
        renderer.draw_sprite("agua", i * 10, 150)


# ============================================================
# EXEMPLO 4: Teste de Performance GPU vs CPU
# ============================================================

def exemplo_benchmark():
    """Comparar performance GPU vs CPU"""
    import time
    import pygame
    from hybrid_renderer import HybridRenderer, RENDERER_TYPE
    
    renderer = HybridRenderer(800, 600)
    renderer.load_sprite("test", "assests/grama.png", 40, 40)
    
    print(f"\nBenchmark usando: {RENDERER_TYPE}")
    print("Renderizando 1000 sprites...")
    
    start = time.time()
    
    for frame in range(100):
        renderer.clear_screen()
        
        # Desenhar muitos sprites
        for x in range(20):
            for y in range(25):
                renderer.draw_sprite("test", x * 40, y * 24)
        
        renderer.flip_display()
    
    elapsed = time.time() - start
    fps = 100 / elapsed
    
    print(f"Tempo: {elapsed:.2f}s")
    print(f"FPS Médio: {fps:.1f}")
    print(f"Sprites/frame: 500")
    print(f"Total: 50,000 renders")


# ============================================================
# EXEMPLO 5: Renderizador com Configurações
# ============================================================

def exemplo_config():
    """Usar arquivo de configuração de GPU"""
    from hybrid_renderer import HybridRenderer
    from gpu_config import apply_preset, print_config
    
    # Aplicar preset de performance
    apply_preset('performance')
    
    # Ver configuração atual
    print_config()
    
    # Criar renderizador com essas configs
    renderer = HybridRenderer(1280, 720)


# ============================================================
# EXEMPLO 6: Renderização Condicional GPU/CPU
# ============================================================

def exemplo_renderizacao_condicional():
    """Usar diferentes estratégias baseado no renderizador"""
    from hybrid_renderer import HybridRenderer, OPENGL_AVAILABLE
    
    renderer = HybridRenderer(800, 600)
    
    if OPENGL_AVAILABLE:
        print("GPU disponível - usando batch rendering")
        # Estratégia de batch rendering
        # Preparar múltiplos sprites para render em paralelo
    else:
        print("GPU indisponível - usando renderização simples")
        # Estratégia otimizada para CPU
        # Menos sprites, qualidade reduzida


# ============================================================
# EXEMPLO 7: Diagnóstico Integrado no Jogo
# ============================================================

def exemplo_diagnostico():
    """Adicionar info de debug durante o jogo"""
    import pygame
    from hybrid_renderer import HybridRenderer, RENDERER_TYPE
    
    renderer = HybridRenderer(1280, 720)
    font = pygame.font.Font(None, 24)
    
    # No loop de renderização:
    running = True
    clock = pygame.time.Clock()
    
    while running:
        renderer.clear_screen()
        
        # Render normal...
        
        # Mostrar debug info
        debug_text = f"GPU: {RENDERER_TYPE} | FPS: {clock.get_fps():.1f}"
        text_surface = font.render(debug_text, True, (255, 255, 255))
        renderer.draw_text(debug_text, font, (255, 255, 255), 10, 10)
        
        renderer.flip_display()
        clock.tick(60)


# ============================================================
# EXEMPLO 8: Fallback Automático em Erro
# ============================================================

def exemplo_error_handling():
    """Tratamento automático de erros com fallback"""
    from hybrid_renderer import HybridRenderer
    
    try:
        # Tentar criar com GPU
        renderer = HybridRenderer(1280, 720, use_opengl=True)
        print("✓ GPU ativada")
    except Exception as e:
        print(f"✗ Erro ao inicializar GPU: {e}")
        # Fallback automático
        renderer = HybridRenderer(1280, 720, use_opengl=False)
        print("✓ CPU ativada como fallback")


# ============================================================
# EXEMPLO 9: Integração com UI.py
# ============================================================

def exemplo_ui_integration():
    """Como usar renderizador com UI.py"""
    from ui import UI
    from hybrid_renderer import HybridRenderer
    
    # O UI.py usa pygame.display diretamente
    # O renderizador híbrido é compatível!
    
    renderer = HybridRenderer(1256, 768)
    ui = UI()
    
    # ui.desenhar_interface(tela, ...)
    # Funciona normalmente porque renderer.get_screen() retorna
    # a superfície pygame para compatibilidade


# ============================================================
# EXEMPLO 10: Monitoramento de Performance
# ============================================================

def exemplo_monitoring():
    """Monitorar performance em tempo real"""
    import time
    from hybrid_renderer import HybridRenderer
    from gpu_config import get_config
    
    renderer = HybridRenderer(1280, 720)
    config = get_config()
    
    print("Configuração de Renderização:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # No loop de jogo:
    frame_times = []
    
    for frame in range(100):
        frame_start = time.time()
        
        # Renderizar...
        renderer.flip_display()
        
        frame_times.append(time.time() - frame_start)
    
    avg_frame_time = sum(frame_times) / len(frame_times)
    fps = 1.0 / avg_frame_time
    
    print(f"\nPerformance:")
    print(f"  Tempo médio por frame: {avg_frame_time*1000:.2f}ms")
    print(f"  FPS: {fps:.1f}")


# ============================================================
# EXEMPLO 11: Testes Unitários
# ============================================================

def test_renderer_loading():
    """Teste: carregamento de sprites"""
    from hybrid_renderer import HybridRenderer
    
    renderer = HybridRenderer(800, 600)
    
    # Deve não falhar
    result = renderer.load_sprite("test", "assests/char.png", 40, 75)
    assert result is not None
    print("✓ Teste de carregamento passou")


def test_renderer_drawing():
    """Teste: desenho de primitivos"""
    from hybrid_renderer import HybridRenderer
    
    renderer = HybridRenderer(800, 600)
    
    # Deve não lançar exceção
    renderer.clear_screen((0, 0, 0))
    renderer.draw_rect(10, 10, 50, 50, (255, 0, 0))
    renderer.draw_circle(100, 100, 25, (0, 255, 0))
    renderer.flip_display()
    
    print("✓ Teste de desenho passou")


# ============================================================
# EXECUTAR EXEMPLOS
# ============================================================

if __name__ == "__main__":
    print("Exemplos de Integração - Renderizador Híbrido\n")
    
    # Descomentar o exemplo desejado:
    
    # exemplo_basico()
    # exemplo_benchmark()
    # exemplo_config()
    # print_config()
    
    print("Veja os exemplos disponíveis comentados neste arquivo")
