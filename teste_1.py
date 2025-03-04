"""
Teste 1: Análise de Dados de Filmes

Este script recebe uma lista de IDs de filmes e gera análises sobre:
1. Participação por ator
2. Frequência de gêneros
3. Top 5 atores com maior bilheteria

Uso:
    python teste_1.py [id_filme1 id_filme2 id_filme3 ...]
    
Exemplo:
    python teste_1.py 550 299536 24428 99861 157336
"""

import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from utils.tmdb_api import TMDBApi

def analisar_filmes(ids_filmes):
    """
    Analisa uma lista de filmes e gera relatórios.
    
    Args:
        ids_filmes (list): Lista de IDs de filmes do TMDB
        
    Returns:
        dict: Resultados das análises
    """
    # Dicionários para armazenar os dados coletados
    participacao_atores = Counter()
    frequencia_generos = Counter()
    bilheteria_atores = defaultdict(int)
    
    # Dados dos filmes para referência
    filmes_analisados = []
    
    # Processar cada filme
    for movie_id in ids_filmes:
        # Obter detalhes do filme
        detalhes = TMDBApi.get_movie_details(movie_id)
        if not detalhes:
            print(f"Não foi possível obter detalhes do filme {movie_id}. Pulando...")
            continue
        
        # Obter créditos do filme
        creditos = TMDBApi.get_movie_credits(movie_id)
        if not creditos:
            print(f"Não foi possível obter créditos do filme {movie_id}. Pulando...")
            continue
        
        # Adicionar à lista de filmes analisados
        filmes_analisados.append({
            "id": movie_id,
            "titulo": detalhes.get("title", "Desconhecido"),
            "ano": detalhes.get("release_date", "")[:4] if detalhes.get("release_date") else "Desconhecido",
            "bilheteria": detalhes.get("revenue", 0)
        })
        
        # Processar gêneros
        for genero in detalhes.get("genres", []):
            frequencia_generos[genero.get("name", "Desconhecido")] += 1
        
        # Processar atores
        bilheteria = detalhes.get("revenue", 0)
        for ator in creditos.get("cast", [])[:10]:  # Considerar apenas os 10 principais atores
            nome_ator = ator.get("name", "Desconhecido")
            participacao_atores[nome_ator] += 1
            bilheteria_atores[nome_ator] += bilheteria
    
    # Calcular top 5 atores com maior bilheteria
    top_atores_bilheteria = sorted(
        bilheteria_atores.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:5]
    
    # Preparar resultados
    resultados = {
        "filmes_analisados": filmes_analisados,
        "participacao_atores": dict(participacao_atores.most_common()),
        "frequencia_generos": dict(frequencia_generos.most_common()),
        "top_atores_bilheteria": [
            {"ator": ator, "bilheteria_total": bilheteria}
            for ator, bilheteria in top_atores_bilheteria
        ]
    }
    
    return resultados

