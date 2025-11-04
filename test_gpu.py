#!/usr/bin/env python3
"""
Script de teste e diagnóstico de GPU
Execute: python3 test_gpu.py
"""

import sys
import platform
import subprocess

def print_section(title):
    """Imprimir seção de título"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)

def test_system_info():
    """Testar informações do sistema"""
    print_section("INFORMAÇÕES DO SISTEMA")
    
    print(f"Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"Arquitetura: {platform.machine()}")
    print(f"Versão Python: {sys.version}")
    print(f"Compilador Python: {platform.python_compiler()}")

def test_pygame():
    """Testar instalação do Pygame"""
    print_section("TESTE PYGAME")
    
    try:
        import pygame
        print(f"✓ Pygame: {pygame.version.ver}")
        print(f"  Pygame SDL: {pygame.version.SDL}")
        return True
    except ImportError as e:
        print(f"✗ Pygame não instalado: {e}")
        return False

def test_opengl():
    """Testar suporte a OpenGL"""
    print_section("TESTE OPENGL")
    
    try:
        import pygame
        pygame.init()
        
        # Tentar criar contexto OpenGL
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        
        # Criar janela oculta
        display = pygame.display.set_mode((100, 100), pygame.OPENGL | pygame.HIDDEN)
        
        from OpenGL.GL import glGetString, GL_VERSION, GL_RENDERER, GL_VENDOR, GL_SHADING_LANGUAGE_VERSION
        
        version = glGetString(GL_VERSION).decode('utf-8') if glGetString(GL_VERSION) else "Desconhecida"
        renderer = glGetString(GL_RENDERER).decode('utf-8') if glGetString(GL_RENDERER) else "Desconhecida"
        vendor = glGetString(GL_VENDOR).decode('utf-8') if glGetString(GL_VENDOR) else "Desconhecida"
        
        try:
            glsl_version = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
        except:
            glsl_version = "Desconhecida"
        
        print(f"✓ OpenGL suportado")
        print(f"  Versão OpenGL: {version}")
        print(f"  GPU (Renderer): {renderer}")
        print(f"  Vendor: {vendor}")
        print(f"  GLSL Version: {glsl_version}")
        
        pygame.display.quit()
        return True
        
    except Exception as e:
        print(f"✗ OpenGL não disponível: {e}")
        pygame.quit()
        return False

def test_dependencies():
    """Testar dependências OpenGL"""
    print_section("TESTE DEPENDÊNCIAS")
    
    dependencies = {
        'PyOpenGL': 'OpenGL.GL',
        'numpy': 'numpy',
        'PyGLM': 'glm',
    }
    
    results = {}
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            module = sys.modules[import_name]
            version = getattr(module, '__version__', 'Desconhecida')
            print(f"✓ {package}: {version}")
            results[package] = True
        except ImportError:
            print(f"✗ {package}: Não instalado")
            results[package] = False
    
    return all(results.values())

def test_renderer():
    """Testar renderizador híbrido"""
    print_section("TESTE RENDERIZADOR HÍBRIDO")
    
    try:
        from hybrid_renderer import check_opengl_support, RENDERER_TYPE, OPENGL_AVAILABLE
        
        print(f"Renderizador detectado: {RENDERER_TYPE}")
        print(f"OpenGL disponível: {'Sim' if OPENGL_AVAILABLE else 'Não'}")
        
        if OPENGL_AVAILABLE:
            print("✓ Sistema está pronto para GPU!")
        else:
            print("ℹ Sistema usará renderização por CPU")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar renderizador: {e}")
        return False

def test_performance():
    """Teste simples de performance"""
    print_section("TESTE PERFORMANCE")
    
    try:
        import pygame
        import time
        
        pygame.init()
        display = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        
        print("Executando teste de renderização...")
        print("(100 frames)")
        
        start = time.time()
        for i in range(100):
            display.fill((30, 30, 30))
            pygame.draw.circle(display, (255, 0, 0), (400, 300), 50)
            pygame.display.flip()
            clock.tick(60)
        
        elapsed = time.time() - start
        avg_fps = 100 / elapsed if elapsed > 0 else 0
        
        print(f"Tempo total: {elapsed:.2f}s")
        print(f"FPS médio: {avg_fps:.1f}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ Erro no teste de performance: {e}")
        return False

def install_opengl():
    """Oferecer instalação de dependências"""
    print_section("INSTALAÇÃO DE DEPENDÊNCIAS")
    
    print("Para instalar dependências OpenGL, execute:")
    print("\n  python3 install_opengl.py\n")
    print("Ou instale manualmente:")
    print("  pip install PyOpenGL PyOpenGL-accelerate numpy PyGLM")

def main():
    """Executar testes"""
    print("\n" + "="*60)
    print("TESTE E DIAGNÓSTICO DE GPU - Mundo-da-Roca")
    print("="*60)
    
    # Executar testes
    has_pygame = test_pygame()
    
    if not has_pygame:
        print("\n✗ Pygame não está instalado")
        print("  Execute: pip install pygame")
        sys.exit(1)
    
    has_opengl = test_opengl()
    has_deps = test_dependencies()
    renderer_ok = test_renderer()
    test_performance()
    
    # Resumo
    print_section("RESUMO")
    
    print("\nStatus:")
    print(f"  Pygame: {'✓' if has_pygame else '✗'}")
    print(f"  OpenGL: {'✓' if has_opengl else '✗'}")
    print(f"  Dependências: {'✓' if has_deps else '✗'}")
    print(f"  Renderizador: {'✓' if renderer_ok else '✗'}")
    
    print("\nResultado:")
    if has_pygame and has_opengl and has_deps:
        print("✓ Sistema pronto para GPU!")
        print("\nExecute: python3 main.py")
    elif has_pygame:
        print("ℹ Pygame funcionando - renderização por CPU ativada")
        print("\nPara ativar GPU:")
        print("  python3 install_opengl.py")
        print("\nExecute: python3 main.py")
    else:
        print("✗ Erro: Pygame não instalado")
        install_opengl()
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTeste cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
