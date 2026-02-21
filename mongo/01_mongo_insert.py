# pip install pymongo

import requests
from pymongo import MongoClient

# 1. Conexão (Sem senha, padrão Docker)
client = MongoClient("mongodb://localhost:27017/")

# 2. Definindo o Banco (aula_nosql) e a Coleção (usuarios)
# Analogia: Banco = Arquivo Excel | Coleção = Aba da Planilha
db = client['aula_nosql']
colecao = db['usuarios']

def importar_dados():
    print("🧹 Limpando coleção antiga (para não duplicar na aula)...")
    colecao.delete_many({}) # Cuidado em produção!

    print("🌍 Baixando 1.000 usuários da API...")
    response = requests.get("https://randomuser.me/api/?results=1000&nat=br")
    dados = response.json()['results']

    print("🚀 Inserindo no MongoDB...")
    
    # MÁGICA: Não precisa converter pra String JSON. O Mongo entende lista de dicts.
    # insert_many é muito mais rápido que insert_one num loop
    resultado = colecao.insert_many(dados)

    print(f"✅ Sucesso! {len(resultado.inserted_ids)} documentos inseridos.")
    
    # Mostrando um exemplo
    print("\n🔍 Exemplo de documento inserido:")
    # find_one pega o primeiro que achar
    #print(colecao.find_one({}, {"name": 1, "email": 1, "_id": 0})) 
    print(colecao.find_one({}))

if __name__ == "__main__":
    importar_dados()