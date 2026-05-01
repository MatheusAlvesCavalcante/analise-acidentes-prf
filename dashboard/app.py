import streamlit as st
import pandas as pd
import plotly.express as px
from regioes import regioes_ce
import numpy as np
from sklearn.linear_model import LinearRegression


# 1. Configuração da Página (Deve ser a primeira linha)
st.set_page_config(layout="wide", page_title="PRF Analytics Dashboard")

# Custom CSS para forçar o estilo dark e melhorar os cards
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 35px; color: #00f2ff; }
    .stApp { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)




# 1. Configuração (Cache para performance)
@st.cache_data
def get_dashboard_data():
    df = pd.read_csv("E:/Projetos/dash_prf/dataset/df_contagem_muni.csv")
    df['inicial'] = df['municipio'].str[0].str.upper()
    lista_letras = sorted(df['inicial'].unique())
    return df, lista_letras
df, lista_letras = get_dashboard_data()




# 2. Lógica de Filtros (Na Sidebar)
with st.sidebar:
    st.title("Análise PRF")
    
    # Filtro de Ano
    lista_anos = sorted(df['ano'].unique(), reverse=True)
    ano_selecionado = st.multiselect("Selecione os Anos", options=lista_anos, default=lista_anos[0])
    
    # Filtro de Letras/Municipio
    st.title("Filtros de Localidade")

    # Seleção das Letras
    letras_escolhidas = st.multiselect(
        "Selecione as iniciais dos municípios:",
        options=lista_letras,
        default=lista_letras[0] # Começa com a letra 'A' por padrão
    )
    
    # Filtra os municípios que batem com as letras
    municipios_disponiveis = df[df['inicial'].isin(letras_escolhidas)]['municipio'].unique()
    
    # Seleção do Município específico
    municipios_escolhidos = st.multiselect(
        "Selecione os Municípios:",
        options=sorted(municipios_disponiveis)
    )

df_filtrado = df[df['ano'].isin(ano_selecionado)]

# Filtragem final do DataFrame para os gráficos
if municipios_escolhidos:
    df_filtrado = df_filtrado[df_filtrado['municipio'].isin(municipios_escolhidos)]
else:
    # Se nada for escolhido, mostra todos das iniciais selecionadas
    df_filtrado = df_filtrado[df_filtrado['inicial'].isin(letras_escolhidas)]




# 3. Filtragem do DataFrame com base na seleção do usuário
df_filtrado = df[
    (df['ano'].isin(ano_selecionado)) & 
    (df['municipio'].isin(municipios_escolhidos))
]




# 4. EXIBIÇÃO DOS INDICADORES (KPIs)
st.markdown("### Análise Estatística Descritiva")
c1, c2, c3 = st.columns(3)

with c1:
    total_acid = df_filtrado['total_acidentes'].sum()
    st.metric("Total de Acidentes", f"{total_acid:,}".replace(",", "."))

with c2:
    # Aqui você pode colocar a média por ano ou outro dado que tiver no CSV
    media_acid = round(df_filtrado['total_acidentes'].mean(), 2)
    st.metric("Média (μ) / Ano", media_acid)

with c3:
    std_acid = df_filtrado['total_acidentes'].std()
    st.metric("Desvio Padrão (σ) / Ano", f"{std_acid:.2f}")





# 5. SEÇÃO DE COMPARAÇÃO DIRETA
st.subheader("Comparação Direta entre Municípios")

# Como você já tem o 'municipios_escolhidos' da sidebar, 
# o gráfico vai focar neles automaticamente.
if len(municipios_escolhidos) > 0:
    
    # Agrupamos os dados para garantir que temos o total por ano e por município
    df_comp = df_filtrado.groupby(['ano', 'municipio'])['total_acidentes'].sum().reset_index()

    # Criando o gráfico de linhas
    fig_comp = px.line(
        df_comp, 
        x='ano', 
        y='total_acidentes', 
        color='municipio', # Cada cidade terá uma cor diferente
        markers=True,      # Adiciona pontos em cada ano para facilitar a leitura
        template="plotly_dark",
        labels={'ano': 'Ano', 'total_acidentes': 'Total de Acidentes Registrados', 'municipio': 'Cidade'},
        color_discrete_sequence=px.colors.qualitative.Prism # Paleta de cores vibrante
    )

    # Ajustes finos no layout para parecer com a foto
    fig_comp.update_layout(
        hovermode="x unified", # Mostra todos os valores ao passar o mouse no eixo X
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig_comp, use_container_width=True)

