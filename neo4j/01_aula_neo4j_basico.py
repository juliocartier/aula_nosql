# BIBLIOTECA NEO4J: pip install neo4j
# Abra o navegador em: http://localhost:7474
# Login: neo4j | Senha: aluno123
# MATCH (n) RETURN n

from neo4j import GraphDatabase

# --- CONFIGURAÇÕES ---
# O Python conecta-se SEMPRE pela porta 7687 (Protocolo Bolt), nunca pela 7474 (HTTP)
URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123" # A senha que definimos no docker-compose.yml

def criar_grafo_inicial():
    print("A conectar ao Neo4j...")
    
    # Inicia o driver de conexão
    driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
    
    # Abre uma sessão (equivalente ao cursor do SQL ou session do Cassandra)
    with driver.session() as session:
        
        # 1. LIMPAR O BANCO (Cuidado em produção!)
        # Cypher: "Encontre todos os nós (n), desconecte as setas (DETACH) e apague (DELETE)"
        print("🧹 A limpar o banco de dados...")
        session.run("MATCH (n) DETACH DELETE n")
        
        # 2. CRIAR OS NÓS E AS SETAS (O Cypher "desenha" o caminho)
        print("🕸️ A criar os Nós (Pessoas e Cidades) e os Relacionamentos...")
        
        query_criacao = """
        // Criando as Cidades
        CREATE (fortaleza:Cidade {nome: 'Fortaleza', estado: 'CE'})
        CREATE (eusebio:Cidade {nome: 'Eusébio', estado: 'CE'})
        
        // Criando as Pessoas e já ligando às Cidades (MORA_EM)
        CREATE (ana:Pessoa {nome: 'Ana', idade: 28})-[:MORA_EM {desde: 2018}]->(fortaleza)
        CREATE (joao:Pessoa {nome: 'João', idade: 32})-[:MORA_EM {desde: 2021}]->(eusebio)
        
        // Criando o relacionamento entre as Pessoas (CONHECE)
        CREATE (ana)-[:CONHECE]->(joao)
        """
        
        session.run(query_criacao)
        
        # 3. CONSULTAR PARA VALIDAR
        print("\n Validando as conexões de Ana:")
        query_busca = """
        MATCH (p:Pessoa {nome: 'Ana'})-[relacionamento]->(destino)
        RETURN type(relacionamento) AS tipo_seta, labels(destino) AS tipo_destino, destino.nome AS nome_destino
        """
        
        resultados = session.run(query_busca)
        
        print("A Ana tem as seguintes ligações:")
        for linha in resultados:
            print(f"  - [{linha['tipo_seta']}] -> {linha['tipo_destino'][0]} ({linha['nome_destino']})")

    driver.close()
    print("\n Grafo criado com sucesso! Hora de ir para o Navegador.")

if __name__ == "__main__":
    criar_grafo_inicial()