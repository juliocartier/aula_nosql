from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
colecao = client['aula_nosql']['usuarios']

# Vamos pegar um usuário aleatório para ser a vítima
vitima = colecao.find_one({"location.state": "São Paulo"})

if vitima:
    id_vitima = vitima['_id']
    nome_antigo = vitima['name']['first']
    
    print(f"🔄 Atualizando usuário: {nome_antigo} (ID: {id_vitima})...")

    # --- UPDATE ONE ---
    # $set: Modifica apenas os campos listados. O resto do documento fica igual.
    # Vamos mudar o nome para "Goku" e dar um campo novo "nivel_poder"
    filtro = { "_id": id_vitima }
    novos_dados = { 
        "$set": { 
            "name.first": "Goku",
            "profissao": "Guerreiro Z" # Campo novo que não existia!
        }
    }

    colecao.update_one(filtro, novos_dados)
    
    # Conferindo
    novo_user = colecao.find_one(filtro)
    print(f"✅ Nome atual: {novo_user['name']['first']}")
    print(f"✅ Profissão: {novo_user.get('profissao')}")

    # --- UPDATE MANY ---
    print("\n🎁 Bônus: Dando um 'premium' para todos as mulheres...")
    # Filtro: gender = female
    # Ação: Adiciona o campo premium = True
    resultado = colecao.update_many(
        { "gender": "female" },
        { "$set": { "assinatura": "Premium" } }
    )
    print(f"   {resultado.modified_count} usuárias atualizadas.")

else:
    print("Nenhum usuário de SP encontrado para teste.")