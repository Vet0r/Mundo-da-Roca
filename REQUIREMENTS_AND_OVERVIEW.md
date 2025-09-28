# Fazenda Virtual - Requisitos e Visão Geral

## Visão Geral da Aplicação

### Conceito Principal
**Fazenda Virtual** é um jogo de simulação agrícola 2D desenvolvido em Python usando Pygame. O jogador controla um agricultor que deve plantar, cultivar e colher diferentes tipos de culturas em um sistema baseado em grid, gerenciando recursos financeiros e de sementes para expandir e otimizar sua fazenda.

### Classificação
- **Gênero**: Simulação/Gestão de Recursos
- **Estilo Visual**: 2D Top-down com sprites
- **Plataforma**: Desktop (Python/Pygame)
- **Público-alvo**: Todas as idades
- **Modo de jogo**: Single-player

---

## Requisitos Funcionais Atuais

### Sistema de Jogabilidade Core

#### RF001 - Movimentação do Personagem
- **Descrição**: O jogador controla um personagem que se move em 4 direções
- **Implementação**: Teclas direcionais (↑↓←→)
- **Velocidade**: 5 pixels por frame
- **Limitações**: Bordas da tela (800x600)

#### RF002 - Sistema de Grid
- **Descrição**: Área de jogo dividida em células de plantio
- **Tamanho**: Células de 40x40 pixels
- **Visualização**: Grid sutilmente visível
- **Funcionalidade**: Base para sistema de plantio/colheita

#### RF003 - Seleção de Sementes
- **Descrição**: Sistema de seleção entre 3 tipos de sementes
- **Controles**: Teclas 1, 2, 3
- **Tipos Disponíveis**:
  - Milho (1): Amarelo, crescimento médio
  - Tomate (2): Vermelho, crescimento lento  
  - Alface (3): Verde, crescimento rápido

### Sistema de Cultivo

#### RF004 - Plantio de Sementes
- **Descrição**: Capacidade de plantar sementes em células vazias
- **Controle**: Espaço (ação única) ou Espaço segurado (ação contínua)
- **Validações**: 
  - Célula deve estar vazia
  - Jogador deve ter sementes disponíveis
- **Consumo**: 1 semente por plantio

#### RF005 - Crescimento Temporal
- **Descrição**: Sistema de crescimento automático baseado em tempo real
- **Estágios**: 7 estágios de crescimento por planta
  - Estágios 1-5: Crescimento progressivo
  - Estágio 6: Maduro (colhível)
  - Estágio 7: Estragado (perdido)
- **Tempos de Crescimento**:
  - Alface: 3 segundos por estágio
  - Milho: 5 segundos por estágio
  - Tomate: 8 segundos por estágio

#### RF006 - Sistema de Colheita
- **Descrição**: Colheita de plantas maduras para obter dinheiro
- **Condições**: Apenas plantas no estágio 6
- **Controle**: Espaço (ação única) ou Espaço segurado (ação contínua)
- **Recompensas**:
  - Alface: $20
  - Milho: $25
  - Tomate: $40

#### RF007 - Deterioração de Plantas
- **Descrição**: Plantas não colhidas eventualmente estragam
- **Comportamento**: Estágio 7 torna plantas não colhíveis
- **Limpeza**: Plantas estragadas são removidas automaticamente

### Sistema Econômico

#### RF008 - Gestão de Dinheiro
- **Descrição**: Sistema monetário do jogo
- **Valor Inicial**: $100
- **Fontes de Renda**: Colheita de plantas maduras
- **Gastos**: Compra de sementes na loja

#### RF009 - Inventário de Sementes
- **Descrição**: Sistema de gestão de sementes disponíveis
- **Estoque Inicial**:
  - Milho: 5 unidades
  - Tomate: 3 unidades  
  - Alface: 2 unidades
- **Reposição**: Através da loja

#### RF010 - Sistema de Loja
- **Descrição**: Interface para compra de sementes
- **Acesso**: Tecla L
- **Funcionalidades**:
  - Navegação com ↑↓
  - Compra unitária (Enter)
  - Compra em lote - 5 unidades (Shift+Enter)
- **Preços**:
  - Alface: $8
  - Milho: $10
  - Tomate: $15

### Sistema de Interface

#### RF011 - HUD (Interface Principal)
- **Descrição**: Painel de informações permanente
- **Localização**: Canto superior esquerdo
- **Conteúdo**:
  - Dinheiro atual
  - Quantidade de sementes por tipo
  - Semente atualmente selecionada
  - Instruções básicas

#### RF012 - Sistema de Feedback Visual
- **Descrição**: Indicadores visuais para o jogador
- **Elementos**:
  - Destaque da célula atual (quadrado branco)
  - Plantas com cores diferenciadas por tipo
  - Plantas estragadas (cor marrom)
  - Interface da loja centralizada

---

## Arquitetura para Futuras Expansões

### Preparação para Modularização
O código atual está em um arquivo monolítico, mas está estruturado de forma que pode ser facilmente separado em módulos:

#### Módulos Sugeridos:
1. **game_engine.py** - Loop principal e gerenciamento de estados
2. **player.py** - Lógica do personagem e controles
3. **farm_system.py** - Sistema de plantio, crescimento e colheita
4. **economy.py** - Sistema econômico e loja
5. **ui_manager.py** - Interface de usuário e renderização
6. **asset_manager.py** - Gerenciamento de recursos (imagens, sons)
7. **config.py** - Configurações e constantes
8. **save_system.py** - Sistema de save/load (futuro)

### Pontos de Extensão Identificados:
- **Novos Tipos de Cultivo**: Fácil adição via dicionário TIPOS_SEMENTE
- **Sistema de Upgrades**: Base econômica já estabelecida
- **Múltiplas Fazendas**: Sistema de grid pode ser expandido
- **Animais**: Estrutura similar ao sistema de plantas
- **Clima/Estações**: Pode afetar tempos de crescimento
- **Multiplayer**: Arquitetura permite separação cliente/servidor

---

## Métricas e Balanceamento Atual

### Economia
| Semente | Custo | Valor Colheita | Lucro | Tempo Total | Lucro/Segundo |
|---------|-------|----------------|-------|-------------|---------------|
| Alface  | $8    | $20            | $12   | 21s         | $0.57/s       |
| Milho   | $10   | $25            | $15   | 35s         | $0.43/s       |
| Tomate  | $15   | $40            | $25   | 56s         | $0.45/s       |

### Observações de Balanceamento:
- Alface oferece maior retorno por segundo
- Tomate oferece maior lucro absoluto
- Milho é intermediário em todos os aspectos
- Sistema incentiva diversificação de cultivos

---

## Conclusão

A **Fazenda Virtual** apresenta uma implementação funcional de um simulador agrícola com mecânicas básicas bem estabelecidas. O sistema atual oferece uma experiência de jogo completa através de seus três pilares principais: cultivo temporal, gestão econômica e interface intuitiva.

O sistema de cultivo com 7 estágios de crescimento proporciona uma progressão temporal interessante, enquanto o sistema econômico com três tipos de sementes diferentes oferece escolhas estratégicas ao jogador. A interface de loja e o sistema de ação contínua tornam a experiência de jogo fluida e acessível.

A arquitetura modular sugerida indica que o código está preparado para expansões futuras, mantendo a base atual como fundamento sólido para desenvolvimentos adicionais. O balanceamento econômico atual demonstra equilíbrio entre as diferentes opções de cultivo, incentivando a diversificação de estratégias.

Este documento serve como referência técnica para o estado atual da aplicação e como guia para futuras modificações e expansões do sistema.
