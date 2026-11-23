import json
from jogo import recursos


class AtaqueDAO:
    def __init__(self, caminho_arquivo="attacks.json"):
        self.cache_todos_ataques = self.carregar_arquivo(recursos.dado(caminho_arquivo))

    def carregar_arquivo(self, caminho_json: str) -> dict:
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            # Antes o erro era engolido e todo inimigo caía no ataque fallback sem aviso.
            print(f"[aviso] attacks.json inválido: {e}")
            return {}

    def carregar_ataques_por_inimigo(self, nome_inimigo: str):
        for nome, dados in self.cache_todos_ataques.items():
            if nome.lower() == nome_inimigo.lower():
                return dados.get("padroes_ataque", [])

        return [{
            "nome": "AtaqueFallback",
            "duracao_ms": 2000,
            "cor_alma": "vermelho",
            "eventos": [
                {"tempo_ms": 0, "tipo": "definir_mensagem", "texto": f"Ataques para {nome_inimigo} não encontrados!"}]
        }]