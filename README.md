# Fazenda Virtual

Um jogo de simulação de fazenda educacional feito em Pygame com suporte a renderização por GPU (OpenGL).

## 🚀 Como Executar

### Opção 1: Com GPU (Recomendado)
```bash
# Primeira vez - instalar dependências OpenGL
python3 install_opengl.py

# Executar o jogo
python3 main.py
```

### Opção 2: Apenas com Pygame (CPU)
```bash
python3 main.py
```

## 📋 Requisitos
- Python 3.12
- Pygame
- **GPU (Opcional)**: PyOpenGL, NumPy, PyGLM para renderização com GPU
- Imagens: `char.png`, `grama.png`

## 🎮 Suporte a GPU

O jogo detecta automaticamente se sua GPU está disponível:

- **✓ GPU Disponível**: Usa OpenGL 3.3+ para renderização paralela
- **✗ GPU Indisponível**: Fallback automático para Pygame (CPU)

### Verificar Compatibilidade

```bash
python3 test_gpu.py
```

### Durante o Jogo

Pressione **G** para ver qual renderizador está sendo usado:
```
Renderizador: OpenGL (GPU)  ← Usando aceleração de GPU
ou
Renderizador: Pygame (CPU)  ← Renderização por CPU
```

## 💾 Sistema de Save

### Menu Inicial
Ao iniciar o jogo, você verá um menu com opções:
- **Novo Jogo**: Inicia uma nova fazenda
- **Continuar Jogo**: Carrega o último save (se existir)
- **Deletar Save**: Remove o save atual (com confirmação)
- **Sair**: Fecha o jogo

### Salvamento
- **Automático**: O jogo é salvo automaticamente ao fechar
- **Manual**: Pressione **S** durante o jogo para salvar
- **Arquivo**: O save é armazenado em `fazenda_save.json`
- **Dados salvos**: Dinheiro, sementes, todas as plantas e seus estágios Pygame em que você ira plantar e colher diferentes tipos de sementes ao mesmo tempo em que gerencia seus recursos através de uma loja.

## Como Jogar

### Controles
- **Setas direcionais**: Mover o personagem
- **1, 2, 3**: Selecionar tipo de semente (Milho, Tomate, Alface)
- **Espaço**: Plantar semente ou colher planta madura (ação única)
- **Segurar Espaço**: Ação contínua - planta/colhe automaticamente enquanto se move
- **L**: Abrir/Fechar loja
- **S**: Salvar jogo manualmente
- **ESC**: Fechar loja (quando aberta)

### Controles da Loja
- **↑↓**: Navegar pelos itens da loja
- **ENTER**: Comprar 1 semente do item selecionado
- **SHIFT + ENTER**: Comprar 5 sementes do item selecionado
- **L ou ESC**: Fechar a loja

## Sistema de Loja

A loja permite que você compre mais sementes usando o dinheiro ganho com as colheitas. Pressione **L** para abrir a loja e navegar pelos itens disponíveis. Você pode comprar sementes individuais ou em pacotes de 5 para economizar tempo.

### Sistema de Sementes
O jogo possui 3 tipos de sementes, cada uma com características únicas:

#### Milho (Tecla 1)
- **Cor**: Amarelo
- **Preço**: $10
- **Valor da colheita**: $25
- **Tempo de crescimento**: 5 segundos por estágio
- **Lucro**: $15 por semente

#### Tomate (Tecla 2)
- **Cor**: Vermelho
- **Preço**: $15
- **Valor da colheita**: $40
- **Tempo de crescimento**: 8 segundos por estágio
- **Lucro**: $25 por semente

#### Alface (Tecla 3)
- **Cor**: Verde
- **Preço**: $8
- **Valor da colheita**: $20
- **Tempo de crescimento**: 3 segundos por estágio
- **Lucro**: $12 por semente

### Estágios de Crescimento
Todas as plantas passam por 7 estágios:
1. **Estágio 1-5**: Crescimento progressivo (planta fica maior)
2. **Estágio 6**: Madura (pronta para colheita - tamanho máximo)
3. **Estágio 7**: Estragada (cor marrom - não pode ser colhida)

### Mecânicas do Jogo
- **Dinheiro inicial**: $100
- **Sementes iniciais**: 5 milho, 3 tomate, 2 alface
- **Plantio**: Posicione-se sobre uma célula vazia e pressione Espaço
- **Plantio contínuo**: Segure Espaço e mova-se para plantar automaticamente
- **Colheita**: Só é possível no estágio 6 (madura)
- **Colheita contínua**: Segure Espaço e mova-se para colher automaticamente
- **Plantas estragadas**: No estágio 7, a planta não pode ser colhida e eventualmente desaparece
- **Compras**: Use a loja para adquirir mais sementes quando precisar

### Interface
- **Painel superior esquerdo**: Mostra dinheiro atual e quantidade de sementes
- **Grid da fazenda**: Linhas sutis dividem a área em células de plantio
- **Destaque**: Célula atual do jogador fica destacada em branco
- **Instruções**: Controles e dicas aparecem no canto inferior esquerdo
- **Loja**: Interface centralizada com navegação por setas e compra por ENTER

## Como Executar
```bash
cd /Users/vitortargino/apps/pygame
python3 main.py
```

## Requisitos
- Python 3.x
- Pygame
- Imagens: `char.png`, `grama.png`

## Estratégia
- **Alface**: Cresce mais rápido mas dá menos lucro - boa para dinheiro rápido
- **Tomate**: Mais lucrativo mas demora mais para crescer - investimento a longo prazo
- **Milho**: Meio termo entre velocidade e lucro - versátil
- **Timing**: Fique atento ao tempo para colher no estágio certo!
- **Ação contínua**: Use Espaço segurado para plantar/colher rapidamente em grandes áreas
- **Gestão de recursos**: Use a loja estrategicamente para expandir sua produção
- **Reinvestimento**: Use os lucros para comprar mais sementes e aumentar a produção

## Dicas da Loja
- Compare preços vs lucros para maximizar retorno
- Compre em pacotes de 5 quando tiver dinheiro suficiente
- Mantenha sempre algumas sementes em estoque
- Diversifique seus tipos de cultivo para ter colheitas em diferentes tempos

Divirta-se cultivando e expandindo sua fazenda virtual!