else:
    st.info(" Selecione pelo menos um município na barra lateral para ver a comparação temporal.")


# Criando a coluna de Região no DF
def atribuir_regiao(muni):
    for regiao, cidades in regioes_ce.items():
        if muni in cidades:
            return regiao
    

df['regiao'] = df['municipio'].apply(atribuir_regiao)



st.markdown("### Análise Regional e Rankings")

# Filtros para os gráficos de barras (pode ficar na sidebar ou aqui)
col_filtros1, col_filtros2 = st.columns(2)
with col_filtros1:
    anos_barra = st.multiselect("Ano de análise:", options=lista_anos, default=[lista_anos[0]])
with col_filtros2:
    regioes_selecionadas = st.multiselect("Região de análise:", options=['SUL', 'OESTE', 'LESTE', 'NORTE'], default=['SUL'])

# Preparando os dados
col_esq, col_espaco, col_dir = st.columns([1, 0.15, 1])

# Filtragem dos dados baseada no multiselect
df_base = df[df['ano'].isin(anos_barra)]

# --- Gráfico da Esquerda (Total por Região) ---
with col_esq:
    
   df_reg = df_base.groupby('regiao')['total_acidentes'].sum().reset_index()
    
    # Criando o rótulo para aparecer dentro da barra
   df_reg['rotulo'] = df_reg['total_acidentes'].apply(lambda x: f"Total - {x:,}".replace(",", "."))
    
   fig_reg = px.bar(
        df_reg, 
        x='total_acidentes', 
        y='regiao', 
        orientation='h',
        text='rotulo', 
        template="plotly_dark", 
        color_discrete_sequence=['#8e44ad']
    )
    
   fig_reg.update_traces(
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color="white", size=11)
    )
    
    # Inverte o eixo X e esconde rótulos desnecessários
   fig_reg.update_xaxes(autorange="reversed", visible=False)
   fig_reg.update_yaxes(title=None, side="right")
    
   fig_reg.update_layout(margin=dict(l=10, r=10, t=30, b=0), height=350)
   st.plotly_chart(fig_reg, use_container_width=True)

with col_espaco:
    st.empty()


with col_dir:
    # Filtra pelas regiões escolhidas e pega o Top 5
    df_muni_reg = df_base[df_base['regiao'].isin(regioes_selecionadas)]
    df_muni_top = df_muni_reg.groupby('municipio')['total_acidentes'].sum().sort_values(ascending=True).tail(5).reset_index()
    
    # Criando o rótulo
    df_muni_top['rotulo'] = df_muni_top['total_acidentes'].apply(lambda x: f"{x:,} - Acidentes".replace(",", "."))
    
    fig_muni = px.bar(
        df_muni_top, 
        x='total_acidentes', 
        y='municipio', 
        orientation='h',
        text='rotulo',
        template="plotly_dark", 
        color_discrete_sequence=['#9b59b6']
    )
    
    fig_muni.update_traces(
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color="white", size=11)
    )
    
    # Esconde os eixos para o visual Clean
    fig_muni.update_xaxes(visible=False)
    fig_muni.update_yaxes(title=None)
    
    fig_muni.update_layout(margin=dict(l=10, r=10, t=30, b=0), height=350)
    st.plotly_chart(fig_muni, use_container_width=True)


# Fazendo o Gráfico de Brs x Municipio

# --- Na Sidebar (Barra Lateral) ---
# ... (abaixo do filtro de municípios) ...

st.sidebar.markdown("---")
st.sidebar.markdown("### Filtro de Rodovias")

