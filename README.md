# Análise de Chuva e Queimadas

Aplicação web construída com **Streamlit** para análise de **precipitação** e **focos de queimada** em qualquer região do Brasil (ou do mundo). Integra dados de duas APIs da NASA: **NASA POWER** (chuva) e **NASA FIRMS** (queimadas por satélite).

---

## Visão Geral

A aplicação permite ao usuário selecionar uma localização (ponto ou área geográfica) e um período de tempo, e então consulta automaticamente as APIs da NASA para gerar:

- Gráficos de precipitação diária
- Mapa interativo com focos de queimada
- Análise combinada (chuva vs. queimadas)
- Comparativos mensais e anuais
- Download dos dados em CSV

---

## Fontes de Dados

| Fonte          | API                            | Parâmetro / Dados                     | Descrição                                 |
| -------------- | ------------------------------ | ------------------------------------- | ----------------------------------------- |
| **NASA POWER** | `power.larc.nasa.gov`          | `PRECTOTCORR`                         | Precipitação diária corrigida (mm/dia)    |
| **NASA FIRMS** | `firms.modaps.eosdis.nasa.gov` | VIIRS (SNPP, NOAA-20, NOAA-21), MODIS | Focos de queimada detectados por satélite |

---

## Funcionalidades

### 1. Seleção de Área

O usuário pode definir a área de análise de duas formas:

- **Ponto no mapa**: Clique no mapa interativo (Folium) ou insira coordenadas manualmente (latitude/longitude). Utilizado principalmente para consultas de precipitação.
- **Upload de Shapefile/GeoJSON**: Envio de um arquivo `.zip` (shapefile) ou `.geojson` para delimitar uma região poligonal. **Obrigatório** para a análise de queimadas, pois a API FIRMS utiliza bounding box e a aplicação faz um filtro espacial preciso dentro do polígono.

### 2. Modos de Análise

| Modo                         | Descrição                                                                  |
| ---------------------------- | -------------------------------------------------------------------------- |
| **Mês Único**                | Analisa precipitação e queimadas de um único mês selecionado               |
| **Comparativo Mensal**       | Compara dois meses lado a lado (Mês A vs. Mês B) alinhados por dia do mês  |
| **Análise Anual Específica** | Análise detalhada de um ano completo, com detalhamento mensal de queimadas |
| **Comparativo Anual**        | Compara múltiplos anos (até 10) para o mesmo mês ou para o ano inteiro     |

### 3. Abas de Visualização

Cada análise é apresentada em **três abas**:

- **Precipitação**: Gráfico de barras diário, métricas (total, dias com chuva, máxima diária) e tabela de dados.
- **Queimadas**: Mapa interativo com clusters de focos, gráfico de focos por dia, métricas (total de focos, fontes de satélite, área queimada estimada) e tabela de dados.
- **Combinado**: Gráfico sobreposto de precipitação (barras) e focos de queimada (linha), com eixos Y independentes, permitindo identificar correlação visual entre seca e incêndios.

### 4. Satélites Configuráveis

O usuário pode selecionar quais fontes de satélite utilizar para detecção de queimadas:

- **VIIRS – Suomi NPP** (resolução ~375m)
- **VIIRS – NOAA-20** (resolução ~375m)
- **VIIRS – NOAA-21** (resolução ~375m)
- **MODIS – Terra/Aqua** (resolução ~1km)

### 5. Estimativa de Área Queimada

A aplicação estima a área queimada com base na área do pixel de cada satélite:

- VIIRS: 375m x 375m = **~14 ha** por foco
- MODIS: 1km x 1km = **~100 ha** por foco

> **Nota:** Trata-se de uma aproximação e não de um dado oficial de área queimada.

### 6. Download de Dados

Todas as tabelas de dados (precipitação, queimadas filtradas e brutas, dados combinados) podem ser baixadas em formato **CSV**.

---

## Pré-requisitos

