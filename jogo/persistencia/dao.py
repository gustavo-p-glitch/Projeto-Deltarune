import json
import os
import shutil
from jogo import recursos
from abc import ABC, abstractmethod

class DAO(ABC):
    @abstractmethod
    def __init__(self, arquivo: str):
        # Caminho absoluto: antes, rodar o jogo de outra pasta criava JSONs vazios
        # nessa outra pasta e "sumia" com os inimigos/relatórios.
        self.__arquivo = arquivo if os.path.isabs(arquivo) else recursos.dado(arquivo)
        self.__cache = []
        self.carregar()

    @property
    def arquivo(self):
        return self.__arquivo

    @arquivo.setter
    def arquivo(self, arquivo: str):
        self.__arquivo = arquivo

    @property
    def cache(self):
        return self.__cache

    @cache.setter
    def cache(self, cache: list):
        self.__cache = cache

    def carregar(self):
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = []
            self.salvar()
        except json.JSONDecodeError as e:
            # Antes: JSON com erro de digitação -> arquivo sobrescrito com [] e
            # todos os dados perdidos. Agora guarda uma cópia antes de recomeçar.
            backup = self.arquivo + ".corrompido.bak"
            shutil.copyfile(self.arquivo, backup)
            print(f"[aviso] {os.path.basename(self.arquivo)} inválido ({e}). Cópia salva em {backup}")
            self.cache = []
            self.salvar()

    def salvar(self):
        # Escreve num temporário e troca: se o jogo fechar no meio, o original não corrompe.
        temporario = self.arquivo + ".tmp"
        with open(temporario, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=4, ensure_ascii=False)
        os.replace(temporario, self.arquivo)

    def ler(self):
        return self.cache

    def adicionar(self, dados_inimigo):
        self.cache.append(dados_inimigo)
        self.salvar()

    def remover(self, ident, chave='nome'):
        self.cache = [item for item in self.cache
                      if item.get(chave) != ident]
        self.salvar()
