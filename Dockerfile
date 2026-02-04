# 1. A BASE (O "Ingrediente Principal")
# Estamos pegando a imagem oficial do Redis, versão Alpine (super leve)
FROM redis:alpine

# 2. A PREPARAÇÃO (Organizando a "Cozinha")
# Cria/Define o diretório de trabalho dentro do container
WORKDIR /usr/local/etc/redis

# 3. O TEMPERO (Personalização)
# Copia o arquivo de configuração do seu PC (redis.conf) para dentro do container
# O formato é: COPY <origem_no_seu_pc> <destino_no_container>
COPY redis.conf .

# 4. O SERVIÇO (Como o prato é servido)
# Comando que roda quando o container inicia.
# Aqui dizemos: "Rode o servidor redis usando ESSE arquivo de configuração"
CMD [ "redis-server", "./redis.conf" ]