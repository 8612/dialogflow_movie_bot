from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Chave da API do TMDB (defina como variável de ambiente)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3/search/movie"

@app.route("/", methods=["POST"])
def dialogflow_webhook():
    req = request.get_json()

    # Pega a intent detectada
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "BuscarFilme":
        # Obtém o nome do filme da requisição
        nome_filme = req["queryResult"]["parameters"].get("nome-filme")

        if nome_filme:
            # Faz a requisição para o TMDb
            response = requests.get(TMDB_URL, params={"api_key": TMDB_API_KEY, "query": nome_filme, "language": "pt-BR"})
            data = response.json()

            if data["results"]:
                filme = data["results"][0]  # Pega o primeiro resultado
                titulo = filme["title"]
                sinopse = filme["overview"]
                nota = filme["vote_average"]

                resposta = f"O filme {titulo} tem nota {nota}/10. Sinopse: {sinopse}"
            else:
                resposta = "Não encontrei esse filme. Tente outro nome."

        else:
            resposta = "Por favor, informe o nome do filme."

        return jsonify({"fulfillmentText": resposta})

    return jsonify({"fulfillmentText": "Não entendi seu pedido."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