def exibir_resultados(resultados):
    """
    Exibe os resultados da análise no console.
    
    Args:
        resultados (dict): Resultados das análises
    """
    print("\n" + "="*50)
    print("ANÁLISE DE DADOS DE FILMES".center(50))
    print("="*50)
    
    # Filmes analisados
    print("\nFilmes analisados:")
    for filme in resultados["filmes_analisados"]:
        print(f"  - {filme['titulo']} ({filme['ano']}) [ID: {filme['id']}]")
    
    # Participação por ator
    print("\nParticipação por Ator:")
    for ator, count in sorted(resultados["participacao_atores"].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {ator}: {count} filme(s)")
    
    # Frequência de gêneros
    print("\nFrequência de Gêneros:")
    for genero, count in resultados["frequencia_generos"].items():
        print(f"  - {genero}: {count} filme(s)")
    
    # Top 5 atores com maior bilheteria
    print("\nTop 5 Atores com Maior Bilheteria:")
    for i, item in enumerate(resultados["top_atores_bilheteria"], 1):
        # Formatar bilheteria em milhões de dólares
        bilheteria_milhoes = item["bilheteria_total"] / 1_000_000
        print(f"  {i}. {item['ator']}: ${bilheteria_milhoes:.2f} milhões")

def salvar_resultados(resultados, formato="json"):
    """
    Salva os resultados da análise em um arquivo.
    
    Args:
        resultados (dict): Resultados das análises
        formato (str): Formato do arquivo (json ou csv)
    """
    if formato.lower() == "json":
        with open("resultados_analise.json", "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        print("\nResultados salvos em 'resultados_analise.json'")
    
    elif formato.lower() == "csv":
        # Salvar participação por ator
        pd.DataFrame(
            {"Ator": list(resultados["participacao_atores"].keys()),
             "Participações": list(resultados["participacao_atores"].values())}
        ).to_csv("participacao_atores.csv", index=False)
        
        # Salvar frequência de gêneros
        pd.DataFrame(
            {"Gênero": list(resultados["frequencia_generos"].keys()),
             "Frequência": list(resultados["frequencia_generos"].values())}
        ).to_csv("frequencia_generos.csv", index=False)
        
        # Salvar top atores por bilheteria
        pd.DataFrame([
            {"Ator": item["ator"], "Bilheteria Total": item["bilheteria_total"]}
            for item in resultados["top_atores_bilheteria"]
        ]).to_csv("top_atores_bilheteria.csv", index=False)
        
        print("\nResultados salvos em arquivos CSV separados.")

def gerar_graficos(resultados):
    """
    Gera gráficos a partir dos resultados da análise.
    
    Args:
        resultados (dict): Resultados das análises
    """
    # Configurar estilo dos gráficos
    plt.style.use('ggplot')
    
    # 1. Gráfico de participação dos 10 atores mais frequentes
    top_atores = dict(sorted(resultados["participacao_atores"].items(), key=lambda x: x[1], reverse=True)[:10])
    
    plt.figure(figsize=(12, 6))
    plt.bar(top_atores.keys(), top_atores.values(), color='skyblue')
    plt.title('Top 10 Atores por Número de Participações')
    plt.xlabel('Ator')
    plt.ylabel('Número de Filmes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('participacao_atores.png')
    
    # 2. Gráfico de frequência de gêneros
    plt.figure(figsize=(12, 6))
    plt.bar(resultados["frequencia_generos"].keys(), resultados["frequencia_generos"].values(), color='lightgreen')
    plt.title('Frequência de Gêneros')
    plt.xlabel('Gênero')
    plt.ylabel('Número de Filmes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('frequencia_generos.png')
    
    # 3. Gráfico de top 5 atores por bilheteria
    atores = [item["ator"] for item in resultados["top_atores_bilheteria"]]
    bilheterias = [item["bilheteria_total"] / 1_000_000 for item in resultados["top_atores_bilheteria"]]
    
    plt.figure(figsize=(12, 6))
    plt.bar(atores, bilheterias, color='salmon')
    plt.title('Top 5 Atores por Bilheteria Total')
    plt.xlabel('Ator')
    plt.ylabel('Bilheteria Total (milhões $)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('top_atores_bilheteria.png')
    
    print("\nGráficos gerados e salvos como arquivos PNG.")

def main():
    """Função principal do script."""
    # Verificar argumentos da linha de comando
    if len(sys.argv) < 2:
        print("Uso: python teste_1.py [id_filme1 id_filme2 id_filme3 ...]")
        print("Exemplo: python teste_1.py 550 299536 24428 99861 157336")
        return
    
    # Obter IDs dos filmes da linha de comando
    ids_filmes = [int(arg) for arg in sys.argv[1:] if arg.isdigit()]
    
    if not ids_filmes:
        print("Nenhum ID de filme válido fornecido.")
        return
    
    print(f"Analisando {len(ids_filmes)} filmes...")
    
    # Realizar análise
    resultados = analisar_filmes(ids_filmes)
    
    # Exibir resultados
    exibir_resultados(resultados)
    
    # Salvar resultados
    salvar_resultados(resultados, "json")
    
    # Gerar gráficos
    gerar_graficos(resultados)

if __name__ == "__main__":
    main()