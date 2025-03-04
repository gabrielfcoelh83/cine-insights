"""
Módulo para interação com a API do The Movie Database (TMDB).
"""
import requests
from config import TMDB_API_KEY, TMDB_BASE_URL, DEFAULT_LANGUAGE

class TMDBApi:
    """Classe para interagir com a API do TMDB."""
    
    @staticmethod
    def get_movie_details(movie_id):
        """
        Obtém detalhes de um filme específico.
        
        Args:
            movie_id (int): ID do filme no TMDB
            
        Returns:
            dict: Dados do filme ou None se ocorrer um erro
        """
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": DEFAULT_LANGUAGE,
            "append_to_response": "revenue"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter detalhes do filme {movie_id}: {e}")
            return None
    
    @staticmethod
    def get_movie_credits(movie_id):
        """
        Obtém os créditos (elenco e equipe) de um filme.
        
        Args:
            movie_id (int): ID do filme no TMDB
            
        Returns:
            dict: Dados dos créditos ou None se ocorrer um erro
        """
        url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
        params = {
            "api_key": TMDB_API_KEY,
            "language": DEFAULT_LANGUAGE
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter créditos do filme {movie_id}: {e}")
            return None
    
    @staticmethod
    def get_movie_recommendations(movie_id, page=1):
        """
        Obtém recomendações de filmes similares.
        
        Args:
            movie_id (int): ID do filme no TMDB
            page (int): Número da página de resultados
            
        Returns:
            dict: Dados das recomendações ou None se ocorrer um erro
        """
        url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
        params = {
            "api_key": TMDB_API_KEY,
            "language": DEFAULT_LANGUAGE,
            "page": page
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter recomendações para o filme {movie_id}: {e}")
            return None
    
    @staticmethod
    def search_movie(query):
        """
        Pesquisa filmes pelo título.
        
        Args:
            query (str): Termo de pesquisa
            
        Returns:
            dict: Resultados da pesquisa ou None se ocorrer um erro
        """
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "language": DEFAULT_LANGUAGE,
            "query": query,
            "include_adult": False
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao pesquisar filmes com o termo '{query}': {e}")
            return None