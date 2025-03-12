from flask import Flask, request, jsonify
import requests
import os
import random

app = Flask(__name__)

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    intent = data['queryResult']['intent']['displayName']

    if intent == 'Gênero':
        genre = data['queryResult']['parameters']['Gênero']
        genre_id = get_genre_id(genre)

        if genre_id:
            movie = get_random_movie_by_genre(genre_id)
            if movie:
                response = {
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    f"Que tal o filme {movie['title']}? {movie['overview']}"
                                ]
                            }
                        ]
                    }
                    return jsonify(response)
                else:
                    response = {
                        "fulfillmentMessages": [
                            {
                                "text": {
                                    "text": [
                                        "Desculpe, não encontrei nenhum filme desse gênero."
                                    ]
                                }
                            }
                        ]
                    }
                    return jsonify(response)
        else:
            response = {
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    "Desculpe, não encontrei esse gênero."
                                ]
                            }
                        ]
                    }
                return jsonify(response)
    else:
        response = {
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    "Desculpe, não entendi."
                                ]
                            }
                        ]
                    }
        return jsonify(response)

def get_genre_id(genre_name):
    response = requests.get(f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=pt-BR')
    genres = response.json()['genres']
    for genre in genres:
        if genre['name'].lower() == genre_name.lower():
            return genre['id']
    return None

def get_random_movie_by_genre(genre_id):
    page = random.randint(1, 10)
    response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&page={page}&language=pt-BR')
    movies = response.json()['results
