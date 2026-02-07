from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client['aula_nosql']
col_produtos = db['produtos']

# Lista de base para gerar nomes aleatórios
marcas = ["Samsung", "Apple", "Dell", "LG", "Sony", "Logitech"]
tipos = ["Smartphone", "Notebook", "Monitor", "Mouse", "Teclado", "Fone"]
adjetivos = ["Gamer", "Pro", "Ultra", "Slim", "4K", "Wireless"]

def gerar_estoque():
    col_produtos.delete_many({}) # Limpa estoque antigo
    
    lista_produtos = []
    print("🏭 Fabricando 1.000 produtos...")

    for i in range(1, 1001):
        marca = random.choice(marcas)
        tipo = random.choice(tipos)
        adj = random.choice(adjetivos)
        
        produto = {
            "_id": i, # ID sequencial facilita nossa vida na aula
            "nome": f"{tipo} {marca} {adj}",
            "categoria": tipo,
            "preco": round(random.uniform(50, 5000), 2),
            "estoque": random.randint(0, 100),
            "specs": { # Objeto aninhado (feature do Mongo)
                "peso": f"{random.randint(100, 2000)}g",
                "garantia": "1 ano"
            }
        }
        lista_produtos.append(produto)

    col_produtos.insert_many(lista_produtos)
    print("✅ Estoque abastecido!")
    
    # Mostra um exemplo
    print(col_produtos.find_one())

if __name__ == "__main__":
    gerar_estoque()