# Pega todas as BRs únicas presentes nos dados
# 1. TRATAMENTO CRÍTICO: Garantir que as BRs sejam tratadas como strings sem o ".0"
# Fazemos isso direto na lista de opções para o usuário
lista_brs_unicas = sorted(df['br'].dropna().unique().tolist())
opcoes_br = [str(int(br)) for br in lista_brs_unicas] # Converte 116.0 -> "116"

brs_selecionadas = st.sidebar.multiselect(
    "Selecione as BRs:",
    options=opcoes_br,
    default=opcoes_br[:2] if opcoes_br else None
)

# --- Na Área Principal ---
st.markdown("---")
st.markdown("##  Evolução Temporal: Municípios vs. Rodovias")

# 2. AJUSTE NA LÓGICA DE FILTRAGEM
# Precisamos garantir que a coluna 'br' do DataFrame também seja comparada como string
# Criamos uma cópia temporária para não alterar o DF original permanentemente
df_temp_filter = df.copy()
df_temp_filter['br_str'] = df_temp_filter['br'].fillna(0).astype(int).astype(str)

# 3. FILTRAGEM: Usamos o 'df' completo para a série temporal (para ver todos os anos)
# ou o 'df_base' se você quiser limitar ao período selecionado. 
# Recomendo usar 'df' para o gráfico de linhas fazer sentido no tempo.
mask = (
    (df_temp_filter['municipio'].isin(municipios_escolhidos)) & 
    (df_temp_filter['br_str'].isin(brs_selecionadas))
)
df_temporal = df_temp_filter[mask]

# Título dinâmico
if municipios_escolhidos and brs_selecionadas:
    st.write(f"Série temporal comparando **{len(municipios_escolhidos)} município(s)** nas rodovias **{', '.join(brs_selecionadas)}**.")

# 4. VERIFICAÇÃO E PLOTAGEM
if not df_temporal.empty:
    # 1. Agrupamos por Ano, Município E BR (para não perder a informação da rodovia)
    df_temporal_agrupado = df_temporal.groupby(['ano', 'municipio', 'br_str'])['total_acidentes'].sum().reset_index()

    # 2. Criamos uma coluna de "Identificação" para a legenda
    # Ex: "Fortaleza (BR-116)"
    df_temporal_agrupado['label_comparacao'] = (
        df_temporal_agrupado['municipio'] + " - BR-" + df_temporal_agrupado['br_str']
    )

    # 3. Geramos o gráfico usando essa nova etiqueta
    fig_temporal = px.line(
        df_temporal_agrupado,
        x='ano',
        y='total_acidentes',
        color='label_comparacao', # Agora cada linha é uma combinação de Cidade + BR
        markers=True,
        template="plotly_dark",
        title="Comparação Detalhada: Municípios por Rodovia",
        labels={'total_acidentes': 'Acidentes', 'ano': 'Ano', 'label_comparacao': 'Filtro'}
    )

    fig_temporal.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_temporal, use_container_width=True)
else:
    # Caso caia aqui, mostramos o que foi filtrado para te ajudar a debugar
    st.info("Nenhum dado encontrado para essa combinação. Verifique se os municípios selecionados possuem registros nas BRs escolhidas.")


st.markdown("---")
st.header(" Predição de Tendência: 2025 - 2026")

# Função para calcular a predição
def predizer_acidentes(dados_agrupados, anos_futuros=[2025, 2026]):
    if len(dados_agrupados) < 2:
        return None
    
    X = dados_agrupados['ano'].values.reshape(-1, 1)
    y = dados_agrupados['total_acidentes'].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    X_futuro = np.array(anos_futuros).reshape(-1, 1)
    y_pred = modelo.predict(X_futuro)
    
    return y_pred

# --- LÓGICA DE PREDIÇÃO POR CONTEXTO ---
col_pred1, col_pred2 = st.columns(2)

