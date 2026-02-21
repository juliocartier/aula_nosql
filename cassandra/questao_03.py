from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('aula_social') # Usando a base de dados que populamos antes

# Criamos a query e definimos o tamanho da página (fetch_size)
query = "SELECT nome, cidade FROM usuarios_completo WHERE estado = 'Ceará'"
statement = SimpleStatement(query, fetch_size=2) # Traz apenas 2 por vez

print("📚 A iniciar leitura paginada...")
resultado = session.execute(statement)

contador = 0
for linha in resultado:
    print(f"  -> {linha.nome} (Mora em {linha.cidade})")
    contador += 1
    
    # Quando atinge o tamanho da página, o driver do Cassandra 
    # vai buscar os próximos dados automaticamente nos bastidores.
    if contador % 2 == 0:
        input("\nPressione ENTER para carregar a próxima página...")

print("🏁 Fim dos registos.")
cluster.shutdown()