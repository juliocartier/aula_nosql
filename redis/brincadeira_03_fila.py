import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

NOME_FILA = "fila:thumbnails"

# --- PARTE 1: O CHEFE (Produtor) ---
print("🏭 Colocando tarefas na fila...")
# Joga 10 IDs de fotos para serem processadas (Empilha na Esquerda - LPUSH)
for i in range(1, 11):
    r.lpush(NOME_FILA, f"foto:{i}")
    print(f" + Foto {i} enviada para a fila.")

tamanho = r.llen(NOME_FILA)
print(f"📦 Tamanho atual da fila: {tamanho} tarefas.")
print("-" * 30)

# --- PARTE 2: O TRABALHADOR (Worker/Consumidor) ---
print("👷 Iniciando processamento (Worker)...")

while True:
    # Tenta pegar tarefa da Direita (RPOP) - FIFO (First In, First Out)
    # RPOP remove da lista e retorna o item. É atômico.
    tarefa = r.rpop(NOME_FILA)
    
    if tarefa:
        print(f" 🔨 Processando {tarefa}...", end="", flush=True)
        time.sleep(0.5) # Finge que está trabalhando pesado
        print(" Feito!")
    else:
        print("💤 Fila vazia! Trabalho concluído.")
        break