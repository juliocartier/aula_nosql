import requests
import time
from neo4j import GraphDatabase

# --- CONFIGURAÇÕES ---
URL_API = "https://randomuser.me/api/?results=5000&nat=br"
URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123"

def baixar_dados():
    print(f"A baixar 5.000 utilizadores da API...")
    inicio = time.time()
    resposta = requests.get(URL_API)
    dados = resposta.json()['results']
    print(f" Download concluído em {time.time() - inicio:.2f} segundos.\n")
    return dados

def popular_neo4j_em_massa(dados_api):
    print("⏳ A conectar ao Neo4j...")
    driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
    
    # 1. Limpar o banco para não misturar com os exercícios anteriores
    with driver.session() as session:
        print(" A limpar o grafo antigo...")
        session.run("MATCH (n) DETACH DELETE n")

    # 2. Preparar a lista de dicionários para enviar ao Neo4j de uma só vez
    print(" A formatar os dados para o Neo4j...")
    lista_usuarios = []
    for user in dados_api:
        lista_usuarios.append({
            "uuid": user['login']['uuid'],
            "nome": user['name']['first'],
            "sobrenome": user['name']['last'],
            "email": user['email'],
            "idade": user['dob']['age'],
            "cidade": user['location']['city'],
            "estado": user['location']['state']
        })

    # 3. A Query Cypher de Inserção em Massa (O coração do script)
    # UNWIND pega a nossa lista do Python e itera sobre ela linha a linha.
    # MERGE garante que não vamos criar cidades duplicadas.
    query_insercao_massa = """
    UNWIND $parametros AS linha
    
    // 1. Garante que o Estado existe (se já existir, não cria outro)
    MERGE (e:Estado {nome: linha.estado})
    
    // 2. Garante que a Cidade existe e a liga ao Estado
    MERGE (c:Cidade {nome: linha.cidade})
    MERGE (c)-[:FICA_NO]->(e)
    
    // 3. Cria a Pessoa (usamos CREATE porque assumimos que cada UUID é único)
    CREATE (p:Pessoa {
        uuid: linha.uuid,
        nome: linha.nome,
        sobrenome: linha.sobrenome,
        email: linha.email,
        idade: linha.idade
    })
    
    // 4. Liga a Pessoa à Cidade onde ela mora
    CREATE (p)-[:MORA_EM]->(c)
    """

    # 4. Executar a Query
    print(f" A injetar {len(lista_usuarios)} nós e relacionamentos no Grafo...")
    inicio_insert = time.time()
    
    with driver.session() as session:
        # Passamos a lista inteira como o parâmetro '$parametros' da query
        session.run(query_insercao_massa, parametros=lista_usuarios)
        
    tempo_total = time.time() - inicio_insert
    print(f" Sucesso! Inserção concluída em {tempo_total:.2f} segundos.")
    
    # 5. Validação Rápida
    with driver.session() as session:
        resultado = session.run("MATCH (p:Pessoa) RETURN count(p) as total")
        total_pessoas = resultado.single()['total']
        
        resultado_cidades = session.run("MATCH (c:Cidade) RETURN count(c) as total")
        total_cidades = resultado_cidades.single()['total']
        
        print(f"Resumo do Grafo: {total_pessoas} Pessoas espalhadas por {total_cidades} Cidades únicas.")

    driver.close()

if __name__ == "__main__":
    dados = baixar_dados()
    popular_neo4j_em_massa(dados)