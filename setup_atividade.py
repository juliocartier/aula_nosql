import redis
from pymongo import MongoClient
import random

# Conexões
client_mongo = MongoClient("mongodb://localhost:27017/")
db = client_mongo['pyshop']
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def reset_ambiente():
    print("♻️  Resetando ambiente...")
    r.flushall()
    db.produtos.delete_many({})
    db.pedidos.delete_many({})
    
    # Criar 100 Produtos
    produtos = []
    for i in range(1, 101):
        produtos.append({
            "_id": i,
            "nome": f"Produto {i}",
            "preco": round(random.uniform(100, 1000), 2),
            "categoria": random.choice(["Eletrônicos", "Casa", "Moda"])
        })
    db.produtos.insert_many(produtos)
    print("Ambiente pronto! Podem começar.")

if __name__ == "__main__":
    reset_ambiente()