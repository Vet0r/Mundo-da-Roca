import time
import random
from config import TAMANHO_CELULA, LARGURA, ALTURA


class WorkerConsciousness:
    """
    Sistema de consciência para trabalhadores.
    Gerencia a alocação de tarefas garantindo que dois trabalhadores
    não trabalhem na mesma tarefa simultaneamente.
    """
    def __init__(self):
        self.tarefas_alocadas = {}  # {(grid_x, grid_y): worker_id}
        self.worker_id_counter = 0
    
    def gerar_id_worker(self):
        self.worker_id_counter += 1
        return self.worker_id_counter
    
    def alocar_tarefa(self, posicao, worker_id):
        """Aloca uma tarefa para um worker específico"""
        if posicao not in self.tarefas_alocadas:
            self.tarefas_alocadas[posicao] = worker_id
            return True
        return False
    
    def desalocar_tarefa(self, posicao, worker_id):
        """Desaloca uma tarefa se pertencer ao worker"""
        if self.tarefas_alocadas.get(posicao) == worker_id:
            del self.tarefas_alocadas[posicao]
            return True
        return False
    
    def tarefa_esta_alocada(self, posicao):
        """Verifica se uma tarefa já está alocada para outro worker"""
        return posicao in self.tarefas_alocadas
    
    def obter_tarefas_do_worker(self, worker_id):
        """Retorna todas as tarefas alocadas para um worker"""
        return [pos for pos, wid in self.tarefas_alocadas.items() if wid == worker_id]
    
    def limpar_tarefas_worker(self, worker_id):
        """Remove todas as tarefas de um worker (para quando ele é removido)"""
        posicoes_para_remover = [pos for pos, wid in self.tarefas_alocadas.items() if wid == worker_id]
        for pos in posicoes_para_remover:
            del self.tarefas_alocadas[pos]