- **Python 3.10+**
- **Chave da API FIRMS** (obtenha gratuitamente em [https://firms.modaps.eosdis.nasa.gov/map/#d:24hrs;@0.0,0.0,3.0z](https://firms.modaps.eosdis.nasa.gov/))

---

## Instalação e Execução

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd preciptacao_app
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a variável de ambiente

Crie um arquivo `.env` na raiz do projeto com sua chave da API FIRMS:

```
FIRMS_MAP_KEY="SUA_CHAVE_API_DA_FIRMS_AQUI"
```

### 5. Execute a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador (por padrão em `http://localhost:8501`).

---

## Dependências

| Pacote             | Versão | Função                                  |
| ------------------ | ------ | --------------------------------------- |
| `streamlit`        | 1.50.0 | Framework web da aplicação              |
| `pandas`           | 2.2.3  | Manipulação de dados tabulares          |
| `altair`           | 5.5.0  | Gráficos interativos                    |
| `folium`           | 0.20.0 | Mapas interativos                       |
| `streamlit-folium` | 0.26.1 | Integração Folium + Streamlit           |
| `geopandas`        | 1.1.2  | Processamento de dados geoespaciais     |
| `shapely`          | 2.1.2  | Operações geométricas (filtro espacial) |
| `requests`         | 2.32.5 | Requisições HTTP às APIs                |
| `python-dateutil`  | 2.9.0  | Manipulação avançada de datas           |
| `python-dotenv`    | 1.2.1  | Carregamento de variáveis de ambiente   |

---

## Estrutura do Projeto

```
preciptacao_app/
├── app.py               # Aplicação principal (Streamlit)
├── requirements.txt     # Dependências do projeto
├── .env                 # Chave da API FIRMS (não versionado)
└── README.md            # Este arquivo
```

---

## Fluxo de Funcionamento

```
┌─────────────────────────────────────────────────────┐
│                   SIDEBAR (Entrada)                 │
│                                                     │
│  1. Seleção de Área                                 │
│     ├── Ponto no mapa (clique ou coordenadas)       │
│     └── Upload de Shapefile/GeoJSON                 │
│                                                     │
│  2. Modo de Análise                                 │
│     ├── Mês Único                                   │
│     ├── Comparativo Mensal                          │
│     ├── Análise Anual Específica                    │
│     └── Comparativo Anual                           │
│                                                     │
│  3. Configuração                                    │
│     ├── Satélites FIRMS                             │
│     └── Botão "Analisar"                            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              BUSCA DE DADOS (APIs NASA)              │
│                                                     │
│  ┌─────────────────┐    ┌────────────────────────┐  │
│  │   NASA POWER    │    │     NASA FIRMS         │  │
│  │  (Precipitação) │    │    (Queimadas)         │  │
│  │                 │    │                        │  │
│  │  Ponto (lat/lon)│    │  BBOX do polígono      │  │
│  │  → JSON diário  │    │  → CSV por chunks de   │  │
│  │                 │    │    5 dias + filtro      │  │
│  │                 │    │    espacial no polígono │  │
│  └─────────────────┘    └────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│            VISUALIZAÇÃO (Abas no corpo)              │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ 💧 Chuva │  │🔥Queimadas│  │📈 Combinado     │  │
│  │          │  │          │  │                  │  │
│  │ Métricas │  │ Mapa     │  │ Gráfico overlay  │  │
│  │ Gráficos │  │ Métricas │  │ Chuva vs Focos   │  │
│  │ Tabela   │  │ Gráficos │  │ Tabela           │  │
│  │ CSV ⬇️   │  │ Tabela   │  │ CSV ⬇️           │  │
│  │          │  │ CSV ⬇️   │  │                  │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Observações Importantes

- A **API FIRMS** possui um limite de **5 dias por requisição**. A aplicação divide automaticamente períodos maiores em chunks sequenciais.
- A análise de **queimadas** requer obrigatoriamente o upload de um arquivo de área (Shapefile ou GeoJSON). Sem ele, apenas a aba de precipitação estará disponível.
- Os dados de precipitação da NASA POWER podem ter atraso de 1-2 dias em relação à data atual.
- A aplicação utiliza **cache** (`st.cache_data`) com TTL de 1 hora para evitar requisições repetidas às APIs.
- Valores de precipitação menores que -900 na API são tratados como dados ausentes (NaN).
