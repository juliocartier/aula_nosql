from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['aula_nosql']
col_orders = db['pedidos']

print("📊 Relatório de Pedidos (Cruzando dados com Usuários)...")

# Pipeline de Agregação
pipeline = [
    # 1. Filtra: Quero apenas pedidos "Pagos" com valor acima de 1000
    { "$match": { 
        "status": "Pago", 
        "total": { "$gt": 1000 } 
    }},
    
    # 2. Limit: Pegar apenas 5 para não poluir a tela
    { "$limit": 5 },
    
    # 3. LOOKUP (O Join do Mongo)
    # "Vá na coleção 'usuarios_bigdata'.
    #  Pegue o campo '_id' de lá.
    #  Compare com meu campo 'usuario_id' daqui.
    #  Salve o resultado no campo 'dados_cliente'."
    { "$lookup": {
        "from": "usuarios_bigdata",
        "localField": "usuario_id",
        "foreignField": "_id",
        "as": "dados_cliente"
    }},
    
    # 4. Project: Limpar a saída (o lookup traz uma lista, pegamos o item 0)
    { "$project": {
        "pedido_id": "$_id",
        "total": 1,
        # ArrayElemAt pega o primeiro item da lista trazida pelo lookup
        "nome_cliente": { "$arrayElemAt": ["$dados_cliente.name.first", 0] },
        "email_cliente": { "$arrayElemAt": ["$dados_cliente.email", 0] },
        "itens_comprados": { "$size": "$itens" } # Conta quantos itens tem
    }}
]

resultados = list(col_orders.aggregate(pipeline))

for ped in resultados:
    print(f"💰 Pedido {ped['pedido_id']} | R$ {ped['total']}")
    print(f"   Cliente: {ped['nome_cliente']} ({ped['email_cliente']})")
    print(f"   Qtd Itens: {ped['itens_comprados']}")
    print("-" * 30)