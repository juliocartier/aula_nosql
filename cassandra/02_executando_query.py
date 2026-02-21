from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

print("⏳ Conectando ao Cluster Cassandra...")

# 1. CONEXÃO
# Não precisamos de senha pois não ativamos autenticação no docker-compose
# Se precisasse: auth_provider = PlainTextAuthProvider(username='cassandra', password='...')
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

print("✅ Conexão estabelecida!")

# 2. CRIAR O KEYSPACE (Equivalente ao "DATABASE" do SQL)
# Aqui definimos a REPLICAÇÃO.
# 'SimpleStrategy': Para desenvolvimento local (1 data center).
# 'replication_factor': 1 (Só temos 1 container/nó).
print("🔧 Criando Keyspace 'aula_social'...")
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS aula_social 
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
""")

# 3. USAR O KEYSPACE
session.set_keyspace('aula_social')

try:
    print("\n☠️ Tentando buscar por conteúdo (Query Proibida)...")
    session.execute("SELECT * FROM timeline WHERE postagem = 'Bom dia pessoal!'")
except Exception as e:
    print(f"❌ ERRO ESPERADO: {e}")