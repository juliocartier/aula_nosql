from pymongo import MongoClient
import time

client = MongoClient("mongodb://localhost:27017/")
colecao = client['aula_nosql']['usuarios_bigdata']

# Vamos pegar um email que existe lá no meio do banco (ex: o usuário 45.000)
# Assim garantimos que o banco tenha que varrer bastante coisa
usuario_teste = colecao.find_one({"_id": 45000})
email_alvo = usuario_teste['email']

print(f"🎯 Alvo: Buscar o usuário com email '{email_alvo}'")
print(f"📚 Total de documentos na coleção: {colecao.count_documents({})}")
print("-" * 40)

# --- TESTE 1: SEM ÍNDICE (Collection Scan) ---
print("1️⃣  Busca SEM índice (O banco lê documento por documento)...")

# Primeiro, removemos índices antigos se existirem (para garantir o teste)
colecao.drop_indexes()

inicio = time.time()
# O Mongo vai ter que abrir 50.000 JSONs para ver se o email bate
resultado = colecao.find_one({"email": email_alvo})
tempo_sem_indice = time.time() - inicio

print(f"   Tempo: {tempo_sem_indice:.6f} segundos")
if tempo_sem_indice > 0.05:
    print("   🐢 Lento! (Para padrões de banco de dados)")


# --- CRIANDO O ÍNDICE ---
print("\n🛠️  Criando Índice no campo 'email'...")
# create_index organiza o campo 'email' em uma árvore B-Tree (como um índice de livro)
colecao.create_index("email")
print("✅ Índice criado!")


# --- TESTE 2: COM ÍNDICE (Index Scan) ---
print("\n2️⃣  Busca COM índice (O banco vai direto no alvo)...")

inicio = time.time()
resultado = colecao.find_one({"email": email_alvo})
tempo_com_indice = time.time() - inicio

print(f"   Tempo: {tempo_com_indice:.6f} segundos")

# --- CONCLUSÃO ---
print("-" * 40)
if tempo_sem_indice > 0 and tempo_com_indice > 0:
    melhoria = tempo_sem_indice / tempo_com_indice
    print(f"🚀 O MongoDB ficou {melhoria:.1f}x mais rápido com o índice!")
else:
    print("🚀 A busca foi tão rápida que o relógio mal marcou (0.0s).")