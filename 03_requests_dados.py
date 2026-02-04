import redis
import json
import time
import requests # Biblioteca para fazer requisições HTTP

# Configuração da API Pública (5000 registros)
URL_API = "https://jsonplaceholder.typicode.com/photos"

# Conexão com o Redis (Docker)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def carregar_dados_web():
    print(f"🌍 Baixando dados reais de: {URL_API} ...")
    
    try:
        # 1. EXTRAÇÃO (Extract)
        inicio_download = time.time()
        response = requests.get(URL_API)
        
        # Verifica se deu certo (Código 200 = OK)
        if response.status_code != 200:
            print(f"❌ Erro ao baixar dados. Status Code: {response.status_code}")
            return

        lista_fotos = response.json()
        tempo_download = time.time() - inicio_download
        
        total = len(lista_fotos)
        print(f"✅ Download concluído! {total} registros baixados em {tempo_download:.2f}s.")
        
        # 2. CARGA (Load)
        print(f"🚀 Iniciando inserção no Redis via Pipeline...")
        
        inicio_insert = time.time()
        pipe = r.pipeline() # Abre o "pacote"
        
        for item in lista_fotos:
            # Definindo a chave (Ex: foto:1, foto:2)
            chave = f"foto:{item['id']}"
            
            # 3. TRANSFORMAÇÃO (Transform)
            # O Redis precisa de string, então convertemos o dict para JSON String
            valor_json = json.dumps(item)
            
            # Enfileira o comando
            pipe.set(chave, valor_json)
        
        # Executa os 5000 comandos de uma vez só
        pipe.execute()
        
        fim_insert = time.time()
        tempo_insert = fim_insert - inicio_insert
        
        print(f"💾 Sucesso! {total} fotos inseridas no Redis.")
        print(f"⏱️ Tempo de Inserção: {tempo_insert:.2f} segundos")
        print(f"⚡ Performance: {total / tempo_insert:.0f} registros/segundo")

        # Validando um registro aleatório (O registro ID 1)
        print("\n🔍 Verificando o primeiro registro (foto:1):")
        print(r.get("foto:1"))

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão com a internet: {e}")
    except redis.ConnectionError:
        print("❌ Erro: O Redis não está rodando. Verifique o Docker.")

if __name__ == "__main__":
    carregar_dados_web()