with col_pred1:
    st.subheader("Total Estado (CE)")
    df_ceara = df.groupby('ano')['total_acidentes'].sum().reset_index()
    pred_ce = predizer_acidentes(df_ceara)
    
    if pred_ce is not None:
        st.write(f"Estimativa para 2025: **{int(pred_ce[0])}**")
        st.write(f"Estimativa para 2026: **{int(pred_ce[1])}**")
        
        # Mini gráfico de tendência do estado
        df_proj_ce = pd.DataFrame({'ano': [2025, 2026], 'total_acidentes': pred_ce, 'tipo': 'Predição'})
        df_hist_ce = df_ceara.copy(); df_hist_ce['tipo'] = 'Histórico'
        df_final_ce = pd.concat([df_hist_ce, df_proj_ce])
        
        fig_ce = px.line(df_final_ce, x='ano', y='total_acidentes', color='tipo', 
                         line_dash='tipo', markers=True, template="plotly_dark",
                         color_discrete_map={'Histórico': '#00f2ff', 'Predição': '#ff4b4b'})
        fig_ce.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig_ce, use_container_width=True)

with col_pred2:
    st.subheader(" Predição por Localidade ou BR")
    
    # 1. Filtros locais
    muni_pred = st.multiselect("Filtrar Cidades (Vazio = CE Todo):", options=sorted(df['municipio'].unique()), key="pred_muni")
    
    # Criamos a lista de opções para o selectbox tratando o .0 na hora
    opcoes_br_limpas = sorted(df['br'].dropna().unique().astype(int).astype(str).tolist())
    br_pred_sel = st.selectbox("Selecione a BR:", options=opcoes_br_limpas, key="pred_br_select")
    
    # 2. Criando o DataFrame de trabalho e tratando a coluna BR
    df_modelo = df.copy()
    # Criamos a br_str aqui para garantir que ela exista para o filtro
    df_modelo['br_str'] = df_modelo['br'].fillna(0).astype(int).astype(str)
    
    # 3. Aplicação dos Filtros
    if muni_pred:
        df_modelo = df_modelo[df_modelo['municipio'].isin(muni_pred)]
    
    # Agora filtramos pela coluna que acabamos de criar
    df_modelo = df_modelo[df_modelo['br_str'] == br_pred_sel]
    
    # 4. Agrupamento por SOMA (Importante para o valor não vir baixo)
    df_agrupado_pred = df_modelo.groupby('ano')['total_acidentes'].sum().reset_index()
    
    # 5. Execução da Função de Predição
    pred_resultado = predizer_acidentes(df_agrupado_pred)
    
    if pred_resultado is not None and not df_agrupado_pred.empty:
        local_nome = "Ceará (Total)" if not muni_pred else ", ".join(muni_pred)
        st.info(f"Tendência para **{local_nome}** na **BR-{br_pred_sel}**")
        
        # Cards com os números em escala real
        p_col1, p_col2 = st.columns(2)
        p_col1.metric("Previsto 2025", int(pred_resultado[0]))
        p_col2.metric("Previsto 2026", int(pred_resultado[1]))
        
        # 6. Gráfico de Projeção
        df_proj = pd.DataFrame({'ano': [2025, 2026], 'total_acidentes': pred_resultado, 'tipo': 'Predição'})
        df_hist = df_agrupado_pred.copy()
        df_hist['tipo'] = 'Histórico'
        df_final_pred = pd.concat([df_hist, df_proj])
        
        fig_p = px.line(df_final_pred, x='ano', y='total_acidentes', color='tipo', 
                         line_dash='tipo', markers=True, template="plotly_dark",
                         color_discrete_map={'Histórico': '#00f2ff', 'Predição': '#ff4b4b'})
        
        fig_p.update_layout(
            height=300, 
            margin=dict(l=0,r=0,t=10,b=0), 
            xaxis=dict(tickmode='linear', dtick=1),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_p, use_container_width=True)
    else:
        st.warning(" Sem dados históricos suficientes para esta combinação.")


# Baixar os dados 
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(" Baixar Dados Filtrados (CSV)", csv, "analise_prf_ceara.csv", "text/csv")