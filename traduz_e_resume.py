from openai import OpenAI
from pydub import AudioSegment

import os
import time
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

# Acessar variáveis de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))


def salvar_transcricao(texto_transcrito, nome_arquivo_saida):
    with open(nome_arquivo_saida, "w") as arquivo_saida:
        arquivo_saida.write(texto_transcrito)

# Função para transcrever áudio usando a API Whisper
def resumir_ai(arquivo):
    with open(arquivo, "r") as conteudo:
        prompt = f"""
                O título da palestra deve ser extraído do nome do arquivo a seguir, retirando a extensão .txt: {arquivo}"
                O conteúdo da palestra é o seguinte: 
                {conteudo.read()}
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", #"gpt-4-1106-preview", 
            response_format={ "type": "text" },
            messages=[
                {"role": "system", "content": """
O conteúdo a seguir é a transcrição de uma palestra.

Por favor, resuma o conteúdo da palestra, incluindo pontos-chave, insights importantes e exemplos relevantes. Gostaria de uma versão mais detalhada e abrangente do que foi discutido. Eu quero que ao ler o resumo eu possa conversar com alguém que esteve na palestra sobre ela, e a pessoa acredite que eu também a assisti. Caso existam nomes das pessoas que estiverem falando, identificar quem falou o quê.

Estrutura de sua resposta:
[Titulo original da palestra em inglês]
[Titulo traduzido para o português]

[Resumo da palestra]

Principais temas abordados:
1. 
2. 
3. 
4. 
5. 

Palavras mais utilizadas: (desconsiderar palavras comuns do idioma, e não escrever esse parênteses na sua resposta)
1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. """},
                {"role": "user", "content": prompt}
            ]
        )
        # return response.choices[0].message.content + " => "+ response.choices[0].finish_reason + " (total tokens: "+ str(response.usage.total_tokens) +")"
        complemento = " => Atenção: Resposta incompleta" if response.choices[0].finish_reason != "stop" else ""
        return response.choices[0].message.content + complemento

def processa(pasta):
    arquivos_na_pasta = os.listdir(pasta)
    
    # Filtra apenas os arquivos de texto
    videos = [arquivo for arquivo in arquivos_na_pasta if arquivo.lower().endswith(('.txt'))]
    for video in tqdm(videos, desc='Resumindo conteúdos'):
        caminho_completo = os.path.join(pasta, video)
        nome_arquivo_sem_extensao = os.path.splitext(video)[0].replace('_transcricao','')
        # print(caminho_completo)
        texto_transcrito = resumir_ai(caminho_completo)
        salvar_transcricao(texto_transcrito, './processados/' + nome_arquivo_sem_extensao + '.txt')

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    processa('./transcricoes/');

if __name__ == '__main__':
    start_time = time.time()  # Tempo inicial
    main()
    end_time = time.time()  # Tempo final
    total_time = end_time - start_time
    print(f"Tempo de execução do script: {total_time:.2f} segundos")
