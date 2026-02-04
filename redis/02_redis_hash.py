import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("🏗️  Salvando um Objeto (Usuário)...")

# Dicionário Python
usuario = {
    "nome": "João da Silva",
    "email": "joao@email.com",
    "idade": "30",  # Redis prefere strings/numeros
    "cidade": "Fortaleza"
}

# HSET (Hash Set) - Salva o dicionário inteiro numa chave só
# Chave principal: "user:100"
# Mapping: o dicionário
r.hset("user:100", mapping=usuario)

print("💾 Usuário salvo! Buscando dados...")

# 1. Pegar tudo de uma vez (HGETALL)
dados_completos = r.hgetall("user:100")
print(f"Dados completos: {dados_completos}")
print(f"Tipo do retorno: {type(dados_completos)}") # Mostra que volta como dict

# 2. Pegar apenas UM campo específico (HGET)
# Isso é super rápido, não precisa trazer o objeto todo pra memória
email = r.hget("user:100", "email")
print(f"Apenas o email: {email}")