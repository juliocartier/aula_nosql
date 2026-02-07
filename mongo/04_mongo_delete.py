from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
colecao = client['aula_nosql']['usuarios']

# --- DELETE ONE ---
print("🗑️  Removendo o usuário 'Goku' que criamos antes...")
res = colecao.delete_one({ "name.first": "Goku" })
print(f"   Documentos deletados: {res.deleted_count}")

# --- DELETE MANY ---
print("\n🚨 Removendo usuários menores de idade (Compliance)...")
# Filtro: idade menor que 18 ($lt = Less Than)
filtro_menores = { "dob.age": { "$lt": 18 } }

# Antes de deletar, é bom contar!
qtd = colecao.count_documents(filtro_menores)
print(f"   Encontrei {qtd} menores de idade.")

if qtd > 0:
    res_many = colecao.delete_many(filtro_menores)
    print(f"   ✅ {res_many.deleted_count} usuários foram removidos do banco.")
else:
    print("   Ninguém para remover.")