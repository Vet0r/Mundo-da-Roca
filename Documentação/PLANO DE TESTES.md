**Plano de teste**   
Universidade Federal Rural do Semi-Árido

# Projeto Mundo da Roça

## **27 de setembro de 2025**

**Responsáveis:**

**Vitor Targino(Organização) Email \- vitor.andrade@alunos.ufersa.edu.br**

**Rômulo Levy (Integrante) Email \- romulo.oliveira39222@alunos.ufersa.edu.br**

# **VISÃO GERAL**

O projeto Mundo da Roça, é um jogo em que o jogador terá o prazer de ter uma experiência rasa mas divertida da geração dos alimentos que chegam a sua casa. ele fará o papel de um agricultor onde terá de cuidar do solo, plantar grãos, fazer colheitas, utilizar maquinário do campo e contratar trabalhadores para ajudar a refazer esse ciclo; O jogador terá informações sobre as plantas como solo ideal, clima ideal e Etc, 

# **OBJETIVOS**

1. Certificar-se de que todas as mecânicas do jogo estão em pleno funcionamento (Plantio, colheita, uso de máquinas, etc.).   
2. Garantir que as mensagens(Caixas de texto), sobre os elementos educativos e informativos estão corretos.  
3. Garantir que as caixas de texto apareçam em momentos certos.  
4. Avaliar as respostas do sistema a partir das ações do jogador como plantar em um solo não preparado.  
5. Testar a progressão do jogador e os ciclos de cultivo.

# **ESCOPO DE TESTE**

* Teste das Ações principais (Andar, Interações com Npcs, Uso das ferramentas, Etc.).  
* Teste de UI  
* Teste de Performance Básica  
* Teste dos Conteúdos educativos (Certificar-se de que as informações estão corretas e legíveis.).

# **CRITÉRIOS DE ACEITAÇÃO** 

* O jogador deve conseguir realizar todas as etapas do ciclo agrícola: preparo do solo, plantio da semente, regar e colher.  
* As informações das caixas de texto devem estar de forma clara e contextualizadas.  
* O jogo responde às entradas de maneira correta como o jogador plantar em solo inadequado.  
* Não ocorrer travamentos durante a jogabilidade.  
* A interface deve permanecer estável (Jogador deve se manter dentro do enquadramento de tela e permanecer dentro do mapa do jogo.).  
* Algumas ações ambientais negativas como (queimar algo ou poluir a água e o solo), afetam visivelmente as plantas e disparam as mensagens de aviso para o jogador.

# **AMBIENTE DE TESTE** 

* Plataforma (MacOs, Linux Ubuntu).  
* Ambiente de Desenvolvimento (Visual Studio Code, Pygame).

# **TIPOS DE TESTE** 

**Tipo de Teste                                                            Descrição**

| Funcional | Verificar se as Funcionalidades estão Operando de maneira correta |
| :---- | :---- |
| Interface UI | Certificar-se de que os elementos da interface estão acessíveis e usuais |
| Educacional | Verificar se todas as Caixas de texto serão apresentadas ao jogador no momento certo |
| Conteúdo | Verificar todas as informações das Caixas de texto que serão apresentadas ao jogador |
| Teste de Fluxo do Jogo | Verificar se a progressão do jogador no ciclo das tarefas está fluindo de maneira  correta |
| Teste de Estresse | Ver como o jogo se comporta caso o jogador sobrecarregue demais o jogo (Inserindo muitas plantas ou contratando muitos trabalhadores) |
| Teste de Erro | Ver como o sistema responde a alguns comportamentos do jogador |
| Teste de compatibilidade | Testar em dispositivos diferentes e em diferentes resoluções |
| Teste de acompanhamento | Câmera fazer acompanhamento do jogador ao movimentar-se pelo mapa  |

# **CASOS DE TESTE** 

**ID                   Caso de Teste                                                                Resultado Esperado**

| CT01 | Jogador planta no solo certo | Planta cresce normalmente com rendimento bom |
| :---- | :---- | :---- |
| CT02 | Jogador planta no solo errado | Planta não pode ser plantada então exibe mensagem de erro |
| CT03 | Jogador aplica agrotóxico duvidoso | Planta morre e aparece uma mensagem de erro de solo danificado |
| CT04 | Jogador aplica agrotóxico supervisionado | Planta cresce saudável e com rendimento melhorado |
| CT05 | Jogador realiza uma queimada | Solo se torna ruim pois foi danificado, jogo exibe mensagem de problema ambiental |
| CT06 | Jogador contrata trabalhador | trabalhador começa a executar tarefas corretamente |
| CT07 | Exibe informações educativas ao plantar | Texto com as informações aparece para o jogador  |
| CT08 | Jogador compra sementes de uma época errada do ano | Texto de advertência aparece para o jogador informando as causas da ação |
| CT09 | Jogador se esquece de regar as plantas | Plantas não crescem e morrem, mensagem informando a morte das plantas aparece para o jogador |
| CT10 | jogador concluiu o seu primeiro ciclo de cultivo | Exibe uma mensagem de parabenização para o jogador |

# **RISCOS IDENTIFICADOS** 

* Jogador ignorar as mensagens educativas por falta de destaque nas mensagens.  
* Bugs na mecânica do solo que podem ocasionar atrasos.  
* Eventos ambientais como (queimadas e acúmulo de lixo) não aplicam o impacto de forma correta.   
* Jogador ignorar tutorial do jogo e sair andando livremente antes da conclusão.  
* Falta de colisão em alguns objetos pelo mapa como cercas e pedras.

# **CRONOGRAMA DE TESTES**

**Fases                                                                Data de Início                       Data de Finalização**

| Planejamento dos testes | 00/09/2025 | 00/00/2025 |
| :---- | :---- | :---- |
| Execução dos testes Manuais | 00/09/2025 | 00/00/2025 |
| Teste de Regressão | 00/09/2025 | 00/00/2025 |
| Teste de Avaliação por terceiros | 00/09/2025 | 00/00/2025 |
| Registro de correção dos Bugs | 00/09/2025 | 00/00/2025 |

# **CRITÉRIOS DE SAÍDA**

* Todos os casos de teste críticos e de alta prioridade passaram nos testes.  
* Jogo jogável e fluido do início ao fim sem erros que causem bloqueios.  
* Gerar um feedback educativo e funcional que cause atração em vários pontos esperados.  
* Bugs críticos resolvidos e informados para melhor identificação em projetos futuros.  
* Bugs Médios e leves parassem nos testes ou estarem em um nível aceitável de acordo com a opinião do docente.  
* Jogo ser leve para que possa ser utilizado em diferentes máquinas.   
* Todos os botões de comando, telas de informações e menus funcionam de maneira correta.  
* As mensagens educativas sobre meio ambiente e uso dos agrotóxicos ou danos ambientais que venham a ocorrer sejam exibidas.

