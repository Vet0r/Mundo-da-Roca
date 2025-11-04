"""
Configurações de Renderização e GPU
Otimizações e ajustes de performance
"""

# ============================================================
# CONFIGURAÇÕES DE RENDERIZAÇÃO
# ============================================================

# Usar GPU quando disponível
USE_GPU = True

# Qualidade de renderização
# 'ultra' (máxima qualidade, + processamento)
# 'high' (boa qualidade, processamento médio)
# 'medium' (qualidade média, melhor performance)
# 'low' (qualidade mínima, máxima performance)
RENDER_QUALITY = 'high'

# FPS máximo (limitador)
MAX_FPS = 60

# VSync (sincronizar com monitor)
USE_VSYNC = True

# ============================================================
# CONFIGURAÇÕES DE OPENGL
# ============================================================

# Versão mínima requerida do OpenGL
OPENGL_VERSION_MAJOR = 3
OPENGL_VERSION_MINOR = 3

# Usar Core Profile (recomendado para 3.3+)
OPENGL_CORE_PROFILE = True

# Habilitar Framebuffer Object para render targets
USE_FBO = False

# Habilitar Shader Caching
CACHE_SHADERS = True

# ============================================================
# OTIMIZAÇÕES
# ============================================================

# Ativar Batch Rendering (agrupar desenhos)
BATCH_RENDERING = True

# Batch size - quantos sprites desenhar por batch
BATCH_SIZE = 100

# Ativar Frustum Culling (não desenhar o que não vê)
FRUSTUM_CULLING = True

# Ativar Dynamic LOD (reduzir qualidade de longe)
DYNAMIC_LOD = False

# ============================================================
# CONFIGURAÇÕES DE TEXTURA
# ============================================================

# Tamanho máximo de textura (potência de 2)
MAX_TEXTURE_SIZE = 2048

# Ativar compressão de textura
TEXTURE_COMPRESSION = False

# Mipmapping
MIPMAP_ENABLED = True

# Filtro de textura
# 'nearest' (pixelado, mais rápido)
# 'linear' (suave, mais lento)
TEXTURE_FILTER = 'linear'

# ============================================================
# DEBUG E MONITORAMENTO
# ============================================================

# Ativar logs de debug
DEBUG_MODE = False

# Mostrar stats de performance
SHOW_PERFORMANCE_STATS = False

# Mostrar grid de debug
SHOW_DEBUG_GRID = False

# Ativar validação de OpenGL (mais lento em debug)
OPENGL_DEBUG = False

# ============================================================
# PRESETS
# ============================================================

PRESETS = {
    'performance': {
        'RENDER_QUALITY': 'low',
        'MAX_FPS': 120,
        'BATCH_RENDERING': True,
        'BATCH_SIZE': 200,
        'FRUSTUM_CULLING': True,
        'MIPMAP_ENABLED': False,
        'TEXTURE_FILTER': 'nearest',
    },
    'balanced': {
        'RENDER_QUALITY': 'medium',
        'MAX_FPS': 60,
        'BATCH_RENDERING': True,
        'BATCH_SIZE': 100,
        'FRUSTUM_CULLING': True,
        'MIPMAP_ENABLED': True,
        'TEXTURE_FILTER': 'linear',
    },
    'quality': {
        'RENDER_QUALITY': 'high',
        'MAX_FPS': 60,
        'BATCH_RENDERING': True,
        'BATCH_SIZE': 50,
        'FRUSTUM_CULLING': True,
        'MIPMAP_ENABLED': True,
        'TEXTURE_FILTER': 'linear',
    },
    'ultra': {
        'RENDER_QUALITY': 'ultra',
        'MAX_FPS': 144,
        'BATCH_RENDERING': True,
        'BATCH_SIZE': 20,
        'FRUSTUM_CULLING': True,
        'DYNAMIC_LOD': True,
        'MIPMAP_ENABLED': True,
        'TEXTURE_FILTER': 'linear',
    },
}

def apply_preset(preset_name):
    """Aplicar preset de configuração"""
    global RENDER_QUALITY, MAX_FPS, BATCH_RENDERING, BATCH_SIZE
    global FRUSTUM_CULLING, DYNAMIC_LOD, MIPMAP_ENABLED, TEXTURE_FILTER
    
    if preset_name not in PRESETS:
        print(f"Preset '{preset_name}' não encontrado")
        return False
    
    preset = PRESETS[preset_name]
    for key, value in preset.items():
        if key.startswith('_'):
            continue
        try:
            globals()[key] = value
        except KeyError:
            pass
    
    print(f"✓ Preset '{preset_name}' aplicado")
    return True

def get_config():
    """Retornar configuração atual como dicionário"""
    return {
        'use_gpu': USE_GPU,
        'render_quality': RENDER_QUALITY,
        'max_fps': MAX_FPS,
        'opengl_version': f"{OPENGL_VERSION_MAJOR}.{OPENGL_VERSION_MINOR}",
        'batch_rendering': BATCH_RENDERING,
        'batch_size': BATCH_SIZE,
        'frustum_culling': FRUSTUM_CULLING,
        'texture_filter': TEXTURE_FILTER,
    }

def print_config():
    """Imprimir configuração atual"""
    config = get_config()
    print("\n" + "="*60)
    print("CONFIGURAÇÃO ATUAL DE RENDERIZAÇÃO")
    print("="*60)
    for key, value in config.items():
        print(f"{key:.<40} {value}")
    print("="*60 + "\n")

# Aplicar preset padrão (balanced)
def init_default():
    """Inicializar com configurações padrão"""
    apply_preset('balanced')

# Inicializar ao importar
if __name__ != "__main__":
    init_default()
