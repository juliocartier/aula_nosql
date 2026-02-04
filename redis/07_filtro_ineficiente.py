import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

ESTADO_ALVO = "Bahia" # O RandomUser BR gera estados brasileiros

print(f"🕵️ Procurando usuários da {ESTADO_ALVO} em 10.000 registros...")
print("   (Note como isso é 'pesado' para o Python processar)")

inicio = time.time()
encontrados = []

# Vamos varrer apenas os primeiros 10.000 para não demorar demais a aula
# Num banco SQL ou Mongo, o banco faria isso. No Redis, O PYTHON tem que fazer.
for i in range(1, 10001):
    chave = f"user:{i}"
    json_str = r.get(chave)
    
    if json_str:
        # 1. DESERIALIZAR (Custo de CPU alto)
        dados = json.loads(json_str)
        
        # 2. VERIFICAR (Lógica na aplicação)
        # O caminho é: location -> state
        estado_usuario = dados['location']['state']
        
        if estado_usuario == ESTADO_ALVO:
            encontrados.append(dados['name']['first'])

tempo = time.time() - inicio

print(f"✅ Encontrados {len(encontrados)} usuários da {ESTADO_ALVO}.")
print(f"⏱️ Tempo: {tempo:.4f} segundos")
print(f"Exemplos: {encontrados[:5]}")

print("\n💡 LIÇÃO: O Redis é rápido para buscar pela CHAVE (user:1).")
print("   Mas é 'burro' para filtrar pelo CONTEÚDO (state='Bahia').")
print("   Para fazer isso eficiente, precisaremos do MONGODB na próxima aula!")