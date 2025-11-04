import time
import random
from config import TIPOS_SEMENTE, POCO_POS

class FarmSystem:
    def __init__(self):
        self.fazenda = {}
        self.terra_adubada = set()
    
    def adubar_terra(self, grid_x, grid_y, water_system):
        posicao = (grid_x, grid_y)
        if (posicao in water_system.terra_aguada and
            posicao not in self.fazenda and 
            posicao not in self.terra_adubada and
            posicao not in water_system.buracos_com_agua and
            posicao != POCO_POS and
            posicao != (POCO_POS[0] + 1, POCO_POS[1]) and
            posicao != (POCO_POS[0], POCO_POS[1] + 1) and
            posicao != (POCO_POS[0] + 1, POCO_POS[1] + 1)):
            self.terra_adubada.add(posicao)
            return True
        return False
    
    def plantar_semente(self, grid_x, grid_y, tipo, sementes, water_system):
        posicao = (grid_x, grid_y)
        if (posicao not in self.fazenda and 
            sementes[tipo] > 0 and 
            posicao in self.terra_adubada and
            posicao not in water_system.buracos_com_agua and
            posicao != POCO_POS and
            posicao != (POCO_POS[0] + 1, POCO_POS[1]) and
            posicao != (POCO_POS[0], POCO_POS[1] + 1) and
            posicao != (POCO_POS[0] + 1, POCO_POS[1] + 1)):
            fator_crescimento = random.uniform(0.7, 1.3)
            
            self.fazenda[posicao] = {
                'tipo': tipo,
                'estagio': 1,
                'tempo_plantio': time.time(),
                'estragada': False,
                'fator_crescimento': fator_crescimento
            }
            sementes[tipo] -= 1
            return True
        return False
    
    def colher_planta(self, grid_x, grid_y):
        posicao = (grid_x, grid_y)
        if posicao in self.fazenda:
            planta = self.fazenda[posicao]
            if planta['estagio'] == 6:
                valor = TIPOS_SEMENTE[planta['tipo']]['valor_colheita']
                del self.fazenda[posicao]
                if posicao in self.terra_adubada:
                    self.terra_adubada.discard(posicao)
                return True, valor
        return False, 0
    
    def remover_planta_podre(self, grid_x, grid_y):
        posicao = (grid_x, grid_y)
        if posicao in self.fazenda:
            planta = self.fazenda[posicao]
            if planta['estagio'] == 7 or planta.get('estragada', False):
                del self.fazenda[posicao]
                if posicao in self.terra_adubada:
                    self.terra_adubada.discard(posicao)
                return True
        return False
    
    def atualizar_plantas(self, water_system):
        tempo_atual = time.time()
        plantas_para_remover = []
        
        for posicao, planta in self.fazenda.items():
            tempo_decorrido = tempo_atual - planta['tempo_plantio']
            tipo = planta['tipo']
            tempo_crescimento_base = TIPOS_SEMENTE[tipo]['tempo_crescimento']
            
            fator_crescimento = planta.get('fator_crescimento', 1.0)
            tempo_crescimento = tempo_crescimento_base * fator_crescimento
            
            if posicao not in water_system.terra_aguada and not planta.get('estragada', False):
                planta['estragada'] = True
                planta['estagio'] = 7
                continue
            
            if not planta.get('estragada', False):
                estagio_calculado = int(tempo_decorrido / tempo_crescimento) + 1
                
                if estagio_calculado >= 6:
                    tempo_ate_estagio_6 = tempo_crescimento * 5
                    tempo_extra = tempo_decorrido - tempo_ate_estagio_6
                    
                    if tempo_extra < tempo_crescimento * 3:
                        novo_estagio = 6
                    else:
                        novo_estagio = 7
                else:
                    novo_estagio = estagio_calculado
                
                planta['estagio'] = novo_estagio
                
                if novo_estagio == 7 and tempo_decorrido > tempo_crescimento * 15:
                    plantas_para_remover.append(posicao)
        
        for posicao in plantas_para_remover:
            del self.fazenda[posicao]
    
    def carregar_dados(self, fazenda, terra_adubada):
        self.fazenda = fazenda
        self.terra_adubada = set(tuple(pos) for pos in terra_adubada)
    
    def obter_dados_save(self):
        tempo_atual = time.time()
        fazenda_serializada = {}
        for posicao, planta in self.fazenda.items():
            key = f"{posicao[0]},{posicao[1]}"
            tempo_decorrido = tempo_atual - planta['tempo_plantio']
            fazenda_serializada[key] = {
                'tipo': planta['tipo'],
                'estagio': planta['estagio'],
                'tempo_decorrido': tempo_decorrido,
                'estragada': planta.get('estragada', False),
                'fator_crescimento': planta.get('fator_crescimento', 1.0)
            }
        
        return {
            'fazenda': fazenda_serializada,
            'terra_adubada': [list(pos) for pos in self.terra_adubada]
        }
