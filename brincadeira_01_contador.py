import redis
import random

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Vamos simular acessos à Foto ID 100
foto_id = 100
chave_contador = f"views:foto:{foto_id}"

print(f"👁️  Simulando tráfego viral na foto {foto_id}...")

# Simula 500 pessoas acessando a foto
for i in range(500):
    # O comando INCR é atômico (thread-safe) e extremamente rápido
    novo_valor = r.incr(chave_contador)
    
    # Só para não poluir a tela, mostra a cada 50 acessos
    if i % 50 == 0:
        print(f"📈 Visualizações atuais: {novo_valor}")

print(f"✅ Total final de views: {r.get(chave_contador)}")

# A Lição: O comando INCR é uma das armas mais poderosas do Redis. Sites de notícias usam isso para "Mais Lidos", jogos usam para "Score".