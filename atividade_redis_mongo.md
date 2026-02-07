# Desafio Final: O Monitor de Mercado (NoSQL)

| **Disciplina** | Banco de Dados NoSQL |
| :--- | :--- |
| **Tecnologias** | Python, Redis, MongoDB, Docker |

---

## O Objetivo
Você foi contratado por uma Fintech para desenvolver o backend de um **Monitor de Preços em Tempo Real**. O sistema precisa ser capaz de:

1.  Entregar a cotação atual com **baixíssima latência** para o site (Uso do **Redis**).
2.  Armazenar o **histórico de preços** para análise futura de gráficos (Uso do **MongoDB**).

---

## A Arquitetura do Sistema

Seu script Python deve seguir rigorosamente este fluxo lógico para economizar recursos e garantir performance:

1.  **Verificação de Cache:** Antes de ir à internet, verifique se a cotação já está salva no **Redis**.
    * *Cache Hit:* Se estiver no Redis e dentro da validade (TTL), exiba o valor recuperado de lá.
    * *Cache Miss:* Se não estiver (ou expirou), prossiga para o passo 2.
2.  **Consulta Externa:** Faça a requisição `GET` na API escolhida.
3.  **Atualização de Cache:** Salve o novo valor no Redis com um tempo de expiração (**TTL**) adequado.
4.  **Persistência:** Salve um documento JSON no **MongoDB** contendo: `Moeda`, `Valor`, `Data/Hora` e `Variação`.

---

## Escolha o seu Caminho

Você deve escolher **uma** das duas APIs abaixo para realizar o trabalho. Ambas são públicas, gratuitas e não requerem autenticação.

### Opção A: Mercado Tradicional (Dólar & Euro)
*Ideal para quem quer simular um sistema bancário ou casa de câmbio.*

* **API:** AwesomeAPI (Economia)
* **Comportamento:** As cotações variam a cada 30 segundos ou mais. Fora do horário comercial e finais de semana, os valores **não mudam**.
* **Endpoint:** `https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL`
* **TTL Recomendado no Redis:** 30 a 60 segundos.

**Exemplo de Retorno JSON:**
```json
{
  "USDBRL": {
    "code": "USD",
    "bid": "5.1543",
    "create_date": "2023-10-24 15:00:00"
  }
}
```

### Opção B: Mercado Cripto (Bitcoin & Ethereum)
*Ideal para quem quer ver volatilidade, gráficos mudando rápido e "telas piscando".*

* **API:** Binance Public Data
* **Comportamento**: O mercado nunca fecha (24/7). Os preços mudam na casa dos milissegundos.
* **Endpoint:**
```bash
Bitcoin: https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT

Ethereum: https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT
```

* **TTL Recomendado no Redis:** 5 a 10 segundos.

* **Exemplo de Retorno JSON:**

```json
{
  "symbol": "BTCUSDT",
  "price": "34500.12000000"
}
```

## Requisitos Técnicos (O que entregar)

Seu script monitor.py deve conter:

* **Conexão Robusta:** Tratamento de erro (try/except) caso o Docker (Redis/Mongo) não esteja rodando.
* **Loop de Monitoramento:** O script deve rodar continuamente (ex: while True) verificando os preços a cada X segundos.
* **Log Visual:** O terminal deve deixar claro de onde veio o dado. Exemplo:

[CACHE] Bitcoin: $ 34,500.00 (Veio do Redis)
[API] Baixando dados novos... (Foi na Internet)

Histórico Mongo: O documento salvo no MongoDB deve ter o campo data_coleta com o timestamp atual (datetime.now()).

### Desafio Extra (Bônus)
*Para quem escolher a Opção B (Binance): Implemente uma lógica visual que compare o preço novo com o preço antigo (que estava no Redis) antes de sobrescrever, e mostre uma seta indicativa:*

Bitcoin: $ 34,500.00 🟢 (Subiu)
Bitcoin: $ 34,490.00 🔴 (Caiu)