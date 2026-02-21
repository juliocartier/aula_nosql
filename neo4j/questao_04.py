from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123"

driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))

with driver.session() as session:
    query_mudanca = """
    // Passo 1 e 2: Encontrar e cortar a ligação antiga com Caxias
    // Mudamos o nome da variável de 'ana' para 'Gildásio'
    MATCH (gildasio:Pessoa {nome: 'Gildásio'})-[seta_antiga:MORA_EM]->(:Cidade {nome: 'Caxias'})
    DELETE seta_antiga
    
    // Passa a variável 'cristiane' para a próxima etapa da query
    WITH gildasio
    
    // Passo 3: Garantir que Sobral existe e pertence ao Ceará
    MERGE (sobral:Cidade {nome: 'Sobral'})
    MERGE (sobral)-[:FICA_NO]->(:Estado {nome: 'Ceará'})
    
    // Passo 4: Criar a nova ligação da Cristiane com Sobral usando a variável correta
    CREATE (gildasio)-[:MORA_EM {desde: 2024}]->(sobral)
    
    RETURN gildasio.nome AS pessoa, sobral.nome AS nova_cidade
    """
    
    print("A processar a mudança de morada da Gildásio...")
    resultado = session.run(query_mudanca).single()
    
    if resultado:
        print(f"Atualização concluída! A {resultado['pessoa']} mudou-se oficialmente para {resultado['nova_cidade']}.")
    else:
        print("Erro: Não foi possível encontrar a Gildásio ou ela não morava em Caxias.")

driver.close()