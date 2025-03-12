import os
import random
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sua chave da API do TMDb (coloque em uma variável de ambiente para segurança)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Mapeamento de gêneros para IDs do TMDb
GENERO_IDS = {
    "ação": 28,
    "aventura": 12,
    "animação": 16,
    "comédia": 35,
    "crime": 80,
    "documentário": 99,
    "drama": 18,
    "família": 10751,
    "fantasia": 14,
    "história": 36,
    "terror": 27,
    "música": 10402,
    "mistério": 9648,
    "romance": 10749,
    "ficção científica": 878,
    "thriller": 53,
    "guerra": 10752,
    "faroeste": 37
}

def buscar_filme_por_genero(genero):
    """Busca um filme aleatório no TMDb com base no gênero."""
    genero_id = GENERO_IDS.get(genero.lower())

    if not genero_id:
        return None

    url = f"https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "pt-BR",
        "sort_by": "popularity.desc",
        "with_genres": genero_id,
        "page": random.randint(1, 10)  # Para pegar filmes variados
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("results"):
        filme = random.choice(data["results"])
        titulo = filme["title"]
        descricao = filme.get("overview", "Sem descrição disponível.")
        poster = f"https://image.tmdb.org/t/p/w500{filme['poster_path']}" if filme.get("poster_path") else None
        return titulo, descricao, poster

    return None

@app.route("/", methods=["GET"])
def home():
    return "Bot de recomendação de filmes está rodando!"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    genero = req.get("queryResult", {}).get("parameters", {}).get("genero")

    if genero:
        resultado = buscar_filme_por_genero(genero)
        if resultado:
            titulo, descricao, poster = resultado
            response_text = f"🎬 *{titulo}*\n\n_{descricao}_\n\n"
            if poster:
                response_text += f"![Poster]({poster})"
        else:
            response_text = "Não encontrei nenhum filme desse gênero no momento. 😢"
    else:
        response_text = "Por favor, informe um gênero de filme! 🎭"

    return jsonify({"fulfillmentText": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
