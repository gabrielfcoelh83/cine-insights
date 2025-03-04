"""
Configurações do projeto de análise de filmes.
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da API TMDB
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Endpoints da API
MOVIE_DETAILS_ENDPOINT = "/movie/{movie_id}"
MOVIE_CREDITS_ENDPOINT = "/movie/{movie_id}/credits"
MOVIE_RECOMMENDATIONS_ENDPOINT = "/movie/{movie_id}/recommendations"

# Configurações gerais
DEFAULT_LANGUAGE = "pt-BR"