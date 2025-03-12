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
                print(f"Filme encontrado: {movie['title']}") #Log
                response = {
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    f"Que tal o filme {movie['title']}? {movie['overview']}"
                                ]
                            }
                        }
                    ]
                }
                return jsonify(response)
            else:
                print("Nenhum filme encontrado.") #Log
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
            print("Gênero não encontrado.") #Log
            response = {
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    "Desculpe, não encontrei esse gênero."
                                ]
                            }
                        }
                    ]
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
                        }
                    ]
        return jsonify(response)

def get_genre_id(genre_name):
    # ...

def get_random_movie_by_genre(genre_id):
    # ...

if __name__ == '__main__':
    app.run(debug=True)
