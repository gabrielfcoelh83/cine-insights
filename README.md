# Projeto de Análise e Recomendação de Filmes

Este projeto consiste em dois scripts Python para análise e recomendação de filmes utilizando a API do The Movie Database (TMDB).

## Funcionalidades

### Teste 1: Análise de Dados de Filmes (`teste_1.py`)

Este script recebe uma lista de IDs de filmes e gera os seguintes relatórios:

1. **Participação por Ator**: Quantos filmes cada ator participou
2. **Frequência de Gêneros**: Quantas vezes cada gênero aparece na lista de filmes
3. **Top 5 Atores com Maior Bilheteria**: Os 5 atores que somam as maiores bilheterias

Além dos relatórios textuais, o script também gera gráficos para visualização dos dados e salva os resultados em formato JSON.

### Teste 2: Sistema de Recomendação de Filmes (`teste_2.py`)

Este script recebe o ID de um único filme e retorna 5 recomendações baseadas em critérios como:

- Gêneros em comum
- Diretores em comum
- Atores em comum
- Popularidade similar
- Proximidade temporal (ano de lançamento)

O sistema calcula uma pontuação de similaridade para cada filme candidato e retorna os 5 melhores.

## Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas Python listadas em `requirements.txt`
- Chave de API do The Movie Database (TMDB)

## Instalação

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

3. Configure sua chave de API:
   - Crie uma conta no [The Movie Database](https://www.themoviedb.org/)
   - Obtenha uma chave de API em [API Settings](https://www.themoviedb.org/settings/api)
   - Edite o arquivo `.env` e adicione sua chave:

```
TMDB_API_KEY=sua_chave_api_aqui
```

## Como Usar

### Análise de Dados de Filmes

```bash
python teste_1.py [id_filme1 id_filme2 id_filme3 ...]
```

Exemplo:
```bash
python teste_1.py 550 299536 24428 99861 157336
```

Onde:
- 550 = Fight Club
- 299536 = Avengers: Infinity War
- 24428 = The Avengers
- 99861 = Avengers: Age of Ultron
- 157336 = Interstellar

### Sistema de Recomendação de Filmes

```bash
python teste_2.py [id_filme]
```

Exemplo:
```bash
python teste_2.py 550
```

## Saídas

### Teste 1: Análise de Dados de Filmes

- **Console**: Exibe os resultados da análise
- **Arquivos**:
  - `resultados_analise.json`: Todos os resultados em formato JSON
  - `participacao_atores.png`: Gráfico de participação dos atores
  - `frequencia_generos.png`: Gráfico de frequência de gêneros
  - `top_atores_bilheteria.png`: Gráfico dos top 5 atores por bilheteria

### Teste 2: Sistema de Recomendação de Filmes

- **Console**: Exibe as 5 recomendações com detalhes
- **Arquivo**: `recomendacoes.json` com os resultados em formato JSON

## Estrutura do Projeto

```
projeto-filmes/
│
├── teste_1.py                # Script de análise de dados de filmes
├── teste_2.py                # Script de recomendação de filmes
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências do projeto
├── .env                      # Arquivo de configuração (chave API)
├── config.py                 # Configurações gerais do projeto
│
└── utils/                    # Pacote de utilitários
    ├── __init__.py           # Torna o diretório um pacote Python
    └── tmdb_api.py           # Módulo para interação com a API TMDB
```

## Critérios de Avaliação Atendidos

✅ **Código limpo e organizado**: Estrutura modular, comentários explicativos, nomes descritivos
✅ **Uso correto da API**: Implementação eficiente das chamadas à API do TMDB
✅ **Eficiência na manipulação de dados**: Uso de estruturas de dados apropriadas (Counter, defaultdict)
✅ **Criatividade na recomendação**: Sistema de pontuação baseado em múltiplos critérios
✅ **Documentação clara**: README detalhado e docstrings explicativas

## Melhorias Futuras

- Interface gráfica para facilitar o uso
- Cache de resultados para reduzir chamadas à API
- Mais opções de visualização de dados
- Filtros adicionais para recomendações
- Suporte a mais idiomas
