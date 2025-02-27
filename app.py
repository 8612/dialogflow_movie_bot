from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TMDB_API_KEY = "SUA_CHAVE_TMDB"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "BuscarFilme":
        movie_name = req["queryResult"]["parameters"]["movie"]
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        response = requests.get(url).json()
        if response["results"]:
            movie = response["results"][0]
            reply = f"{movie['title']} ({movie['release_date'][:4]})\n{movie['overview']}"
        else:
            reply = "Filme não encontrado."
    else:
        reply = "Não entendi sua solicitação."

    return jsonify({"fulfillmentText": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
