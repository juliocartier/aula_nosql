from cassandra.cluster import Cluster

def preparar_ambiente_exercicios():
    print("⏳ A conectar ao Cassandra local...")
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()

    # ==========================================
    # 1. AMBIENTE PARA OS EXERCÍCIOS DE E-COMMERCE
    # ==========================================
    print("\n🛒 A criar Keyspace 'ecommerce'...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS ecommerce 
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
    """)
    session.set_keyspace('ecommerce')

    print("📝 A criar tabela 'avaliacoes' (Para Exercícios Python 1 e 2)...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id_produto uuid,
            data_hora timestamp,
            nota int,
            comentario text,
            PRIMARY KEY (id_produto, data_hora)
        ) WITH CLUSTERING ORDER BY (data_hora DESC);
    """)

    print("📝 A criar tabela 'carrinho_compras' (Para Exercício de Terminal/Modelagem)...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS carrinho_compras (
            id_usuario uuid,
            id_produto uuid,
            nome_produto text,
            quantidade int,
            PRIMARY KEY (id_usuario, id_produto)
        );
    """)

    # ==========================================
    # 2. AMBIENTE PARA OS EXERCÍCIOS DE SEGURANÇA
    # ==========================================
    print("\n🔐 A criar Keyspace 'seguranca'...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS seguranca 
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
    """)
    session.set_keyspace('seguranca')

    print("📝 A criar tabela 'logs_acesso' (Para Exercício Python de Gerador de Logs)...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS logs_acesso (
            id_aluno int,
            data_hora timestamp,
            acao text,
            PRIMARY KEY (id_aluno, data_hora)
        ) WITH CLUSTERING ORDER BY (data_hora DESC);
    """)

    print("\n✅ Setup dos exercícios concluído com sucesso!")
    print("👉 Peça aos alunos para atualizarem (Refresh) a extensão do VS Code para visualizarem a estrutura.")
    
    cluster.shutdown()

if __name__ == "__main__":
    preparar_ambiente_exercicios()