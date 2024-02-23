Esse script Baixa e processa vídeos, gerando resumos em português.

Configure as variáveis no .env
OPENAI_TOKEN=
NOTION_DATABASE_ID=
NOTION_TOKEN=

Na função main() do main.py edite a pasta onde estão os seus vídeos:

processar_videos_pasta('path/da/pasta')

Execute o main.py