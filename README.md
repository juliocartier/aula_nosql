# 🐳 Ambiente de Aulas: Bancos de Dados NoSQL

Bem-vindo ao ambiente prático da disciplina de NoSQL! 
Este projeto utiliza **Docker** para garantir que todos tenham a mesma configuração de banco de dados, independentemente do sistema operacional (Windows, Linux ou Mac).

---

## 📋 Pré-requisitos

1.  **Docker** instalado e rodando (Docker Desktop ou Engine).
2.  **Python 3.x** instalado.
3.  **VS Code** (Recomendado) com as extensões sugeridas em aula.

---

## Início Rápido (Docker Compose) - **RECOMENDADO**

Nós utilizaremos o **Docker Compose** para subir todos os bancos de dados necessários de uma só vez, como se fosse um "combo".

### 1. Subir o ambiente (Redis + MongoDB)
Abra o terminal na pasta deste arquivo e execute:

```bash
docker-compose up -d
```

### Verificar status
Mostra quais bancos estão rodando.
```bash
docker ps
```

### Parar o ambiente
Desliga os containers e remove a rede.
```bash
docker-compose down
```


### Comandos Individuais (Opcional)
Se quiser subir apenas um banco por vez:

```bash
# Apenas Redis
docker-compose up -d redis-aula

# Apenas MongoDB
docker-compose up -d mongo-aula
```

### Ver Logs (Depuração)
```bash
docker logs redis-aula
docker logs mongo-aula
```

### 2. Acesso via Terminal (CLI)
Comandos para entrar no shell do banco sem instalar o cliente no seu PC.

MongoDB Shell (mongosh):

```Bash
docker exec -it mongo-aula mongosh
```

Redis CLI:

```Bash
docker exec -it redis-aula redis-cli
```
