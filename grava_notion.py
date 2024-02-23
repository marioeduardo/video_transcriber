import notion
import os
import time
from datetime import datetime, timezone
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

# Acessar variáveis de ambiente
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def processa(pasta):
    arquivos_na_pasta = os.listdir(pasta)

    # Filtra apenas os arquivos de texto
    videos = [arquivo for arquivo in arquivos_na_pasta if arquivo.lower().endswith(('.txt'))]
    for video in tqdm(videos, desc='Cadastrando no Notion'):
        caminho_completo = os.path.join(pasta, video)
        nome_arquivo_sem_extensao = os.path.splitext(video)[0]

        with open(caminho_completo, "r") as arquivo_raw:
            conteudo = arquivo_raw.read()
            body = notion.Body()
            body.add('heading_1', nome_arquivo_sem_extensao)
            body.add('paragraph', conteudo)

            published_date = datetime.now().astimezone(timezone.utc).isoformat()
            data = {
                        "Titulo":{
                            "title":[
                                {
                                    "text":{ "content":nome_arquivo_sem_extensao }
                                }
                            ]
                        }
            }

            payload = {"parent": {"database_id": DATABASE_ID}, "properties": data, **body.to_json()}
            print('\n --')
            print(payload)
            notion.create_page_withbody(payload)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')    
    # notion.get_pages(DATABASE_ID, None, '.log_page.json')
    # testa()
    processa('./processados/');

if __name__ == '__main__':
    start_time = time.time()  # Tempo inicial
    main()
    end_time = time.time()  # Tempo final
    total_time = end_time - start_time
    print(f"Tempo de execução do script: {total_time:.2f} segundos")
