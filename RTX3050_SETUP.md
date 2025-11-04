# 🎮 Forçar GPU NVIDIA RTX 3050 - Guia Específico

Seu setup: **NVIDIA RTX 3050 (6GB VRAM)**

## ⚡ Quick Fix (2 minutos)

### Passo 1: Executar diagnóstico
```bash
python3 nvidia_diagnostic.py
```

Procure por:
- ✅ "nvidia-smi" - deve funcionar
- ✅ "NVIDIA GeForce RTX 3050" - deve aparecer
- ✅ "Memory Total: 6.00 GB" - deve mostrar

### Passo 2: Executar com GPU forçada
```bash
python3 run_with_nvidia.py
```

Este script:
1. Configura variáveis de ambiente CUDA
2. Força GPU 0 (sua RTX 3050)
3. Inicia o jogo
4. Mostra qual GPU está usando

### Passo 3: Verificar no jogo
Pressione **G** durante o jogo

Deve mostrar:
```
✓ GPU Vendor: NVIDIA Corporation
✓ GPU Name: NVIDIA GeForce RTX 3050
✓ GPU Dedicada detectada
```

---

## 🔍 Se Não Aparecer

### Problema 1: nvidia-smi não funciona

**Solução:**
```bash
# Verificar se drivers estão instalados
nvidia-smi

# Se não encontrar, reinstalar drivers:
# Windows: https://www.nvidia.com/Download/index.aspx?lang=en-us
# Linux: sudo apt install nvidia-driver-550
# macOS: Use Metal (não suporta NVIDIA)
```

### Problema 2: nvidia-smi funciona mas OpenGL usa iGPU

**Solução - Editar `main.py`:**

Adicione NO INÍCIO (antes de `import pygame`):

```python
import os

# ============================================================
# FORÇAR GPU NVIDIA RTX 3050
# ============================================================

os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ['CUDA_FORCE_PTX_JIT'] = '1'

# Linha do pygame deve estar DEPOIS disso:
import pygame
```

### Problema 3: OpenGL mostra Intel mas nvidia-smi mostra 3050

**Causa:** Pygame/OpenGL está usando GPU integrada

**Solução:**

1. **Verificar qual GPU está no BIOS:**
   - Reinicie o PC
   - Entre no BIOS (DEL, F2, ou F10 durante boot)
   - Procure por "Primary GPU" ou "GPU Priority"
   - Defina para NVIDIA ou Discrete GPU

2. **Desabilitar GPU integrada (opcional):**
   - BIOS > Integrated Graphics > Disabled
   - Isto força usar NVIDIA

3. **Usar NVIDIA Control Panel (Windows):**
   - Clique direito > NVIDIA Control Panel
   - 3D Settings > Manage 3D Settings
   - Global Settings > Preferred Graphics Processor
   - Selecione "NVIDIA GeForce RTX 3050"

---

## 📊 Verificar Performance

### Monitorar GPU em tempo real

**Windows (cmd):**
```batch
# Em outro terminal, enquanto o jogo roda:
nvidia-smi -l 1
```

Procure por:
- **GPU**: 0 (sua RTX 3050)
- **Memory Used**: Deve crescer quando o jogo inicia
- **GPU-Util**: Deve ser 60%+ quando o jogo roda

**Linux:**
```bash
watch -n 1 nvidia-smi
```

**macOS:**
```bash
system_profiler SPDisplaysDataType
```

---

## ✅ Checklist

- [ ] Executou `nvidia_diagnostic.py`
- [ ] Viu RTX 3050 no output
- [ ] Executou `python3 run_with_nvidia.py`
- [ ] Pressionou G e viu NVIDIA RTX 3050
- [ ] Monitora nvidia-smi enquanto joga
- [ ] Vê GPU Util > 50% e Memory > 500MB

---

## 📈 Performance Esperada (RTX 3050 6GB)

### Cenários
```
Simples (poucas plantas):       60 FPS (limitado)
Médio (mapa com várias plantas): 55-60 FPS
Complexo (muitas plantas/efeitos): 50-60 FPS
Tela Cheia (1920x1080):         50-60 FPS
```

### Comparação
```
Com RTX 3050:    55-60 FPS | GPU 70% | VRAM 1.5GB
Sem otimização:  25-40 FPS | CPU 100% | RAM 800MB
```

---

## 🔧 Forçar GPU Manualmente (Terminal)

### Windows
```batch
set CUDA_DEVICE_ORDER=PCI_BUS_ID
set CUDA_VISIBLE_DEVICES=0
python main.py
```

### Linux
```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=0
python3 main.py
```

### macOS
```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=0
python3 main.py
```

---

## 💾 Criar Script Permanente

### Windows (create_run_nvidia.bat)
```batch
@echo off
set CUDA_DEVICE_ORDER=PCI_BUS_ID
set CUDA_VISIBLE_DEVICES=0
set CUDA_LAUNCH_BLOCKING=1
cd /d "%~dp0"
python main.py
pause
```

**Usar:**
1. Salvar como `run_nvidia.bat` na pasta do jogo
2. Clicar 2x para rodar

### Linux/macOS (create_run_nvidia.sh)
```bash
#!/bin/bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=0
export CUDA_LAUNCH_BLOCKING=1
python3 main.py
```

**Usar:**
```bash
chmod +x run_nvidia.sh
./run_nvidia.sh
```

---

## 🐛 Troubleshooting Avançado

### GPU mostrada como "GPU-0" ou device desconhecido

**Solução:**
Verificar em `nvidia_diagnostic.py` qual é o device ID correto
```python
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Ou 1, 2, etc
```

### "Out of Memory" com RTX 3050

**Não deve acontecer** (você tem 6GB)
Mas se acontecer:
1. Reduzir resolução
2. Fechar outros programas
3. Limpar cache: `nvidia-smi --gpu-reset`

### Driver crash ou OpenGL error

**Solução:**
1. Atualizar driver NVIDIA para versão mais recente
2. Usar `CUDA_LAUNCH_BLOCKING=1` (já está configurado)
3. Se continuar: atualizar Windows/Linux/macOS

---

## 📞 Suporte

Se ainda não funcionar:

1. **Rodar diagnóstico completo:**
   ```bash
   python3 nvidia_diagnostic.py
   ```

2. **Verificar drivers:**
   ```bash
   nvidia-smi --query-gpu=driver_version --format=csv
   ```

3. **Limpar cache CUDA:**
   ```bash
   nvidia-smi --gpu-reset
   ```

4. **Se nada funcionar:**
   - Atualizar drivers NVIDIA
   - Reiniciar PC
   - Verificar BIOS (Primary GPU)

---

## 📋 Resumo dos Arquivos

| Arquivo | Função |
|---------|--------|
| `run_with_nvidia.py` | Executar com GPU forçada |
| `nvidia_diagnostic.py` | Diagnosticar problema |
| `hybrid_renderer.py` | Configurações automáticas |
| `main.py` | Jogo principal (adicione código acima) |

---

## ✨ Resultado Final

Quando tudo estiver funcionando:
- ✅ RTX 3050 aparece em nvidia-smi
- ✅ OpenGL detecta NVIDIA
- ✅ Pressionar G mostra RTX 3050
- ✅ FPS estável 55-60
- ✅ Performance máxima com 6GB VRAM

---

**Desenvolvido para RTX 3050 | CUDA | OpenGL 4.6 | Pygame**
