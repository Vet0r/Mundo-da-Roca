import time
import random
from config import TAMANHO_CELULA, LARGURA, ALTURA

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
            self.direcao_patrulha = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
            if self.direcao_patrulha == [0, 0]:
                self.direcao_patrulha = [random.choice([-1, 1]), 0]
    
    def mover_para_alvo(self):
        if not self.alvo_atual:
            return False
        
        alvo_x = self.alvo_atual[0] * TAMANHO_CELULA
        alvo_y = self.alvo_atual[1] * TAMANHO_CELULA
        
        if abs(self.x - alvo_x) > self.velocidade:
            self.x += self.velocidade if self.x < alvo_x else -self.velocidade
        elif abs(self.y - alvo_y) > self.velocidade:
            self.y += self.velocidade if self.y < alvo_y else -self.velocidade
        else:
            return True
        
        return False
    
    def executar_trabalho(self, farm_system, water_system, player):
        tempo_atual = time.time()
        
        if tempo_atual - self.ultimo_trabalho < self.intervalo_trabalho:
            return False
        
        if not self.alvo_atual:
            self.alvo_atual = self.encontrar_proximo_alvo(farm_system, water_system, player)
            
            if not self.alvo_atual:
                self.ativo = False
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
            
            # Se o alvo não é mais válido, limpar e procurar novo na próxima iteração
            if not alvo_valido:
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
                resultado = farm_system.adubar_terra(grid_x, grid_y, water_system)
            
            self.ultimo_trabalho = tempo_atual
            self.alvo_atual = None
            
            return resultado
        
        return False

class WorkerSystem:
    def __init__(self):
        self.trabalhadores = []
        self.tipos_trabalhador = {
            'cultivador': {'nome': 'Cultivador', 'preco': 300, 'descricao': 'Planta sementes'},
            'coletador': {'nome': 'Coletador', 'preco': 300, 'descricao': 'Colhe plantas'},
            'adubador': {'nome': 'Adubador', 'preco': 300, 'descricao': 'Aduba terra'}
        }
    
    def contratar_trabalhador(self, tipo, player, posicao_spawn):
        preco = self.tipos_trabalhador[tipo]['preco']
        
        if player.gastar_dinheiro(preco):
            worker = Worker(tipo, posicao_spawn)
            self.trabalhadores.append(worker)
            return True
        return False
    
    def atualizar_trabalhadores(self, farm_system, water_system, player):
        trabalhadores_inativos = []
        
        for i, worker in enumerate(self.trabalhadores):
            if worker.ativo:
                worker.executar_trabalho(farm_system, water_system, player)
            else:
                trabalhadores_inativos.append(i)
        
        for i in reversed(trabalhadores_inativos):
            print(f"Trabalhador {self.trabalhadores[i].tipo} finalizou o serviço!")
            del self.trabalhadores[i]
    
    def obter_trabalhadores_ativos(self):
        return [(w.tipo, w.x, w.y) for w in self.trabalhadores if w.ativo]
    
    def contar_trabalhadores_por_tipo(self):
        contagem = {'cultivador': 0, 'coletador': 0, 'adubador': 0}
        for worker in self.trabalhadores:
            if worker.ativo:
                contagem[worker.tipo] += 1
        return contagem
    
    def carregar_dados(self, dados_trabalhadores):
        self.trabalhadores = []
        for dado in dados_trabalhadores:
            worker = Worker(dado['tipo'], (dado['x'], dado['y']))
            worker.ativo = dado.get('ativo', True)
            self.trabalhadores.append(worker)
    
    def obter_dados_save(self):
        return [{
            'tipo': w.tipo,
            'x': w.x,
            'y': w.y,
            'ativo': w.ativo
        } for w in self.trabalhadores]
