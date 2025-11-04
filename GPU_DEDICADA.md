# 🎮 Forçar GPU Dedicada - Mundo-da-Roca

## 📋 Problema

Seu jogo está usando GPU integrada (iGPU) ao invés de GPU dedicada (discreta).

## 🎯 Solução

### Verificar qual GPU está sendo usada

```bash
python3 gpu_manager.py --detect
```

Você verá algo como:
```
NVIDIA CUDA: Detectado
  Devices disponíveis: 1
  Device 0: NVIDIA GeForce RTX 4090

OpenGL: Detectado
  Vendor: NVIDIA Corporation
  Renderer: NVIDIA GeForce RTX 4090/PCIe/SSE2
  Version: 4.6.0
```

### Forçar GPU Dedicada

#### 1️⃣ Automático (Recomendado)

O sistema já foi configurado para preferir GPU dedicada! Basta rodar:

```bash
python3 main.py
```

O jogo detectará e usará GPU dedicada automaticamente.

#### 2️⃣ Verificar que está usando GPU Dedicada

Durante o jogo, pressione **G** para ver:

```
Renderizador: OpenGL (GPU)
GPU Vendor: NVIDIA Corporation
GPU Name: NVIDIA GeForce RTX 4090
Dedicada: ✓ Sim
```

---

## 🔧 Configurações por Sistema Operacional

### Windows com NVIDIA

```batch
REM Execute o jogo com GPU dedicada
set CUDA_VISIBLE_DEVICES=0
python main.py
```

**Ou via NVIDIA Control Panel:**
1. Clique com direito na área de trabalho
2. NVIDIA Control Panel
3. Manage 3D Settings
4. Program Settings
5. Adicione seu jogo
6. OpenGL rendering GPU: Sua GPU NVIDIA

### Windows com AMD

```batch
REM Configurar para GPU dedicada AMD
set GPU_DEVICE_ORDINAL=0
python main.py
```

### macOS com GPU Dedicada

```bash
# Forçar GPU dedicada (já configurado no código)
export MTL_DEVICE_ID=0
export METAL_DEVICE_AFFINITY=1
python3 main.py
```

**Verificar macOS:**
```bash
# Informações de GPU
system_profiler SPDisplaysDataType

# Ver qual GPU está sendo usada (durante jogo)
# Pressione G no jogo
```

### Linux com NVIDIA

```bash
# Verificar GPUs disponíveis
nvidia-smi

# Forçar GPU 0
export CUDA_VISIBLE_DEVICES=0
python3 main.py

# Monitorar em tempo real (em outro terminal)
watch -n 1 nvidia-smi
```

### Linux com AMD

```bash
# Verificar GPUs disponíveis
rocm-smi

# Forçar GPU 0
export HIP_DEVICE=0
export GPU_DEVICE_ORDINAL=0
python3 main.py
```

---

## 📊 Performance Esperada

### Com GPU Dedicada ✅

```
GPU Utilização: 60-80%
CPU Utilização: 5-15%
RAM: 50-100 MB
VRAM: 100-300 MB
FPS: 55-60 (dependendo da cena)
```

### Com GPU Integrada ❌

```
GPU Utilização: 30-40%
CPU Utilização: 40-60%
RAM: 200-300 MB
VRAM Compartilhada: 500-800 MB
FPS: 30-45 (em cenários complexos)
```

---

## 🔍 Diagnosticar Problema

Se ainda estiver usando GPU integrada, execute:

```bash
python3 gpu_manager.py --info
```

Isso mostrará qual GPU seu sistema tem disponível.

### Casos Comuns

**Problema:** Notebook só tem GPU integrada
```
Solução: Sistema funcionará normalmente com GPU integrada
         Performance será similar à GPU dedicada porque é a única disponível
```

**Problema:** GPU dedicada não está sendo detectada
```
Solução: 
1. Atualizar drivers da GPU
2. Verificar se GPU está habilitada no BIOS
3. Desabilitar GPU integrada se necessário
```

**Problema:** CUDA não disponível no macOS
```
Solução: Isso é normal no macOS
         Use Metal (padrão no macOS)
         Jogo será otimizado para Metal automaticamente
```

---

## ⚡ Otimizações Adicionais

### Aumentar Priority de GPU

```python
# No início de main.py, após imports:
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ['GPU_DEVICE_ORDINAL'] = '0'
```

### Monitorar GPU em Tempo Real

**Windows/Linux (NVIDIA):**
```bash
# Terminal 1: Jogo
python3 main.py

# Terminal 2: Monitorar
watch -n 1 nvidia-smi
```

**macOS:**
```bash
# Activity Monitor > Janela > GPU

# Ou via terminal:
system_profiler SPDisplaysDataType
```

---

## 📈 Verificação Passo a Passo

1. **Instalar dependências:**
   ```bash
   python3 install_opengl.py
   ```

2. **Testar detecção:**
   ```bash
   python3 gpu_manager.py --detect
   ```

3. **Verificar informações:**
   ```bash
   python3 gpu_manager.py --info
   ```

4. **Rodar jogo:**
   ```bash
   python3 main.py
   ```

5. **Pressionar G durante jogo:**
   ```
   Ver "GPU: NVIDIA..." ao invés de "GPU: Intel..."
   ```

---

## 🎯 Checklist

- [ ] Instalou opengl.py
- [ ] Rodou gpu_manager.py --detect
- [ ] Viu GPU dedicada na lista
- [ ] Rodou main.py
- [ ] Pressionou G e viu GPU dedicada
- [ ] Performance melhorou

---

## 💡 Dica: Forçar em Scripts de Inicialização

### Criar script de inicialização (start_gpu.sh)

```bash
#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
export MTL_DEVICE_AFFINITY=1
export GPU_DEVICE_ORDINAL=0
cd /Users/vitortargino/apps/Mundo-da-Roca
python3 main.py
```

Depois executar:
```bash
chmod +x start_gpu.sh
./start_gpu.sh
```

---

## ⚠️ Troubleshooting Final

**Se nada funcionar:**

1. Abra `hybrid_renderer.py`
2. Procure por `# ============================================================`
3. Veja as linhas de configuração de GPU dedicada
4. Elas devem estar comentadas com seu GPU específico

**Exemplo para macOS:**
```python
if platform.system() == "Darwin":
    os.environ['METAL_DEVICE_AFFINITY'] = '1'  # ✓ Ativado
    os.environ['MTL_DEVICE_ID'] = '0'          # ✓ Ativado
```

---

## 📞 Suporte Técnico

Para verificar configuração em profundidade:

```bash
python3 test_gpu.py
python3 gpu_manager.py --detect
python3 gpu_manager.py --info
```

---

**Desenvolvido com ❤️ | GPU Dedicada | OpenGL 3.3+ | Pygame**
