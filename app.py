import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Chave da API do TMDb (substitua pela sua chave da API)
TMDB_API_KEY = 'sua-chave-da-api-aqui'

# Função para buscar um filme baseado no gênero
def buscar_filme_por_genero(genero):
    # Mapeamento dos gêneros (de acordo com o TMDb)
    generos_map = {
        "ação": 28,
        "comédia": 35,
        "drama": 18,
        "terror": 27
    }

    # Verifica se o gênero existe no mapeamento
    if genero not in generos_map:
        return None

    genero_id = generos_map[genero]

    # Fazendo uma requisição à API do TMDb para buscar filmes do gênero
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genero_id}&sort_by=popularity.desc'
    response = requests.get(url)
    data = response.json()

    # Se não houver filmes, retorna None
    if not data['results']:
        return None

    # Pega o primeiro filme da lista de resultados
    filme = data['results'][0]

    return {
        "titulo": filme['title'],
        "descricao": filme['overview'],
        "poster": f"https://image.tmdb.org/t/p/w500/{filme['poster_path']}"
    }

# Função para gerar o Custom Payload para o Telegram
def gerar_custom_payload(filme):
    payload = {
        "text": f"🎬 *{filme['titulo']}*\n\n_{filme['descricao']}_",
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "Ver Poster",
                        "url": filme['poster']
                    }
                ]
            ]
        }
    }

    return payload

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Pega o gênero da requisição do Dialogflow
    genero = data['queryResult']['parameters']['Genero']

    # Busca o filme baseado no gênero
    filme = buscar_filme_por_genero(genero)

    if filme is None:
        return jsonify({
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["Desculpe, não encontrei filmes desse gênero."]
                    }
                }
            ]
        })

    # Gera o payload para enviar ao Telegram
    custom_payload = gerar_custom_payload(filme)

    # Retorna o fulfillment com o Custom Payload
    response = {
        "fulfillmentMessages": [
            {
                "payload": custom_payload
            }
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
