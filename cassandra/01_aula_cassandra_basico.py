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

# 4. CRIAR TABELA (Modelagem)
# Cenário: Timeline de Usuário (Quem postou o quê e quando)
# Partition Key: usuario_id (Para saber em qual servidor guardar)
# Clustering Key: id_post (Para ordenar os dados dentro da partição)
print("📝 Criando Tabela 'timeline'...")
session.execute("""
    CREATE TABLE IF NOT EXISTS timeline (
        usuario_id int,
        usuario_nome text,
        data_hora timestamp,
        postagem text,
        PRIMARY KEY (usuario_id, data_hora)
    ) WITH CLUSTERING ORDER BY (data_hora DESC);
""")
# Nota: 'ORDER BY' faz o Cassandra já gravar no disco ordenado do mais novo para o mais velho!

# 5. INSERIR DADOS (Escrita Rápida)
print("🚀 Inserindo posts...")
# Repare que repetimos o usuario_nome. Desnormalização é normal no Cassandra!
session.execute("INSERT INTO timeline (usuario_id, usuario_nome, data_hora, postagem) VALUES (1, 'Carlos', '2024-02-18 10:00', 'Bom dia pessoal!')")
session.execute("INSERT INTO timeline (usuario_id, usuario_nome, data_hora, postagem) VALUES (1, 'Carlos', '2024-02-18 10:05', 'Partiu aula de NoSQL')")
session.execute("INSERT INTO timeline (usuario_id, usuario_nome, data_hora, postagem) VALUES (2, 'Ana',    '2024-02-18 11:00', 'Alguém viu meu caderno?')")

# 6. CONSULTAR DADOS (Leitura por Partição)
print("\n🔍 Lendo a timeline do Carlos (ID 1):")
# O WHERE precisa usar a Partition Key (usuario_id)
rows = session.execute("SELECT * FROM timeline WHERE usuario_id = 1")

for row in rows:
    # O driver converte timestamp automaticamente para datetime do Python
    print(f"[{row.data_hora}] {row.usuario_nome} disse: {row.postagem}")

# Fechar conexão
cluster.shutdown()