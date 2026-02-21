import requests
import time
import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args

# --- CONFIGURAÇÕES ---
URL_API = "https://randomuser.me/api/?results=5000&nat=br"
KEYSPACE = "aula_social"

def baixar_dados():
    print(f"🌍 Baixando 5.000 usuários com TODOS os dados...")
    inicio = time.time()
    resposta = requests.get(URL_API)
    dados = resposta.json()['results']
    print(f"✅ Download concluído em {time.time() - inicio:.2f} segundos.\n")
    return dados

def popular_cassandra_completo(dados_api):
    print("⏳ Conectando ao Cassandra...")
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()

    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} 
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': 1 }}
    """)
    session.set_keyspace(KEYSPACE)

    # 1. A TABELA GIGANTE (O Achatamento / Flattening)
    # Veja como mapeamos cada detalhe do JSON para uma coluna específica!
    print("📝 Criando a tabela 'usuarios_completo' (Wide-Column)...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_completo (
            estado text,
            cidade text,
            uuid uuid,
            genero text,
            titulo text,
            nome text,
            sobrenome text,
            email text,
            telefone text,
            celular text,
            rua text,
            numero int,
            cep text,
            pais text,
            latitude text,
            longitude text,
            username text,
            password text,
            data_nascimento timestamp,
            idade int,
            data_registro timestamp,
            foto_large text,
            nacionalidade text,
            PRIMARY KEY ((estado), cidade, uuid)
        ) WITH CLUSTERING ORDER BY (cidade ASC);
    """)

    # 2. PREPARAR A QUERY (Com 23 parâmetros!)
    # Isso mostra para a turma que no SQL/CQL, temos que declarar o destino de cada dado.
    query_insert = session.prepare("""
        INSERT INTO usuarios_completo (
            estado, cidade, uuid, genero, titulo, nome, sobrenome, email, 
            telefone, celular, rua, numero, cep, pais, latitude, longitude, 
            username, password, data_nascimento, idade, data_registro, 
            foto_large, nacionalidade
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?
        )
    """)

    print("⚙️ Mapeando o JSON para as Colunas do Cassandra...")
    parametros_insert = []
    
    for user in dados_api:
        # Extração e conversão de datas ISO para objetos datetime do Python
        # A API retorna algo como "1993-07-20T09:44:18.674Z"
        dt_nasc = datetime.fromisoformat(user['dob']['date'].replace('Z', '+00:00'))
        dt_reg = datetime.fromisoformat(user['registered']['date'].replace('Z', '+00:00'))
        
        # Mapeando todos os campos (Flattening)
        tupla_dados = (
            user['location']['state'],                # estado (Partition Key)
            user['location']['city'],                 # cidade (Clustering Key)
            uuid.UUID(user['login']['uuid']),                    # uuid vindo da própria API
            user['gender'],                           # genero
            user['name']['title'],                    # titulo
            user['name']['first'],                    # nome
            user['name']['last'],                     # sobrenome
            user['email'],                            # email
            user['phone'],                            # telefone
            user['cell'],                             # celular
            user['location']['street']['name'],       # rua
            user['location']['street']['number'],     # numero
            str(user['location']['postcode']),        # cep (forçando string caso venha int)
            user['location']['country'],              # pais
            user['location']['coordinates']['latitude'], # latitude
            user['location']['coordinates']['longitude'],# longitude
            user['login']['username'],                # username
            user['login']['password'],                # password
            dt_nasc,                                  # data_nascimento
            user['dob']['age'],                       # idade
            dt_reg,                                   # data_registro
            user['picture']['large'],                 # foto_large
            user['nat']                               # nacionalidade
        )
        parametros_insert.append(tupla_dados)

    print(f"🚀 Iniciando inserção paralela de {len(parametros_insert)} registros completos...")
    inicio_insert = time.time()
    
    execute_concurrent_with_args(session, query_insert, parametros_insert, concurrency=100)
    
    tempo_total = time.time() - inicio_insert
    print(f"💾 Sucesso! Inserção concluída em {tempo_total:.2f} segundos.\n")

    # 3. VALIDAÇÃO LOCAL 
    estado_busca = "Ceará"
    print(f"🔍 Validando: Trazendo dados complexos do {estado_busca}...")
    
    query_busca = session.prepare("""
        SELECT nome, sobrenome, cidade, rua, numero, data_nascimento 
        FROM usuarios_completo 
        WHERE estado = ? LIMIT 3
    """)
    
    resultados = session.execute(query_busca, [estado_busca])
    
    for row in resultados:
        data_nasc_formatada = row.data_nascimento.strftime("%d/%m/%Y")
        print(f"👤 {row.nome} {row.sobrenome} (Nasc: {data_nasc_formatada})")
        print(f"   📍 Endereço: {row.rua}, {row.numero} - {row.cidade}")
        print("-" * 40)

    cluster.shutdown()

if __name__ == "__main__":
    dados = baixar_dados()
    popular_cassandra_completo(dados)