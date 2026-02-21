from cassandra.cluster import Cluster
import uuid
from datetime import datetime

# 1. Ligação
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('ecommerce') # Assume que o keyspace já existe

id_meu_produto = uuid.uuid4()
agora = datetime.now()

# 2. Inserção
query_inserir = """
    INSERT INTO avaliacoes (id_produto, data_hora, nota, comentario) 
    VALUES (%s, %s, %s, %s)
"""
session.execute(query_inserir, (id_meu_produto, agora, 5, "Excelente produto!"))
print("✅ Avaliação inserida com sucesso!")

# 3. Confirmação (Leitura)
query_ler = "SELECT nota, comentario FROM avaliacoes WHERE id_produto = %s"
resultado = session.execute(query_ler, [id_meu_produto])

for linha in resultado:
    print(f"Confirmação -> Nota: {linha.nota} | Comentário: {linha.comentario}")

cluster.shutdown()