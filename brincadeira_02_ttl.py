import redis
import json
import time
import uuid

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Pega os dados da foto 50
dados_foto_raw = r.get("foto:50")
dados_foto = json.loads(dados_foto_raw)
url_real = dados_foto['url']

# Gera um token único
token = str(uuid.uuid4())
chave_token = f"download:{token}"

print("⏳ Gerando link temporário (expira em 5s)...")

# Salva o token apontando para a URL real, com vida de 5 segundos
r.setex(chave_token, 5, url_real)

print(f"🔗 Link gerado: meussite.com/download/{token}")

# Contagem regressiva visual
for i in range(6):
    existe = r.get(chave_token)
    ttl = r.ttl(chave_token)
    
    if existe:
        print(f"segundo {i}: ✅ Link ativo (Resta: {ttl}s) -> Redireciona para {existe[:30]}...")
    else:
        print(f"segundo {i}: ❌ Link expirou! (Erro 404)")
        break
    time.sleep(1)