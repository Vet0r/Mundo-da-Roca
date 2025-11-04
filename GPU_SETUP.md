# 🚀 Suporte a GPU (OpenGL) - Mundo-da-Roca

Implementação de renderização com OpenGL para usar a GPU do computador, com fallback automático para Pygame se OpenGL não estiver disponível.

## ✨ Características

- **Renderização Híbrida**: Detecta automaticamente disponibilidade de OpenGL
- **GPU Acceleration**: Usa a GPU quando disponível (OpenGL 3.3+)
- **Fallback Automático**: Retorna para CPU (Pygame) se GPU não estiver disponível
- **Sem Quebra de Compatibilidade**: Código existente continua funcionando
- **Detecção de Sistema**: Verifica dependências automaticamente

## 📦 Instalação de Dependências

### Opção 1: Script Automático (Recomendado)

```bash
python3 install_opengl.py
```

### Opção 2: Instalação Manual

```bash
# Instalar PyOpenGL
pip install PyOpenGL PyOpenGL-accelerate

# Instalar dependências de suporte
pip install numpy PyGLM

# Verificar no macOS (se necessário)
brew install glfw3
```

## 🎮 Como Usar

### Executar com GPU (se disponível)

```bash
python3 main.py
```

O jogo detectará automaticamente se OpenGL está disponível e utilizará GPU.

### Forçar Renderização por CPU

Se tiver problemas com OpenGL, o jogo automaticamente fará fallback para Pygame. Para forçar manualmente:

```bash
# Editar main.py e mudar:
# use_opengl=True para use_opengl=False
```

### Verificar Renderizador em Uso

Durante o jogo, pressione **G** para ver qual renderizador está sendo usado:

```
Renderizador: OpenGL (GPU)
ou
Renderizador: Pygame (CPU)
```

## 📊 Comparação de Performance

| Aspecto | GPU (OpenGL) | CPU (Pygame) |
|---------|--------------|--------------|
| Renderização de Sprites | Paralela na GPU | Serial na CPU |
| Escalabilidade | Excelente | Limitada |
| Uso de Vídeo RAM | 50-200 MB | 0 MB |
| Latência | Menor | Maior |
| Compatibilidade | Requer GPU | Universal |

## 🔧 Arquivos Novos

- `opengl_renderer.py` - Renderizador com shaders OpenGL (completo)
- `hybrid_renderer.py` - Renderizador híbrido (GPU/CPU)
- `install_opengl.py` - Script de instalação de dependências
- `main_gpu.py` - Versão atualizada do main.py com suporte GPU

## 🐛 Troubleshooting

### "ImportError: No module named OpenGL"

```bash
pip install PyOpenGL
```

### "OpenGL context creation failed"

Seu sistema não tem suporte a OpenGL 3.3+. O jogo utilizará Pygame (CPU).

### Performance ruim com GPU

1. Verifique se drivers da GPU estão atualizados
2. Reduza resolução da janela
3. Pressione 'G' para verificar qual renderizador está sendo usado

### macOS - Problemas com GPU

```bash
# Atualizar drivers é recomendado
brew install glfw3
pip install --upgrade PyOpenGL
```

## 📈 Monitoramento

Durante o jogo, você pode:

- **Pressionar G**: Ver informações do renderizador
- **Pressionar F11**: Alternar tela cheia (ambos os modos otimizados)
- **Ver Console**: Mensagens de inicialização indicam qual renderizador está ativo

## 🎯 Próximos Passos para Otimização

1. **Batch Rendering**: Agrupar sprites para menos chamadas OpenGL
2. **Shader Customizado**: Efeitos de iluminação na GPU
3. **Particle System**: Efeitos de partículas renderizados na GPU
4. **Textura Atlas**: Combinar múltiplas texturas em uma

## 📝 Exemplo de Código

```python
from hybrid_renderer import HybridRenderer, OPENGL_AVAILABLE, RENDERER_TYPE

# Criar renderizador (auto-detecta)
renderer = HybridRenderer(1256, 768, "Meu Jogo")

print(f"Usando: {RENDERER_TYPE}")  # "OpenGL (GPU)" ou "Pygame (CPU)"

# Renderizar normalmente
renderer.draw_sprite("char", 100, 100)
renderer.flip_display()
```

## ⚙️ Configuração Avançada

### Forçar OpenGL 4.1 (macOS)

Editar `hybrid_renderer.py`:

```python
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
```

### Habilitar VSync

```python
pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)
```

## 📚 Referências

- [PyOpenGL Docs](https://pyopengl.sourceforge.net/)
- [Pygame OpenGL](https://www.pygame.org/docs/ref/pygame.html#pygame.GL_)
- [OpenGL ES 3.0](https://www.khronos.org/opengl/wiki/OpenGL_ES)

---

**Desenvolvido com ❤️ para melhor performance do Mundo-da-Roca**
