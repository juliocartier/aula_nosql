import requests
from pymongo import MongoClient
import time

# Conexão
client = MongoClient("mongodb://localhost:27017/")
db = client['aula_nosql']
colecao = db['usuarios_bigdata'] # Vamos criar uma coleção separada

def carga_massiva_mongo():
    # Limpa a coleção para o teste ser justo
    colecao.delete_many({})
    
    print("🌍 Baixando 5.000 usuários base da API...")
    try:
        response = requests.get("https://randomuser.me/api/?results=5000&nat=br")
        dados_base = response.json()['results']
        
        print("✅ Download concluído.")
        
        # Multiplicação dos dados (5k -> 50k)
        lista_final = []
        print("⚙️  Duplicando dados para gerar volume de 50.000...")
        
        contador_id = 1
        for _ in range(10): # 10x 5000
            for user in dados_base:
                # O Mongo precisa que cada documento seja uma CÓPIA nova na memória
                novo_user = user.copy()
                
                # Criando um ID personalizado para facilitar busca depois
                novo_user['_id'] = contador_id 
                # Adicionando um campo 'salario' aleatório para brincarmos depois
                novo_user['salario'] = contador_id * 10 
                
                lista_final.append(novo_user)
                contador_id += 1
        
        print(f"🚀 Inserindo {len(lista_final)} documentos no MongoDB...")
        inicio = time.time()
        
        # O COMANDO MÁGICO: insert_many
        # Ele manda pacotes otimizados para o banco. 
        colecao.insert_many(lista_final)
        
        tempo = time.time() - inicio
        print("-" * 30)
        print(f"✅ SUCESSO! 50.000 documentos inseridos.")
        print(f"⏱️ Tempo de Escrita: {tempo:.2f} segundos")
        print(f"⚡ Performance: {len(lista_final)/tempo:.0f} docs/segundo")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    carga_massiva_mongo()