from pymongo import MongoClient
import random
import time
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['aula_nosql']

# Referências para as 3 coleções
col_users = db['usuarios_bigdata'] # Nossos 50k usuários
col_prods = db['produtos']         # Nossos 1k produtos
col_orders = db['pedidos']         # Onde vamos gravar

def simular_compras():
    print("🛒 Simulando Black Friday (Gerando Pedidos)...")
    
    # 1. Pegar alguns IDs de usuários e produtos reais para não dar erro
    # Vamos pegar os primeiros 100 de cada pra ser rápido
    ids_usuarios = [u['_id'] for u in col_users.find({}, {"_id": 1}).limit(100)]
    ids_produtos = [p['_id'] for p in col_prods.find({}, {"_id": 1}).limit(100)]
    
    pedidos = []
    
    # Gerar 5.000 pedidos
    for _ in range(5000):
        comprador_id = random.choice(ids_usuarios)
        
        # O usuário compra de 1 a 5 produtos aleatórios
        qtd_itens = random.randint(1, 5)
        produtos_escolhidos_ids = random.sample(ids_produtos, k=qtd_itens)
        
        # Buscar os dados REAIS dos produtos (Preço, Nome)
        # O operador $in busca vários IDs de uma vez
        itens_db = list(col_prods.find({"_id": {"$in": produtos_escolhidos_ids}}))
        
        itens_carrinho = []
        total_pedido = 0
        
        for item in itens_db:
            qtd_comprada = random.randint(1, 3)
            
            # SNAPSHOT: Copiamos nome e preço para dentro do pedido
            # Se o preço na coleção 'produtos' mudar, esse pedido fica intacto.
            itens_carrinho.append({
                "produto_id": item['_id'], # Referência (Link)
                "nome_fixo": item['nome'], # Cópia (Histórico)
                "preco_unitario": item['preco'],
                "qtd": qtd_comprada
            })
            total_pedido += (item['preco'] * qtd_comprada)
            
        pedido = {
            "usuario_id": comprador_id,
            "data": datetime.now(),
            "status": random.choice(["Pago", "Pendente", "Enviado"]),
            "itens": itens_carrinho, # Array de objetos (Poder do Mongo!)
            "total": round(total_pedido, 2)
        }
        pedidos.append(pedido)
    
    col_orders.insert_many(pedidos)
    print(f"✅ {len(pedidos)} pedidos realizados com sucesso!")

if __name__ == "__main__":
    simular_compras()