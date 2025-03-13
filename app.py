import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

TMDB_API_KEY = 'YOUR_API_KEY'  # Substitua com sua chave da API do TMDb
TMDB_API_URL = 'https://api.themoviedb.org/3/discover/movie'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    genre = req['queryResult']['parameters'].get('Genero')

    # IDs dos gêneros no TMDb (exemplo: 28 é Ação, 35 é Comédia, etc.)
    genre_ids = {
        "Ação": 28,
        "Comédia": 35,
        "Drama": 18,
        "Terror": 27,
        "Ficção científica": 878,
        "Romance": 10749
    }

    # Verifique se o gênero fornecido é válido
    genre_id = genre_ids.get(genre)
    if genre_id:
        params = {
            'api_key': TMDB_API_KEY,
            'with_genres': genre_id,
            'sort_by': 'popularity.desc'
        }

        # Faz a requisição à API do TMDb
        response = requests.get(TMDB_API_URL, params=params)
        movies = response.json().get('results')

        if movies:
            # Escolher um filme aleatório da lista de resultados
            movie = random.choice(movies)
            movie_title = movie['title']
            movie_overview = movie['overview']
            movie_poster = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"

            fulfillment_text = f"🎬 *{movie_title}*\n\n_{movie_overview}_\n\n[Ver Poster]({movie_poster})"
        else:
            fulfillment_text = "Desculpe, não encontrei filmes para esse gênero."

    else:
        fulfillment_text = "Desculpe, não entendi o gênero. Tente novamente com um gênero válido como Ação, Comédia, etc."

    return jsonify({
        'fulfillmentText': fulfillment_text
    })

if __name__ == '__main__':
    app.run(debug=True)
