from pathlib import Path
from time import sleep

from watchdog.observers import Observer

from LeitordeEvento import LeitordeEventos

print("começou")
if __name__ == '__main__':
    pasta_download = Path.home() / 'Downloads'
    raiz_destino = Path.home() / 'Downloads' / 'yohan'
    leitor_eventos = LeitordeEventos(pasta=pasta_download, raiz=raiz_destino)

    observer = Observer()
    observer.schedule(leitor_eventos, f'{pasta_download}', recursive=True)
    observer.start

    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()   
