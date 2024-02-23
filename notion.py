from datetime import datetime, timezone
import requests

from dotenv import load_dotenv
load_dotenv()

# Acessar variáveis de ambiente
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# NOTION_TOKEN = "secret_2zcIGqd...."  # Monday Backup
# DATABASE_ID = "708a387729d5418ba4847603b..."  # Demandas Jurídicas

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

class Body:
    def __init__(self):
        self.blocks = []

    def add(self, type_, content):
        # self.blocks.append({"object": "block", "type": type_, type_: {"text": [{"type": "text", "text": {"content": content}}]}})
        self.blocks.append({"object": "block", "type": type_, type_: { "rich_text": [{ "type": "text", "text": { "content": content } }] }})

    def src(self):
        return self.blocks

    def to_json(self):
        return {"children": self.blocks}

def create_page(DATABASE_ID: str, data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data }
    res = requests.post(create_url, headers=headers, json=payload)
    return res

def create_page_withbody(payload):
    create_url = "https://api.notion.com/v1/pages"
    res = requests.post(create_url, headers=headers, json=payload)
    print(res)
    return res



def create_databasepage(DATABASE_ID: str, data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"page_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res


def create_database(data: dict):
    create_url = "https://api.notion.com/v1/databases/"
    payload = data
    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res


def create_comment(page_id: str, str_comment: str):
    comments_url = "https://api.notion.com/v1/comments"

    payload = {"parent": {"page_id": page_id},
               "rich_text": [{"text": {"content": str_comment}}]
               }

    res = requests.post(comments_url, headers=headers, json=payload)
    return res


def create_comment_reply(discussion_id: str, str_comment: str):
    comments_url = "https://api.notion.com/v1/comments"

    payload = {"discussion_id": discussion_id,
               "rich_text": [{"text": {"content": str_comment}}]
               }

    res = requests.post(comments_url, headers=headers, json=payload)
    return res


def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res


def get_pages(DATABASE_ID: str, num_pages=None, logfile=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file

    if not logfile is None:
        import json
        with open(logfile, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)
    return res

# Exemplos de uso

# if __name__ == '__main__':
#     BOARDS = get_pages("824ab59ce6354e718785fee0728b9a7d")
#     for page in BOARDS:
#         page_id = page["id"]
#         props = page["properties"]
#         db_importar = props["Importar"]["checkbox"]
#         db_nome = props["Nome"]["title"][0]["text"]["content"]
#         db_link = props["Link"]["rich_text"][0]["text"]["content"]
#         db_ID = props["ID"]["rich_text"][0]["text"]["content"]
#         db_Subtasks = props["Subtasks"]["rich_text"][0]["text"]["content"]
#         if db_importar:
#             print(
#                 f"\nNome: {db_nome}\nLink: {db_link}\nID: {db_ID}\nSubtasks: {db_Subtasks}\nImportar?: {db_importar}\n\n")

    # create_comment_reply("e4fe2126acb24b14a8c6f988140a71f5", "Deu certo")

    # CREATE PAGE exemplo
    # title = "Test Title"
    # description = "Test Description"
    # published_date = datetime.now().astimezone(timezone.utc).isoformat()
    # data = {
    #     "URL": {"title": [{"text": {"content": description}}]},
    #     "Title": {"rich_text": [{"text": {"content": title}}]},
    #     "Published": {"date": {"start": published_date, "end": None}}
    # }
    # create_page(data)

    # "Existe algum documento que precisamos saber?": {"files": []},

    # data_juridico = {
    #     "Demanda": {"title": [{"text": {"content": "Teste"}, "plain_text": "Teste", }]},
    #     "Status": {"select": {"name": "Novas Demandas"}},
    #     "Conta mais sobre a sua necessidade!": {"rich_text": [{"text": {"content": "teste"}}]},
    #     "Qual é o seu email?": {"rich_text": [{"text": {"content": "teste"}}]},
    #     "Quem precisa assinar o documento?": {"rich_text": [{"text": {"content": "teste"}}]},
    #     "Para quando essa demanda deve estar feita?": {"date": {"start": "2023-07-30"}},
    #     "Tipo": {"select": {"name": "Contratos com Creators", }},
    #     "Qual é a prioridade disso?": {"select": {"name": "Alta", }},
    #     "monday_id": {"rich_text": [{"text": {"content": "123131231"}}]}
    # }
    # resp = create_page(data_juridico)
    # print(resp)
    # # getpage exemplo
    # pages = get_pages()
    # for page in pages:
    #     page_id = page["id"]
    #     props = page["properties"]
    #     url = props["URL"]["title"][0]["text"]["content"]
    #     title = props["Title"]["rich_text"][0]["text"]["content"]
    #     published = props["Published"]["date"]["start"]
    #     published = datetime.fromisoformat(published)

    # # UPDATE PAGE Exemplo
    #  page_id = "the page id"

    # new_date = datetime(2023, 1, 15).astimezone(timezone.utc).isoformat()
    # update_data = {"Published": {"date": {"start": new_date, "end": None}}}

    # update_page(page_id, update_data)
