from cassandra.cluster import Cluster

# --- CONFIGURAÇÕES ---
KEYSPACE = "aula_social"

def demonstrar_crud():
    print("⏳ A conectar ao cluster Cassandra...")
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect(KEYSPACE)

    print("\n" + "="*50)
    print(" 📖 1. READ (CONSULTA) - O Ponto de Partida")
    print("="*50)
    
    # Vamos buscar UM utilizador do estado "Ceará" para ser o nosso "alvo" de testes.
    # No Cassandra, a cláusula WHERE tem de usar sempre a Partition Key (estado).
    query_busca = "SELECT estado, cidade, uuid, nome, sobrenome, email FROM usuarios_completo WHERE estado = 'Ceará' LIMIT 1"
    alvo = session.execute(query_busca).one()

    if not alvo:
        print("❌ Nenhum utilizador encontrado no Ceará. Execute o script de inserção primeiro.")
        return

    print(f"🎯 Utilizador Alvo Encontrado:")
    print(f"   Nome: {alvo.nome} {alvo.sobrenome}")
    print(f"   Email atual: {alvo.email}")
    print(f"   Localização: {alvo.cidade}, {alvo.estado}")
    print(f"   UUID: {alvo.uuid}")

    print("\n" + "="*50)
    print(" ✏️ 2. UPDATE (ATUALIZAÇÃO DE DADOS)")
    print("="*50)
    
    # REGRA DE OURO DO CASSANDRA: Para atualizar um registo específico, 
    # TEMOS de fornecer a Chave Primária COMPLETA no WHERE (estado, cidade, uuid).
    novo_email = "novo.email.aula@exemplo.com"
    
    query_update = """
        UPDATE usuarios_completo 
        SET email = %s 
        WHERE estado = %s AND cidade = %s AND uuid = %s
    """
    
    print(f"🔄 A alterar o email para: {novo_email} ...")
    session.execute(query_update, (novo_email, alvo.estado, alvo.cidade, alvo.uuid))
    
    # Vamos ler novamente para provar que alterou
    alvo_atualizado = session.execute(query_busca).one()
    print(f"✅ Email após o Update: {alvo_atualizado.email}")


    print("\n" + "="*50)
    print(" 🗑️ 3. DELETE (ELIMINAÇÃO DE DADOS)")
    print("="*50)
    
    # O DELETE também exige a Chave Primária para saber exatamente o que eliminar.
    # Pode eliminar uma linha inteira, ou apenas uma partição inteira (se omitisse a cidade e o uuid).
    query_delete = """
        DELETE FROM usuarios_completo 
        WHERE estado = %s AND cidade = %s AND uuid = %s
    """
    
    print(f"💣 A eliminar o utilizador {alvo.nome} do banco de dados...")
    session.execute(query_delete, (alvo.estado, alvo.cidade, alvo.uuid))
    
    # Vamos tentar ler o utilizador novamente usando a chave primária completa
    query_verificacao = "SELECT * FROM usuarios_completo WHERE estado = %s AND cidade = %s AND uuid = %s"
    verificacao = session.execute(query_verificacao, (alvo.estado, alvo.cidade, alvo.uuid)).one()
    
    if verificacao is None:
        print(f"✅ Sucesso! O utilizador {alvo.nome} desapareceu do mapa.")
    else:
        print("❌ Ops, o utilizador ainda lá está.")

    print("\n🏁 Fim da demonstração CRUD.")
    cluster.shutdown()

if __name__ == "__main__":
    demonstrar_crud()