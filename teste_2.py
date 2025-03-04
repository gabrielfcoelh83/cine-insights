"""
Teste 2: Sistema de Recomendação de Filmes

Este script recebe o ID de um filme e retorna 5 filmes recomendados
baseados em critérios como gênero, popularidade, diretores e elenco.

Uso:
    python teste_2.py [id_filme]
    
Exemplo:
    python teste_2.py 550
"""

import sys
import json
from collections import Counter
from utils.tmdb_api import TMDBApi

class RecomendadorFilmes:
    """Classe para recomendar filmes com base em um filme de referência."""
    
    def __init__(self, filme_id):
        """
        Inicializa o recomendador com um filme de referência.
        
        Args:
            filme_id (int): ID do filme de referência no TMDB
        """
        self.filme_id = filme_id
        self.filme_referencia = None
        self.creditos_referencia = None
        self.recomendacoes_api = None
        
        # Carregar dados do filme de referência
        self._carregar_dados_referencia()
    
    def _carregar_dados_referencia(self):
        """Carrega os dados do filme de referência."""
        # Obter detalhes do filme
        self.filme_referencia = TMDBApi.get_movie_details(self.filme_id)
        if not self.filme_referencia:
            print(f"Erro: Não foi possível obter detalhes do filme {self.filme_id}.")
            return False
        
        # Obter créditos do filme
        self.creditos_referencia = TMDBApi.get_movie_credits(self.filme_id)
        if not self.creditos_referencia:
            print(f"Erro: Não foi possível obter créditos do filme {self.filme_id}.")
            return False
        
        # Obter recomendações da API
        self.recomendacoes_api = TMDBApi.get_movie_recommendations(self.filme_id)
        if not self.recomendacoes_api:
            print(f"Erro: Não foi possível obter recomendações para o filme {self.filme_id}.")
            return False
        
        return True
    
    def _extrair_caracteristicas_referencia(self):
        """
        Extrai características relevantes do filme de referência.
        
        Returns:
            dict: Características do filme de referência
        """
        if not self.filme_referencia or not self.creditos_referencia:
            return None
        
        # Extrair gêneros
        generos = [genero["id"] for genero in self.filme_referencia.get("genres", [])]
        
        # Extrair diretores
        diretores = []
        for membro in self.creditos_referencia.get("crew", []):
            if membro.get("job") == "Director":
                diretores.append(membro.get("id"))
        
        # Extrair atores principais (top 5)
        atores = [ator.get("id") for ator in self.creditos_referencia.get("cast", [])[:5]]
        
        return {
            "id": self.filme_id,
            "titulo": self.filme_referencia.get("title", ""),
            "generos": generos,
            "diretores": diretores,
            "atores": atores,
            "popularidade": self.filme_referencia.get("popularity", 0),
            "ano": self.filme_referencia.get("release_date", "")[:4] if self.filme_referencia.get("release_date") else ""
        }
    
    def recomendar_filmes(self, num_recomendacoes=5):
        """
        Gera recomendações de filmes com base no filme de referência.
        
        Args:
            num_recomendacoes (int): Número de filmes a recomendar
            
        Returns:
            list: Lista de filmes recomendados
        """
        if not self.filme_referencia or not self.creditos_referencia or not self.recomendacoes_api:
            print("Erro: Dados insuficientes para gerar recomendações.")
            return []
        
        # Características do filme de referência
        caracteristicas_ref = self._extrair_caracteristicas_referencia()
        if not caracteristicas_ref:
            return []
        
        # Lista de filmes candidatos (da API de recomendações)
        candidatos = self.recomendacoes_api.get("results", [])
        
        # Se não houver candidatos suficientes, retornar o que temos
        if len(candidatos) <= num_recomendacoes:
            return [self._formatar_recomendacao(filme) for filme in candidatos]
        
        # Calcular pontuação para cada candidato
        filmes_pontuados = []
        
        for filme in candidatos:
            # Obter detalhes e créditos do filme candidato
            detalhes = TMDBApi.get_movie_details(filme["id"])
            creditos = TMDBApi.get_movie_credits(filme["id"])
            
            if not detalhes or not creditos:
                continue
            
            # Calcular pontuação
            pontuacao = self._calcular_pontuacao(caracteristicas_ref, detalhes, creditos)
            
            filmes_pontuados.append({
                "filme": filme,
                "detalhes": detalhes,
                "pontuacao": pontuacao
            })
        
        # Ordenar por pontuação e selecionar os melhores
        recomendacoes = sorted(filmes_pontuados, key=lambda x: x["pontuacao"], reverse=True)[:num_recomendacoes]
        
        # Formatar resultados
        return [self._formatar_recomendacao(rec["filme"], rec["detalhes"], rec["pontuacao"]) 
                for rec in recomendacoes]
    
    def _calcular_pontuacao(self, ref, detalhes, creditos):
        """
        Calcula a pontuação de similaridade entre o filme de referência e um candidato.
        
        Args:
            ref (dict): Características do filme de referência
            detalhes (dict): Detalhes do filme candidato
            creditos (dict): Créditos do filme candidato
            
        Returns:
            float: Pontuação de similaridade
        """
        pontuacao = 0
        
        # 1. Similaridade de gêneros (até 40 pontos)
        generos_candidato = [genero["id"] for genero in detalhes.get("genres", [])]
        generos_comuns = set(ref["generos"]) & set(generos_candidato)
        pontuacao += len(generos_comuns) * (40 / max(1, len(ref["generos"])))
        
        # 2. Diretores em comum (até 20 pontos)
        diretores_candidato = [membro.get("id") for membro in creditos.get("crew", []) 
                              if membro.get("job") == "Director"]
        diretores_comuns = set(ref["diretores"]) & set(diretores_candidato)
        pontuacao += len(diretores_comuns) * 20
        
        # 3. Atores em comum (até 20 pontos)
        atores_candidato = [ator.get("id") for ator in creditos.get("cast", [])[:5]]
        atores_comuns = set(ref["atores"]) & set(atores_candidato)
        pontuacao += len(atores_comuns) * (20 / max(1, len(ref["atores"])))
        
        # 4. Popularidade (até 10 pontos)
        popularidade_ref = ref["popularidade"]
        popularidade_candidato = detalhes.get("popularity", 0)
        # Quanto mais próxima a popularidade, melhor
        diff_popularidade = abs(popularidade_ref - popularidade_candidato)
        pontuacao += max(0, 10 - (diff_popularidade / 10))
        
        # 5. Proximidade temporal (até 10 pontos)
        if ref["ano"] and detalhes.get("release_date"):
            ano_ref = int(ref["ano"])
            ano_candidato = int(detalhes.get("release_date", "")[:4])
            diff_anos = abs(ano_ref - ano_candidato)
            pontuacao += max(0, 10 - diff_anos)
        
        return pontuacao
    
    def _formatar_recomendacao(self, filme, detalhes=None, pontuacao=None):
        """
        Formata os dados de um filme recomendado.
        
        Args:
            filme (dict): Dados básicos do filme
            detalhes (dict, optional): Detalhes adicionais do filme
            pontuacao (float, optional): Pontuação de similaridade
            
        Returns:
            dict: Dados formatados do filme recomendado
        """
        # Se não temos detalhes, obtê-los
        if not detalhes:
            detalhes = TMDBApi.get_movie_details(filme["id"]) or {}
        
        # Formatar resultado
        resultado = {
            "id": filme["id"],
            "titulo": filme["title"],
            "titulo_original": filme.get("original_title", ""),
            "ano": filme.get("release_date", "")[:4] if filme.get("release_date") else "",
            "generos": [genero["name"] for genero in detalhes.get("genres", [])],
            "sinopse": filme.get("overview", ""),
            "popularidade": filme.get("popularity", 0),
            "avaliacao": filme.get("vote_average", 0),
            "poster": f"https://image.tmdb.org/t/p/w500{filme.get('poster_path')}" if filme.get("poster_path") else None
        }
        
        # Adicionar pontuação se disponível
        if pontuacao is not None:
            resultado["pontuacao_similaridade"] = round(pontuacao, 2)
        
        return resultado

