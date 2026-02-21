from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123"

driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))

with driver.session() as session:
    query_idosos = """
    MATCH (p:Pessoa)-[:MORA_EM]->(c:Cidade)-[:FICA_NO]->(e:Estado {nome: 'Ceará'})
    WHERE p.idade >= 60
    RETURN p.nome AS nome, p.idade AS idade, c.nome AS cidade
    ORDER BY p.idade DESC
    LIMIT 5
    """
    resultados = session.run(query_idosos)
    
    print("Público-alvo da campanha (+60 anos no CE):")
    for linha in resultados:
        print(f"  -> {linha['nome']} ({linha['idade']} anos) - Mora em {linha['cidade']}")

driver.close()