class Worker:
    def __init__(self, tipo, posicao_inicial):
        self.tipo = tipo
        self.x = posicao_inicial[0]
        self.y = posicao_inicial[1]
        self.ativo = True
        self.ultimo_trabalho = time.time()
        self.intervalo_trabalho = 0.5
        self.alvo_atual = None
        self.velocidade = 12
        self.tempo_sem_trabalho = 0
        self.ultimo_check = time.time()
        self.direcao_patrulha = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.ultimo_pagamento = time.time()
        self.intervalo_pagamento = 20  # 20 segundos
        self.custo_manutencao = 5  # $5 por pagamento
        self.worker_id = None  # Será definido quando criado no WorkerSystem
    
    def encontrar_proximo_alvo(self, farm_system, water_system, player):
        grid_x = int(self.x // TAMANHO_CELULA)
        grid_y = int(self.y // TAMANHO_CELULA)
        
        if self.tipo == 'cultivador':
            return self._encontrar_terra_para_plantar(farm_system, water_system, grid_x, grid_y)
        elif self.tipo == 'coletador':
            return self._encontrar_planta_para_colher(farm_system, grid_x, grid_y)
        elif self.tipo == 'adubador':
            return self._encontrar_terra_para_adubar(farm_system, water_system, grid_x, grid_y)
        return None
    
    def encontrar_proximo_alvo_consciente(self, farm_system, water_system, player, worker_consciousness):
        """
        Dinâmica consciente de decisão:
        1. Encontrar o tile mais próximo com atividade
        2. Verificar se não há ninguém que já vai fazer essa tarefa
        3. Caso haja, volta para 1. Caso não, aloca e faz a tarefa
        4. Após fazer a tarefa, repete passo 1
        """
        grid_x = int(self.x // TAMANHO_CELULA)
        grid_y = int(self.y // TAMANHO_CELULA)
        
        if self.tipo == 'cultivador':
            alvos = self._gerar_lista_terra_para_plantar(farm_system, water_system, grid_x, grid_y)
        elif self.tipo == 'coletador':
            alvos = self._gerar_lista_planta_para_colher(farm_system, grid_x, grid_y)
        elif self.tipo == 'adubador':
            alvos = self._gerar_lista_terra_para_adubar(farm_system, water_system, grid_x, grid_y)
        else:
            return None
        
        # Passo 1 & 2: Encontrar o tile mais próximo que não está alocado
        for distancia, posicao in alvos:
            # Passo 2: Verificar se ninguém já vai fazer essa tarefa
            if not worker_consciousness.tarefa_esta_alocada(posicao):
                # Passo 3: Alocar a tarefa para este worker
                if worker_consciousness.alocar_tarefa(posicao, self.worker_id):
                    return posicao
        
        # Se nenhuma tarefa disponível foi encontrada
        return None
    
    def _encontrar_terra_para_plantar(self, farm_system, water_system, worker_x, worker_y):
        alvos_proximos = []
        for pos in farm_system.terra_adubada:
            if pos not in farm_system.fazenda:
                distancia = abs(pos[0] - worker_x) + abs(pos[1] - worker_y)
                alvos_proximos.append((distancia, pos))
        
        if alvos_proximos:
            alvos_proximos.sort(key=lambda x: x[0])
            return alvos_proximos[0][1]
        return None
    
    def _encontrar_planta_para_colher(self, farm_system, worker_x, worker_y):
        alvos_proximos = []
        for pos, planta in farm_system.fazenda.items():
            if planta['estagio'] == 6 and not planta.get('estragada', False):
                distancia = abs(pos[0] - worker_x) + abs(pos[1] - worker_y)
                alvos_proximos.append((distancia, pos))
        
        if alvos_proximos:
            alvos_proximos.sort(key=lambda x: x[0])
            return alvos_proximos[0][1]
        return None
    
    def _encontrar_terra_para_adubar(self, farm_system, water_system, worker_x, worker_y):
        alvos_proximos = []
        for pos in water_system.terra_aguada:
            if (pos not in farm_system.terra_adubada and 
                pos not in farm_system.fazenda and
                pos not in water_system.buracos_com_agua):
                distancia = abs(pos[0] - worker_x) + abs(pos[1] - worker_y)
                alvos_proximos.append((distancia, pos))
        
        if alvos_proximos:
            alvos_proximos.sort(key=lambda x: x[0])
            return alvos_proximos[0][1]
        return None
    
    def _gerar_lista_terra_para_plantar(self, farm_system, water_system, worker_x, worker_y):
        """Retorna lista ordenada por distância de terras para plantar"""
        alvos_proximos = []
        for pos in farm_system.terra_adubada:
            if pos not in farm_system.fazenda:
                distancia = abs(pos[0] - worker_x) + abs(pos[1] - worker_y)
                alvos_proximos.append((distancia, pos))
        
        alvos_proximos.sort(key=lambda x: x[0])
        return alvos_proximos
    
    def _gerar_lista_planta_para_colher(self, farm_system, worker_x, worker_y):
        """Retorna lista ordenada por distância de plantas para colher"""
        alvos_proximos = []
        for pos, planta in farm_system.fazenda.items():
            if planta['estagio'] == 6 and not planta.get('estragada', False):
                distancia = abs(pos[0] - worker_x) + abs(pos[1] - worker_y)
                alvos_proximos.append((distancia, pos))
        
        alvos_proximos.sort(key=lambda x: x[0])
        return alvos_proximos
    
    def _gerar_lista_terra_para_adubar(self, farm_system, water_system, worker_x, worker_y):
        """Retorna lista ordenada por distância de terras para adubar"""
        alvos_proximos = []
        for pos in water_system.terra_aguada:
            if (pos not in farm_system.terra_adubada and 
                pos not in farm_system.fazenda and
                pos not in water_system.buracos_com_agua):
                distancia = abs(pos[0] - worker_x) + abs(pos[1] - worker_y)
                alvos_proximos.append((distancia, pos))
        
        alvos_proximos.sort(key=lambda x: x[0])
        return alvos_proximos
    
    def patrulhar(self):
        self.x += self.direcao_patrulha[0] * self.velocidade
        self.y += self.direcao_patrulha[1] * self.velocidade
        
        if self.x < 0 or self.x > LARGURA - 40:
            self.direcao_patrulha[0] *= -1
            self.x = max(0, min(self.x, LARGURA - 40))
        
        if self.y < 0 or self.y > ALTURA - 40:
            self.direcao_patrulha[1] *= -1
            self.y = max(0, min(self.y, ALTURA - 40))
        
        if random.random() < 0.02:
            # Permite movimento em 8 direções (incluindo diagonais)
            self.direcao_patrulha = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
            # Se não tiver movimento, escolhe uma diagonal aleatória
            if self.direcao_patrulha == [0, 0]:
                self.direcao_patrulha = [random.choice([-1, 1]), random.choice([-1, 1])]
    
    def mover_para_alvo(self):
        if not self.alvo_atual:
            return False
        
        alvo_x = self.alvo_atual[0] * TAMANHO_CELULA
        alvo_y = self.alvo_atual[1] * TAMANHO_CELULA
        
        # Calcular distância em X e Y
        dist_x = abs(self.x - alvo_x)
        dist_y = abs(self.y - alvo_y)
        
        # Se chegou ao alvo
        if dist_x <= self.velocidade and dist_y <= self.velocidade:
            self.x = alvo_x
            self.y = alvo_y
            return True
        
        # Movimento na diagonal
        if dist_x > self.velocidade:
            self.x += self.velocidade if self.x < alvo_x else -self.velocidade
        
        if dist_y > self.velocidade:
            self.y += self.velocidade if self.y < alvo_y else -self.velocidade
        
        return False
    
    def executar_trabalho(self, farm_system, water_system, player, worker_consciousness):
        tempo_atual = time.time()
        
        # Sistema de pagamento: cobrar manutenção a cada 20 segundos
        if tempo_atual - self.ultimo_pagamento >= self.intervalo_pagamento:
            if player.dinheiro >= self.custo_manutencao:
                player.gastar_dinheiro(self.custo_manutencao)
                self.ultimo_pagamento = tempo_atual
                print(f"Trabalhador {self.tipo} recebeu pagamento de ${self.custo_manutencao}")
            else:
                # Se não tiver dinheiro, trabalhador para de trabalhar mas não é removido
                self.ativo = False
                print(f"Trabalhador {self.tipo} parou de trabalhar por falta de pagamento!")
                return False
        
        if tempo_atual - self.ultimo_trabalho < self.intervalo_trabalho:
            return False
        
        if not self.alvo_atual:
            # Usar a dinâmica consciente para encontrar próximo alvo
            self.alvo_atual = self.encontrar_proximo_alvo_consciente(
                farm_system, water_system, player, worker_consciousness
            )
            
            if not self.alvo_atual:
                # Não tem trabalho disponível
                return False
        
        if self.mover_para_alvo():
            grid_x, grid_y = self.alvo_atual
            resultado = False
            
            # Validar se o alvo ainda é válido antes de executar
            alvo_valido = False
            if self.tipo == 'cultivador':
                alvo_valido = ((grid_x, grid_y) in farm_system.terra_adubada and 
                              (grid_x, grid_y) not in farm_system.fazenda)
            elif self.tipo == 'coletador':
                planta = farm_system.fazenda.get((grid_x, grid_y))
                alvo_valido = planta is not None and planta['estagio'] == 6 and not planta.get('estragada', False)
            elif self.tipo == 'adubador':
                alvo_valido = ((grid_x, grid_y) in water_system.terra_aguada and
                              (grid_x, grid_y) not in farm_system.terra_adubada and
                              (grid_x, grid_y) not in farm_system.fazenda and
                              (grid_x, grid_y) not in water_system.buracos_com_agua)
            
            # Se o alvo não é mais válido, desalocar e procurar novo na próxima iteração
            if not alvo_valido:
                worker_consciousness.desalocar_tarefa(self.alvo_atual, self.worker_id)
                self.alvo_atual = None
                return False
            
            # Executar a ação
            if self.tipo == 'cultivador':
                if player.sementes.get(player.semente_selecionada, 0) > 0:
                    resultado = farm_system.plantar_semente(grid_x, grid_y, 
                                                           player.semente_selecionada, 
                                                           player.sementes, water_system)
            elif self.tipo == 'coletador':
                colheu, valor = farm_system.colher_planta(grid_x, grid_y)
                if colheu:
                    player.adicionar_dinheiro(valor)
                    resultado = True
            elif self.tipo == 'adubador':
                resultado, _ = farm_system.adubar_terra(grid_x, grid_y, water_system, player)
            
            # Desalocar a tarefa após tentativa de execução
            worker_consciousness.desalocar_tarefa(self.alvo_atual, self.worker_id)
            self.ultimo_trabalho = tempo_atual
            self.alvo_atual = None
            
            return resultado
        
        return False


class WorkerSystem:
    def __init__(self):
        self.trabalhadores = []
        self.tipos_trabalhador = {
            'cultivador': {'nome': 'Cultivador', 'preco': 300, 'descricao': 'Planta sementes', 'custo_manutencao': 1},
            'coletador': {'nome': 'Coletador', 'preco': 300, 'descricao': 'Colhe plantas', 'custo_manutencao': 1},
            'adubador': {'nome': 'Adubador', 'preco': 300, 'descricao': 'Aduba terra', 'custo_manutencao': 1}
        }
        self.worker_consciousness = WorkerConsciousness()
    
    def contratar_trabalhador(self, tipo, player, posicao_spawn):
        preco = self.tipos_trabalhador[tipo]['preco']
        
        if player.gastar_dinheiro(preco):
            worker = Worker(tipo, posicao_spawn)
            worker.worker_id = self.worker_consciousness.gerar_id_worker()
            self.trabalhadores.append(worker)
            return True
        return False
    
    def atualizar_trabalhadores(self, farm_system, water_system, player):
        for worker in self.trabalhadores:
            if worker.ativo:
                worker.executar_trabalho(farm_system, water_system, player, self.worker_consciousness)
            else:
                # Tentar reativar trabalhador se houver dinheiro
                tempo_atual = time.time()
                if tempo_atual - worker.ultimo_pagamento >= worker.intervalo_pagamento:
                    if player.dinheiro >= worker.custo_manutencao:
                        worker.ativo = True
                        print(f"Trabalhador {worker.tipo} voltou ao trabalho!")
    
    def remover_trabalhador(self, index):
        """Remove um trabalhador e limpa suas tarefas alocadas"""
        if 0 <= index < len(self.trabalhadores):
            worker = self.trabalhadores[index]
            self.worker_consciousness.limpar_tarefas_worker(worker.worker_id)
            self.trabalhadores.pop(index)
            return True
        return False
    
    def obter_trabalhadores_ativos(self):
        # Retorna todos os trabalhadores, não apenas os ativos
        return [(w.tipo, w.x, w.y, w.ativo) for w in self.trabalhadores]
    
    def contar_trabalhadores_por_tipo(self):
        contagem_ativos = {'cultivador': 0, 'coletador': 0, 'adubador': 0}
        contagem_total = {'cultivador': 0, 'coletador': 0, 'adubador': 0}
        for worker in self.trabalhadores:
            contagem_total[worker.tipo] += 1
            if worker.ativo:
                contagem_ativos[worker.tipo] += 1
        return contagem_ativos, contagem_total
    
    def carregar_dados(self, dados_trabalhadores):
        self.trabalhadores = []
        self.worker_consciousness = WorkerConsciousness()
        tempo_atual = time.time()
        for dado in dados_trabalhadores:
            worker = Worker(dado['tipo'], (dado['x'], dado['y']))
            worker.ativo = dado.get('ativo', True)
            worker.worker_id = self.worker_consciousness.gerar_id_worker()
            # Restaurar tempo de último pagamento
            worker.ultimo_pagamento = dado.get('ultimo_pagamento', tempo_atual)
            self.trabalhadores.append(worker)
    
    def obter_dados_save(self):
        return [{
            'tipo': w.tipo,
            'x': w.x,
            'y': w.y,
            'ativo': w.ativo,
            'ultimo_pagamento': w.ultimo_pagamento
        } for w in self.trabalhadores]
