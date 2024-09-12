import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta


@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(
        period="1y", start="2021-01-01", end="2024-09-11")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao


@st.cache_data
def carregar_tickers():
    base_tickers = pd.read_csv(
        "data_tickers/IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    print(tickers)
    tickers = [item + ".SA" for item in tickers]
    return tickers


# acoes = carregar_tickers()
acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
dados = carregar_dados(acoes)

st.write("""
# App Preço de Ações
O gráfico abaixo represen-a a evolução do preço das ações ao longo dos anos 
         """)

st.sidebar.header("Filtros")

# filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# filtros da datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Escolha as datas",
                                   min_value=data_inicial,
                                   max_value=data_final,
                                   value=(data_inicial, data_final),
                                   step=timedelta(days=30))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

st.line_chart(dados)


texto_performance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})

for acao in lista_acoes:
    performance_ativo = dados[acao].iloc[-1]/dados[acao].iloc[0]-1
    performance_ativo = float(performance_ativo)
    if performance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + \
            f"  \n {acao}: :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + \
            f"  \n {acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + \
            f"  \n {acao}: {performance_ativo:.1%}"


st.write(f""" ### Performance
         Essa foi a perfomance de cada ativo no período selecionado:
         {texto_performance_ativos}
         """)
