from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123"

# MATCH (n) RETURN n

def demonstrar_crud_neo4j():
    driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
    
    with driver.session() as session:
        print("\n" + "="*50)
        print(" 1. READ (SELECIONAR DADOS)")
        print("="*50)
        
        # MATCH: É o "SELECT" do Neo4j. Encontra o padrão desenhado.
        query_read = """
        MATCH (p:Pessoa)-[r:MORA_EM]->(c:Cidade)
        RETURN p.nome AS nome, p.idade AS idade, c.nome AS cidade, r.desde AS ano_mudanca
        """
        resultados = session.run(query_read)
        
        for linha in resultados:
            print(f"👤 {linha['nome']} ({linha['idade']} anos) mora em {linha['cidade']} desde {linha['ano_mudanca']}.")


        print("\n" + "="*50)
        print(" 2. UPDATE (ATUALIZAR NÓS E SETAS)")
        print("="*50)
        
        # SET: Adiciona ou atualiza propriedades. 
        # Vamos fazer a Ana fazer aniversário e ganhar uma nova profissão!
        # E também vamos colocar uma propriedade na seta "CONHECE".
        query_update = """
        // 1. Atualizando o Nó da Ana
        MATCH (ana:Pessoa {nome: 'Ana'})
        SET ana.idade = 29, ana.profissao = 'Engenheira de Software'
        
        // 2. Atualizando a Seta entre a Ana e o João
        WITH ana // Passa a Ana para a próxima etapa da query
        MATCH (ana)-[rel:CONHECE]->(joao:Pessoa {nome: 'João'})
        SET rel.nivel_amizade = 'Melhores Amigos', rel.desde = 2024
        
        RETURN ana.nome AS nome, ana.idade AS nova_idade, ana.profissao AS profissao, rel.nivel_amizade AS amizade
        """
        
        resultado_update = session.run(query_update).single()
        print(f"Atualizado! A {resultado_update['nome']} agora tem {resultado_update['nova_idade']} anos e trabalha como {resultado_update['profissao']}.")
        print(f" Nível de amizade com o João: {resultado_update['amizade']}.")


        print("\n" + "="*50)
        print("  3. DELETE (REMOVER DADOS)")
        print("="*50)
        
        # ATENÇÃO: O Neo4j NÃO DEIXA apagar um nó se ele tiver setas conectadas a ele (para evitar nós "fantasmas").
        # Precisamos usar o DETACH DELETE (Desconecte e Apague).
        
        query_delete = """
        // Vamos apagar o João do banco de dados
        MATCH (joao:Pessoa {nome: 'João'})
        DETACH DELETE joao
        """
        
        print("💣 A apagar o João e todas as conexões que ele tem...")
        session.run(query_delete)
        
        # Validando se o João sumiu
        query_validacao = "MATCH (j:Pessoa {nome: 'João'}) RETURN j"
        verificacao = session.run(query_validacao).single()
        
        if verificacao is None:
            print(" Sucesso! O João foi removido completamente do grafo.")
            
    driver.close()
    print("\n Demonstração CRUD finalizada. Pode ir no navegador ver como a Ana ficou sozinha!")

if __name__ == "__main__":
    demonstrar_crud_neo4j()