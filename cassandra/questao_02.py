from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import uuid
from datetime import datetime

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('ecommerce')

id_produto = uuid.uuid4()

# Em vez de passar a string diretamente para o session.execute, 
# criamos um SimpleStatement para configurar o nível de consistência.
query_string = "INSERT INTO avaliacoes (id_produto, data_hora, nota, comentario) VALUES (%s, %s, %s, %s)"

statement = SimpleStatement(
    query_string, 
    consistency_level=ConsistencyLevel.ALL # Exige confirmação de TODOS os nós
)

print("⏳ A tentar inserir com consistência ALL...")
try:
    session.execute(statement, (id_produto, datetime.now(), 4, "Muito bom, mas a entrega atrasou."))
    print("✅ Inserido com segurança máxima!")
except Exception as e:
    print(f"❌ Erro ao inserir: {e}")

cluster.shutdown()