import os
import shutil
from pathlib import Path
from datetime import date

from watchdog.events import FileSystemEventHandler

from extensions import extension_paths

def adiciona_data(path: Path):
    """
    Adiciona a data atual para o path destino do arquivo, se o caminho nao existe ele cria a pasta
    """
    path_data = path / f'{date.today().year}' / f'{date.today().month:02d}'
    path_data.mkdir(parents=True, exist_ok=True)
    return path_data

def renomeia_arquivo(origem: Path, destino: Path):
    """
    renomeia o arquivo caso tenha mais de um arquivo com o mesmo nome
    """
    if Path(destino / origem.name).exists():
        incremento = 0
    
        while True:
            incremento += 1
            novo_nome = destino / f'{origem.stem}_{incremento}{origem.suffix}'

            if not novo_nome.exists():
                return novo_nome
    else:
        return destino / origem.nome

class LeitordeEventos(FileSystemEventHandler):
    def __init__(self, pasta: Path, raiz: Path):
        self.pasta = pasta.resolve()
        self.raiz = raiz.resolve()

    def on_modified(self, event):
        print(event.src_path)
        for nome_arquivo in self.pasta.iterdir():
            if nome_arquivo.is_file() and nome_arquivo.suffix.lower() in extension_paths:
                pasta_destino = self.raiz / extension_paths[nome_arquivo.suffix.lower()]
                pasta_destino = adiciona_data(path=pasta_destino)
                pasta_destino = renomeia_arquivo(source=nome_arquivo, pasta_destino=pasta_destino)
                shutil.move(src=nome_arquivo, dst=pasta_destino)
