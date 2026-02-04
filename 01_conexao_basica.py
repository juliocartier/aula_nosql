import redis

# Conecta no Redis rodando no localhost (Docker)
# decode_responses=True é crucial: faz o Redis devolver Strings (texto) ao invés de Bytes (b'texto')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    # O comando PING retorna "PONG" se o banco estiver vivo
    resposta = r.ping()
    print(f"✅ Conexão bem sucedida! Redis respondeu: {resposta}")
    
    # Vamos salvar a primeira chave
    r.set("aula", "Introdução ao NoSQL")
    valor = r.get("aula")
    print(f"🔑 Valor recuperado do banco: {valor}")

except redis.ConnectionError:
    print("❌ Erro: Não foi possível conectar. Verifique se o Docker está rodando.")