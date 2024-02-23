from openai import OpenAI
from pydub import AudioSegment

import os
import time
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

# Acessar variáveis de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")




def salvar_transcricao(texto_transcrito, nome_arquivo_saida):
    with open(nome_arquivo_saida, "w") as arquivo_saida:
        arquivo_saida.write(texto_transcrito)

# Função para transcrever áudio usando a API Whisper
def ai_transcribe(audio_path, model="whisper-1"):
    if audio_path is not None and audio_path != "None":
        audio = AudioSegment.from_file(audio_path)
        # Reduz a taxa de amostragem para 16kHz (arquivo mais leve)
        audio = audio.set_frame_rate(16000)
        
        # Crie um nome de arquivo temporário para salvar o arquivo MP3 localmente
        temp_mp3_filename = "temp_mp3_file.mp3"
        audio.export(temp_mp3_filename, format="mp3")

        # Leia o arquivo MP3 localmente
        with open(temp_mp3_filename, "rb") as temp_mp3:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=temp_mp3, 
                response_format="text"
            )
        os.remove(temp_mp3_filename)

        if isinstance(transcript, list):
            transcript = ', '.join(transcript)
        return transcript
    return "Este vídeo não contém áudio"

def processar_videos_pasta(pasta):
    # Lista todos os arquivos na pasta
    arquivos_na_pasta = os.listdir(pasta)
    
    # Filtra apenas os arquivos de vídeo
    videos = [arquivo for arquivo in arquivos_na_pasta if arquivo.lower().endswith(('.mp4', '.avi', '.mkv', '.mp3'))]
    for video in tqdm(videos, desc='Transcrevendo vídeos'):
        nome_arquivo_transcricao = os.path.splitext(video)[0] + ".txt"
        texto_transcrito = ai_transcribe(os.path.join(pasta, video))
        resumo = resumir_ai(texto_transcrito)
        salvar_transcricao(resumo, nome_arquivo_transcricao, nome_arquivo_transcricao)

def resumir_ai(conteudo, arquivo_titulo):
    prompt = f"""
            O título da palestra deve ser extraído do nome do arquivo a seguir, retirando a extensão .txt: {arquivo_titulo}"
            O conteúdo da palestra é o seguinte: 
            {conteudo.read()}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", #"gpt-4-1106-preview", 
        response_format={ "type": "text" },
        messages=[ {"role": "system", "content": """
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


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Aqui eu baixei os vídeos com outro script e os coloquei na pasta abaixo, então nesse script eu apenas o processo
    # processar_videos_pasta('NRF2024/NRF 2024 Exhibitor Big Ideas')
    print(os.getenv("OPENAI_TOKEN"))
    print(os.getenv("NOTION_DATABASE_ID"))

if __name__ == '__main__':
    start_time = time.time()  # Tempo inicial
    main()
    end_time = time.time()  # Tempo final
    total_time = end_time - start_time
    print(f"Tempo de execução do script: {total_time:.2f} segundos")
