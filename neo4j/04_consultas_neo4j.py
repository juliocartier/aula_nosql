from neo4j import GraphDatabase
import time

# --- CONFIGURAÇÕES ---
URI = "bolt://localhost:7687"
USUARIO = "neo4j"
SENHA = "aluno123"

def brincar_com_consultas_completas():
    print(" A conectar ao Neo4j para extrair inteligência...\n")
    driver = GraphDatabase.driver(URI, auth=(USUARIO, SENHA))
    
    with driver.session() as session:
        
        # ==========================================
        # CONSULTA 1: Todas as Cidades (Sem Limite)
        # ==========================================
        print(" RANKING COMPLETO DE CIDADES NO BRASIL:")
        inicio = time.time()
        
        query_todas_cidades = """
        MATCH (p:Pessoa)-[:MORA_EM]->(c:Cidade)-[:FICA_NO]->(e:Estado)
        RETURN c.nome AS cidade, e.nome AS estado, count(p) AS total_pessoas
        ORDER BY total_pessoas DESC
        """
        resultados = session.run(query_todas_cidades)
        
        total_cidades = 0
        for posicao, linha in enumerate(resultados, 1):
            print(f"  {posicao}º Lugar: {linha['cidade']} ({linha['estado']}) - {linha['total_pessoas']} habitantes")
            total_cidades += 1
            
        print(f" {total_cidades} cidades listadas em {time.time() - inicio:.2f} segundos.\n")
        input("Pressione ENTER para continuar para a próxima consulta...")


        # ==========================================
        # CONSULTA 2: Toda a população de Fortaleza
        # ==========================================
        print("\n TODAS AS PESSOAS EM FORTALEZA (CE):")
        inicio = time.time()
        
        query_fortaleza = """
        MATCH (p:Pessoa)-[:MORA_EM]->(c:Cidade {nome: 'Fortaleza'})-[:FICA_NO]->(e:Estado {nome: 'Ceará'})
        RETURN p.nome AS nome, p.sobrenome AS sobrenome, p.idade AS idade
        ORDER BY p.nome ASC
        """
        resultados_fortaleza = session.run(query_fortaleza)
        
        total_fortaleza = 0
        for linha in resultados_fortaleza:
            print(f"  {linha['nome']} {linha['sobrenome']}, {linha['idade']} anos.")
            total_fortaleza += 1
            
        print(f"{total_fortaleza} pessoas encontradas em {time.time() - inicio:.2f} segundos.\n")
        input("Pressione ENTER para continuar para a próxima consulta...")


        # ==========================================
        # CONSULTA 3: Recomendações para TODO O BANCO
        # ==========================================
        print("\nSISTEMA DE RECOMENDAÇÃO (Para todos os utilizadores):")
        inicio = time.time()
        
        # Removemos o LIMIT da query e também o corte da lista de sugestões (lista_vizinhos)
        # Agora ele traz TODOS os vizinhos possíveis para cada pessoa.
        query_recomendacao = """
        MATCH (alvo:Pessoa)-[:MORA_EM]->(c:Cidade)<-[:MORA_EM]-(vizinho:Pessoa)
        WHERE alvo.uuid <> vizinho.uuid
        WITH alvo, c, collect(vizinho.nome + ' ' + vizinho.sobrenome) AS lista_vizinhos
        RETURN alvo.nome AS nome_alvo, c.nome AS cidade, lista_vizinhos AS sugestoes
        """
        resultados_recomendacao = session.run(query_recomendacao)
        
        total_recomendacoes = 0
        for linha in resultados_recomendacao:
            alvo = linha['nome_alvo']
            cidade = linha['cidade']
            # Como a lista de sugestões pode ter dezenas de pessoas, vamos apenas mostrar o total de amigos sugeridos
            total_sugestoes = len(linha['sugestoes'])
            
            print(f" {alvo} ({cidade}) recebeu {total_sugestoes} sugestões de amizade locais.")
            total_recomendacoes += 1
            
        print(f"Foram processadas recomendações para {total_recomendacoes} utilizadores em {time.time() - inicio:.2f} segundos.\n")

    driver.close()
    print(" Consultas massivas finalizadas com sucesso!")

if __name__ == "__main__":
    brincar_com_consultas_completas()