import json
import os

__file_path = os.path.join(os.getcwd(), 'databases')

if not os.path.exists('databases'):
    os.makedirs('databases')

# __file_path = 'databases/'

def carregar_dados(self):
    try:
        with open(f"{__file_path}/materials.json", "r") as arquivo_json:
            self.materiais = json.load(arquivo_json)
    except FileNotFoundError:
        self.materiais = []

    try:
        with open(f"{__file_path}/products.json", "r") as arquivo_json:
            self.produtos = json.load(arquivo_json)
    except FileNotFoundError:
        self.produtos = []

    try:
        with open(f"{__file_path}/config.json", "r") as arquivo_json:
            self.system_config = json.load(arquivo_json)
    except FileNotFoundError:
        self.system_config = []

def salvar_dados(self, type):
    if type == "materials":
        dados = self.materiais
    elif type == "products":
        dados = self.produtos

    with open(f'{__file_path}/{type}.json', "w") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4)