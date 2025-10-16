import json
import os
import time
from datetime import datetime

class SaveSystem:
    
    SAVE_FILE = "fazenda_save.json"
    
    @staticmethod
    def save_game(dinheiro, sementes, fazenda, terra_adubada=None):
        try:
            tempo_atual = time.time()
            fazenda_serializada = {}
            for posicao, planta in fazenda.items():
                key = f"{posicao[0]},{posicao[1]}"
                tempo_decorrido = tempo_atual - planta['tempo_plantio']
                fazenda_serializada[key] = {
                    'tipo': planta['tipo'],
                    'estagio': planta['estagio'],
                    'tempo_decorrido': tempo_decorrido
                }
            
            # Serializar terra adubada
            terra_adubada_lista = []
            if terra_adubada:
                terra_adubada_lista = [list(pos) for pos in terra_adubada]
            
            dados_save = {
                'dinheiro': dinheiro,
                'sementes': sementes,
                'fazenda': fazenda_serializada,
                'terra_adubada': terra_adubada_lista,
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
                    'tempo_plantio': tempo_plantio
                }
            
            return {
                'dinheiro': dados_save['dinheiro'],
                'sementes': dados_save['sementes'],
                'fazenda': fazenda,
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
