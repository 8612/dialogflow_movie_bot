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
                poster_url = IMAGE_BASE_URL + poster_path if poster_path else None

                # URL para mais detalhes do filme
                filme_url = f"https://www.themoviedb.org/movie/{filme['id']}"

                resposta_texto = f"*🎬 {titulo}*\n📊 *Nota:* {nota}/10\n📖 *Sinopse:* {sinopse}\n🔗 [Mais detalhes]({filme_url})"

                # Criando o payload no formato do Telegram
                telegram_payload = {
                    "telegram": {
                        "text": resposta_texto,
                        "parse_mode": "Markdown",
                        "reply_markup": {
                            "inline_keyboard": [[
                                {"text": "🎥 Ver no TMDb", "url": filme_url}
                            ]]
                        }
                    }
                }

                if poster_url:
                    telegram_payload["telegram"]["photo"] = poster_url  # Adiciona a imagem

                return jsonify({"payload": telegram_payload})

            else:
                return jsonify({"fulfillmentText": "Não encontrei esse filme. Tente outro nome."})

    return jsonify({"fulfillmentText": "Não entendi seu pedido."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
