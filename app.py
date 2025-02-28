from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Chave da API do TMDB (defina como variável de ambiente no Render)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3/search/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # URL base para os pôsteres

@app.route("/", methods=["POST"])
def dialogflow_webhook():
    req = request.get_json()

    # Pega a intent detectada
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "BuscarFilme":
        # Obtém o nome do filme da requisição
        nome_filme = req["queryResult"]["parameters"].get("nome-filme")

        if nome_filme:
            # Faz a requisição para o TMDB
            response = requests.get(TMDB_URL, params={"api_key": TMDB_API_KEY, "query": nome_filme, "language": "pt-BR"})
            data = response.json()

            if data["results"]:
                filme = data["results"][0]  # Pega o primeiro resultado
                titulo = filme["title"]
                sinopse = filme["overview"]
                nota = filme["vote_average"]
                poster_path = filme.get("poster_path")  # Obtém o caminho da imagem

                # Constrói a URL do pôster (se existir)
                poster_url = IMAGE_BASE_URL + poster_path if poster_path else None

                resposta = f"🎬 *{titulo}*\n📊 Nota: {nota}/10\n📖 Sinopse: {sinopse}"

                # Retorna a resposta formatada para o Telegram
                return jsonify({
                    "fulfillmentMessages": [
                        {"text": {"text": [resposta]}},
                        {"image": {"imageUri": poster_url}} if poster_url else {}
                    ]
                })
            else:
                resposta = "Não encontrei esse filme. Tente outro nome."

        else:
            resposta = "Por favor, informe o nome do filme."

        return jsonify({"fulfillmentText": resposta})

    return jsonify({"fulfillmentText": "Não entendi seu pedido."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

