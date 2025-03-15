import requests
import csv
import time

# Lista de palavras-chave para buscar
keywords = ["chromecast", "google home", "apple tv", "amazon fire tv"]

# Função para buscar IDs de itens
def get_item_ids(header, keyword, limit=50):
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={keyword}&limit={limit}" # MLA é o código do site da Argentina
    response = requests.get(url, headers=header) # Fazendo a requisição com os headers

    if response.status_code == 200: # Se a resposta for bem sucedida
        results = response.json().get("results", []) # Captura o campo results da resposta
        return [item["id"] for item in results] # Retorna uma lista com os IDs dos itens
    
    return [] # Se a resposta não for bem sucedida, retorna uma lista vazia

# Função para obter detalhes do item
def get_item_details(header, item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}" # URL para buscar os detalhes do item
    response = requests.get(url, headers=header) # Fazendo a requisição com os headers

    if response.status_code == 200: # Se a resposta for bem sucedida
        return response.json() # Retorna os detalhes do item
    
    return None

token = input("Digite o token de acesso: ") # Solicita o token de acesso ao usuário

if not token: # Se o token não for informado
    print("Token de acesso inválido!")
    exit()

token_header = {
    'Authorization': f'Bearer {token}' # Adiciona o token de acesso ao cabeçalho
}

# Coletar todos os IDs
all_item_ids = []
for keyword in keywords: # Para cada palavra-chave
    all_item_ids.extend(get_item_ids(token_header, keyword)) # Adiciona os IDs dos itens encontrados

all_item_ids = list(set(all_item_ids)) # Remove IDs duplicados

print(f"{len(all_item_ids)} IDs de itens coletados com sucesso!")

# Coletar dados de cada item
items_data = []
for item_id in all_item_ids: # Para cada ID de item
    item_data = get_item_details(token_header, item_id) # Coleta os detalhes do item usando o token_header
    if item_data: # Se os detalhes do item foram coletados com sucesso
        items_data.append(item_data) # Adiciona os detalhes do item à lista
    time.sleep(0.2)  # Aguarda 0.2 segundos para evitar sobrecarregar o servidor

print(f"{len(items_data)} itens coletados com sucesso!")

# Escrever os dados no CSV
with open("api//items.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Cabeçalho
    headers = ["id", "title", "price", "currency_id", "available_quantity", "sold_quantity", "condition", "category_id", "permalink"]
    csv_writer.writerow(headers)

    # Dados
    for item in items_data:
        csv_writer.writerow([
            item.get("id"),
            item.get("title"),
            item.get("price"),
            item.get("currency_id"),
            item.get("available_quantity"),
            item.get("sold_quantity"),
            item.get("condition"),
            item.get("category_id"),
            item.get("permalink")
        ])

print("Arquivo CSV gerado com sucesso!")
