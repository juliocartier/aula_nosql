import redis
import requests
import json
import time

# API excelente para gerar perfis completos
# nat=br garante que venham dados que pareçam brasileiros
URL_API = "https://randomuser.me/api/?results=5000&nat=br"
MULTIPLICADOR = 10  # 5k * 10 = 50k

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def carregar_usuarios_complexos():
    print(f"🌍 Baixando 5.000 perfis brasileiros de: {URL_API} ...")
    print("   (Isso pode levar uns 5-10 segundos dependendo da internet)")
    
    try:
        response = requests.get(URL_API)
        dados = response.json()
        lista_usuarios = dados['results'] # A lista real fica dentro da chave 'results'
        
        print(f"🚀 Iniciando inserção de {len(lista_usuarios) * MULTIPLICADOR} usuários no Redis...")
        
        inicio = time.time()
        pipe = r.pipeline()
        contador = 0
        
        for rodada in range(MULTIPLICADOR):
            for user in lista_usuarios:
                contador += 1
                
                # Criando uma chave sequencial fácil de achar
                chave = f"user:{contador}"
                
                # Pequena gambiarra para o ID parecer único no JSON também
                user['login']['uuid'] = f"fake-uuid-{contador}"
                user['email'] = f"usuario{contador}@exemplo.com.br"
                
                # Serializa o objeto complexo para String JSON
                valor_json = json.dumps(user)
                
                pipe.set(chave, valor_json)
                
                # Batch de 5000 em 5000
                if contador % 5000 == 0:
                    pipe.execute()
                    pipe = r.pipeline()
                    print(f"   ... {contador} usuários processados.")

        # Finaliza o restante
        pipe.execute()
        
        tempo = time.time() - inicio
        print("-" * 30)
        print(f"✅ SUCESSO! {contador} perfis salvos.")
        print(f"⏱️ Tempo: {tempo:.2f}s | Velocidade: {contador/tempo:.0f} ops/s")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    carregar_usuarios_complexos()