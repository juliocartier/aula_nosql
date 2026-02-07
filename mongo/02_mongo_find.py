from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['aula_nosql']
colecao = db['usuarios']

print("🕵️  BUSCAS AVANÇADAS NO MONGODB\n")

# --- CENÁRIO 1: Busca Exata (Nested Fields) ---
estado_alvo = "Bahia"
print(f"1️⃣  Procurando quem mora na {estado_alvo}...")

# Sintaxe de Ponto: "location.state" acessa campos dentro de campos
filtro = { "location.state": estado_alvo }
projecao = { "name.first": 1, "email": 1, "location.city": 1, "_id": 0 }

# .find() retorna um CURSOR (um iterável), não uma lista imediata
usuarios = colecao.find(filtro, projecao)

contador = 0
for user in usuarios:
    print(f"   -> {user['name']['first']} mora em {user['location']['city']}")
    contador += 1
print(f"   Total: {contador} encontrados.\n")


# --- CENÁRIO 2: Operadores Lógicos ($gt = Greater Than) ---
print("2️⃣  Procurando usuários com idade MAIOR que 60 anos...")

# Query: Onde dob.age > 60
filtro_idade = { "dob.age": { "$gt": 60 } }

usuarios_idosos = list(colecao.find(filtro_idade, {"name.first": 1, "dob.age": 1}))

print(f"   Encontrados {len(usuarios_idosos)} usuários acima de 60 anos.")
if usuarios_idosos:
    print(f"   Exemplo: {usuarios_idosos[0]}")