def main():
    """Função principal do script."""
    # Verificar argumentos da linha de comando
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Uso: python teste_2.py [id_filme]")
        print("Exemplo: python teste_2.py 550")
        return
    
    # Obter ID do filme da linha de comando
    filme_id = int(sys.argv[1])
    
    # Criar recomendador
    recomendador = RecomendadorFilmes(filme_id)
    
    # Obter detalhes do filme de referência
    filme_ref = recomendador.filme_referencia
    if not filme_ref:
        print(f"Erro: Filme com ID {filme_id} não encontrado.")
        return
    
    print("\n" + "="*50)
    print("SISTEMA DE RECOMENDAÇÃO DE FILMES".center(50))
    print("="*50)
    
    print(f"\nFilme de referência: {filme_ref.get('title')} ({filme_ref.get('release_date', '')[:4]})")
    print(f"Gêneros: {', '.join(g['name'] for g in filme_ref.get('genres', []))}")
    
    # Gerar recomendações
    print("\nGerando recomendações...")
    recomendacoes = recomendador.recomendar_filmes(5)
    
    # Exibir recomendações
    if recomendacoes:
        print("\nFilmes recomendados:")
        for i, filme in enumerate(recomendacoes, 1):
            print(f"\n{i}. {filme['titulo']} ({filme['ano']})")
            print(f"   Gêneros: {', '.join(filme['generos'])}")
            print(f"   Avaliação: {filme['avaliacao']}/10")
            if "pontuacao_similaridade" in filme:
                print(f"   Similaridade: {filme['pontuacao_similaridade']}/100")
            print(f"   Sinopse: {filme['sinopse'][:150]}..." if len(filme['sinopse']) > 150 else f"   Sinopse: {filme['sinopse']}")
    else:
        print("\nNão foi possível gerar recomendações para este filme.")
    
    # Salvar recomendações em arquivo JSON
    if recomendacoes:
        resultado = {
            "filme_referencia": {
                "id": filme_id,
                "titulo": filme_ref.get("title"),
                "ano": filme_ref.get("release_date", "")[:4] if filme_ref.get("release_date") else ""
            },
            "recomendacoes": recomendacoes
        }
        
        with open("recomendacoes.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
        
        print("\nRecomendações salvas em 'recomendacoes.json'")

if __name__ == "__main__":
    main()