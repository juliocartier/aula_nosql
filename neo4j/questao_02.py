from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123"

driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))

with driver.session() as session:
    query_inserir = """
    // 1. Encontra ou cria a cidade de Eusébio
    MERGE (c:Cidade {nome: 'Eusébio'})
    
    // 2. Cria o Marcos e liga-o à cidade
    CREATE (m:Pessoa {nome: 'Marcos', idade: 25})-[:MORA_EM {desde: 2024}]->(c)
    """
    
    print("A registar o Marcos no sistema...")
    session.run(query_inserir)
    print("Sucesso! O Marcos agora faz parte do Grafo e mora no Eusébio.")

driver.close()