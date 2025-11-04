import json
import os
import time
from datetime import datetime

class SaveSystem:
    SAVE_FILE = "fazenda_save.json"
    
    @staticmethod
    def save_game(player, farm_system, water_system, worker_system):
        try:
            dados_farm = farm_system.obter_dados_save()
            dados_water = water_system.obter_dados_save()
            dados_workers = worker_system.obter_dados_save()
            
            dados_save = {
                'dinheiro': player.dinheiro,
                'sementes': player.sementes,
                'fazenda': dados_farm['fazenda'],
                'terra_adubada': dados_farm['terra_adubada'],
                'buracos_com_agua': dados_water['buracos_com_agua'],
                'terra_aguada': dados_water['terra_aguada'],
                'trabalhadores': dados_workers,
                'data_save': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(SaveSystem.SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(dados_save, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar jogo: {e}")
            return False
    
    @staticmethod
    def load_game():
        try:
            if not os.path.exists(SaveSystem.SAVE_FILE):
                return None
            
            with open(SaveSystem.SAVE_FILE, 'r', encoding='utf-8') as f:
                dados_save = json.load(f)
            
            tempo_atual = time.time()
            fazenda = {}
            for key, planta in dados_save['fazenda'].items():
                pos_x, pos_y = map(int, key.split(','))
                
                if 'tempo_decorrido' in planta:
                    tempo_plantio = tempo_atual - planta['tempo_decorrido']
                else:
                    tempo_plantio = planta.get('tempo_plantio', tempo_atual)
                
                fazenda[(pos_x, pos_y)] = {
                    'tipo': planta['tipo'],
                    'estagio': planta['estagio'],
                    'tempo_plantio': tempo_plantio,
                    'estragada': planta.get('estragada', False),
                    'fator_crescimento': planta.get('fator_crescimento', 1.0)
                }
            
            return {
                'dinheiro': dados_save['dinheiro'],
                'sementes': dados_save['sementes'],
                'fazenda': fazenda,
                'terra_adubada': dados_save.get('terra_adubada', []),
                'buracos_com_agua': dados_save.get('buracos_com_agua', []),
                'terra_aguada': dados_save.get('terra_aguada', []),
                'trabalhadores': dados_save.get('trabalhadores', []),
                'data_save': dados_save.get('data_save', 'Desconhecida')
            }
        except Exception as e:
            print(f"Erro ao carregar jogo: {e}")
            return None
    
    @staticmethod
    def save_exists():
        return os.path.exists(SaveSystem.SAVE_FILE)
    
    @staticmethod
    def get_save_info():
        try:
            if not SaveSystem.save_exists():
                return None
            
            with open(SaveSystem.SAVE_FILE, 'r', encoding='utf-8') as f:
                dados_save = json.load(f)
            
            return {
                'dinheiro': dados_save['dinheiro'],
                'data_save': dados_save.get('data_save', 'Desconhecida'),
                'total_plantas': len(dados_save.get('fazenda', {}))
            }
        except:
            return None
    
    @staticmethod
    def delete_save():
        try:
            if os.path.exists(SaveSystem.SAVE_FILE):
                os.remove(SaveSystem.SAVE_FILE)
            return True
        except:
            return False
