"""A ideia do código é criar uma playlist com 100 músicas de um ano específico, buscando informações
na bilboard e repassando para a API do Spotify"""
"""aqui, as bibliotecas necessárias, conforme explicação no código."""
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
"""input pois o usuário q irá informar a data exata da parada que ele quer ouvir"""
# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
"""#aqui o request para obter a informação do site, usando a url padrão mais a data informada no input"""
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
"""aqui, a variável soup guarda a variável response em formato text, ou seja, todo o código html do site
em formato de texto, para isso, são passados os dois atributos abaixo"""
soup = BeautifulSoup(response.text, 'html.parser')
"""aqui, a variável guarda o resultado do comando para encontrar todas as informações dentro da tag
span e da classe abaixo, lembrando que é necessário inspecionar o elemento para ter o parâmetro de onde está a informação
 que se quer encontrar"""
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
"""aqui, um list comprehension faz um loop e guarda o nome das músicas"""
song_names = [song.getText() for song in song_names_spans]
"""aqui é o código para lidar com a API do Spotify, primeiro usou o spotipy que é uma biblioteca
 para lidar com o spotify, cuja autenticação é bem complexa, pelo que entendi da documentação, o escopo são
as permissões dadas, nesse caso, permissão para mexer em uma playlist privada, a chave é criada provisoriamente
e deve ser encripitada, (no vídeo do youtube que vi, ele faz isso em um programa), o cliente id é fornecida pela API
, o Spotify usa um sistema de OAuth (melhor explicado aqui no material), mas que é o sistema de autenticação
sem passar as informações de login (como acessar sites usando o login do GMAIL)
Creates a SpotifyOAuth object

Parameters:
client_id - the client id of your app
client_secret - the client secret of your app
redirect_uri - the redirect URI of your app
state - security state
scope - the desired scope of the request
cache_path - path to location to save tokens
requests_timeout - tell Requests to stop waiting for a response
after a given number of seconds
username - username of current client"""
#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=YOUR CLIENT ID,
        client_secret=YOUR CLIENT SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
"""aqui, um outro método do Spotipy
current_user()
Get detailed profile information about the current user. An alias for the ‘me’ method.
Esse método cria um dicionário com o ID do usuário, que depois é utilizado abaixo"""
user_id = sp.current_user()["id"]
print(user_id)
"""aqui será feita a busca pela música no spotify, primeiro, cria-se um dicionário vazio, depois, a função
split separa a data por - e pega o primeiro item, então o for loop usa uma função do spotipy para achar
a música dentro do spotify, e imprime o resultado. Como pode acontecer da música não constar no spotify, 
é usado o try o except"""
#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
"""aqui são usadas outras duas funções do spotipy para criar e adicionar itens, os atributos aqui preenchidos
são os obrigatórios, conforme documentação da API"""
#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
