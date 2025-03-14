import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def trata_dados(
        df: pd.DataFrame,
        vlr_col_name: str
) -> pd.DataFrame:
    df_tratado = df.copy()
    df_tratado = df_tratado[df_tratado['Country Code'] == 'ARG']
    df_tratado.drop(columns=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], inplace=True)
    df_tratado = df_tratado.T
    df_tratado.columns = [vlr_col_name]
    df_tratado = df_tratado[df_tratado[vlr_col_name].notnull()]
    df_tratado.reset_index(inplace=True)
    df_tratado.columns = ['Year', vlr_col_name]

    return df_tratado

st.title('🖥️ Evolução da Internet na Argentina')
st.write('Este dashboard tem como objetivo analisar a evolução do uso da internet na Argentina e suas respectivas causas.')
st.write('Por Thiago Monica Huertas')

st.divider()

st.write('### Atualmente na Argentina')

df_populacao = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/populacao_pais.csv')
df_populacao_argentina = df_populacao[df_populacao['Country Code'] == 'ARG']
populacao_argentina = df_populacao_argentina['2023'].values[0]
populacao_argentina = np.floor(populacao_argentina/1000000)
populacao_argentina = "{:,.0f}".format(populacao_argentina)

df_pib = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/pib_pais.csv')
df_pib_argentina = df_pib[df_pib['Country Code'] == 'ARG']
pib_argentina = df_pib_argentina['2023'].values[0]
pib_argentina = np.floor(pib_argentina/1000000)
pib_argentina = "{:,.0f}".format(pib_argentina)

df_uso_internet = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/uso_internet.csv')
df_uso_internet_argentina = trata_dados(df_uso_internet, 'Internet_Users_Percent')
uso_internet_argentina = df_uso_internet_argentina[df_uso_internet_argentina['Year'] == '2023']['Internet_Users_Percent'].values[0]

df_expectativa_vida = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/expectativa_vida.csv')

df_expectativa_vida_argentina = df_expectativa_vida[(df_expectativa_vida['Country Code'] == 'ARG') & (df_expectativa_vida['Series Name'] == 'Life expectancy at birth, total (years)')]
expectativa_vida_argentina = df_expectativa_vida_argentina['2022 [YR2022]'].values[0]
expectativa_vida_argentina = "{:,.1f}".format(expectativa_vida_argentina)

col1, col2 = st.columns(2, gap='medium')
col1.metric('População (2023) 👨‍👩‍👧‍👦', f'{populacao_argentina}MM habitantes')
col1.metric('Expectativa de Vida (2022) 👴', f'{expectativa_vida_argentina} anos')

col2.metric('PIB (2023) 💸', f'{pib_argentina}MM USD')
col2.metric('População com Acesso à Internet (2023) 🌐', f'{uso_internet_argentina:.2f}%')



st.divider()

st.write('### Análise das Tendências de Uso da Internet')
st.write('#### Uso da Internet na Argentina 🌐')
st.write("""
    O gráfico abaixo mostra a evolução do uso da internet na Argentina.
    Os dados são referentes ao percentual de usuários de internet em relação à população total do país.
    É considerado usuário de internet qualquer pessoa que tenha utilizado a internet nos últimos 3 meses em dispositivos como computadores, celulares, tablets, entre outros.
""")



st.line_chart(
    data=df_uso_internet_argentina.set_index('Year')['Internet_Users_Percent'].sort_index(ascending=False),
    x_label='Ano',
    y_label='Usuários de Internet (%)',
    color='#6CACE4',
    use_container_width=True
)

st.write('#### 🔎 Análise:')
st.write("""
    - Os primeiros usuários de internet na Argentina surgiram em 1992.
    - O uso da internet na Argentina aumentou consideravelmente nos últimos anos.
    - A partir de 2009, o uso da internet cresceu de forma mais acelerada.
    - Em 2011, mais da metade da população argentina já utilizava a internet.
    - Em 2017, a Argentina atingiu 74,3% de usuários de internet.
""")

st.write('#### Expansão da Largura de Banda de Internet 📈')
st.write("""
    A largura de banda de internet é a capacidade de transmissão de dados de uma rede de internet.
""")

df_largura_banda = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/largura_banda.csv')
df_largura_banda_argentina = df_largura_banda[df_largura_banda['Economy ISO3'] == 'ARG']
df_largura_banda_argentina.drop(columns=['Economy ISO3', 'Economy Name', 'Indicator ID', 'Attribute 2', 'Attribute 3', 'Partner'], inplace=True)
df_largura_banda_argentina = df_largura_banda_argentina.melt(id_vars=['Indicator', 'Attribute 1'], var_name='Year', value_name='Bandwidth')
df_largura_banda_argentina_bandwidth = df_largura_banda_argentina[df_largura_banda_argentina['Indicator'].isin([
    'Fixed broadband subscriptions: >10 Mbit/s',
    'Fixed broadband subscriptions: 2 to 10 Mbit/s',
    'Fixed broadband subscriptions: 256kbit/s - <2Mbit/s'
])]
df_largura_banda_argentina_bandwidth = df_largura_banda_argentina_bandwidth[df_largura_banda_argentina_bandwidth['Bandwidth'].notnull()]

st.line_chart(
    data=df_largura_banda_argentina_bandwidth,
    x='Year',
    x_label='Ano',
    y='Bandwidth',
    y_label='Quantidade de Assinaturas',
    color='Indicator',
    use_container_width=True
)
st.write('##### 🔎 Análise:')
st.write("""
    - A quantidade de assinaturas de banda larga fixa de 10 Mbit/s ou mais aumentou significativamente nos últimos anos.
    - A quantidade de assinaturas de banda larga fixa de 2 a 10 Mbit/s também aumentou, mas em menor proporção.
    - A quantidade de assinaturas de banda larga fixa de 256kbit/s a <2Mbit/s diminuiu ao longo dos anos.
    - A análise sugere que ao longo dos anos, a Argentina tem investido em infraestrutura de internet de alta velocidade, o que pode ter contribuído para o aumento do uso da internet no país.
""")

st.write('#### Aquisição de Dispositivos Eletrônicos 📱')
st.write("""
    A seguir, analisamos a aquisição de dispositivos eletrônicos na Argentina.
    Os dados são referentes à porcentagem de indivíduos que possuem um celular e de domicílios que possuem um computador.
""")

df_uso_internet_dispositivo = df_largura_banda_argentina[df_largura_banda_argentina['Indicator'].isin([
    'Individuals owning a mobile phone (%)',
    'Households with a computer at home (%)'
])]

st.bar_chart(
    data=df_uso_internet_dispositivo,
    x='Year',
    x_label='Ano',
    y='Bandwidth',
    y_label='Porcentagem de Indivíduos (%)',
    color='Indicator',
    stack=False
)

st.write('##### 🔎 Análise:')
st.write("""
    - A porcentagem de indivíduos que possuem um celular na Argentina é maior do que a porcentagem de domicílios que possuem um computador.
    - A porcentagem de domicílios que possuem um computador oscilou ao longo dos anos.
    - A análise sugere que a aquisição de dispositivos eletrônicos pode ter contribuído para o aumento do uso da internet na Argentina.
""")

st.divider()

st.write('### Análise das Causas do Uso da Internet')
st.write('#### Acesso à Eletricidade ⚡')
st.write("""
    Para entender as causas do aumento do uso da internet na Argentina, vamos analisar o acesso à eletricidade no país.
    Acesso à eletricidade é a porcentagem da população com acesso à eletricidade. Os dados são coletados da indústria, pesquisas nacionais e fontes internacionais.
""")

df_acesso_eletricidade = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/acesso_eletricidade.csv')
df_acesso_eletricidade_argentina = trata_dados(df_acesso_eletricidade, 'Access_Electricity_Percent')

chart_acesso_eletricidade = alt.Chart(df_acesso_eletricidade_argentina).mark_line().encode(
    alt.X('Year:O', title='Ano', type='ordinal'),
    alt.Y('Access_Electricity_Percent:Q', title='Acesso à Eletricidade (%)', type='quantitative', scale=alt.Scale(domain=(df_acesso_eletricidade_argentina['Access_Electricity_Percent'].min(), df_acesso_eletricidade_argentina['Access_Electricity_Percent'].max()))),
    color=alt.value('#6CACE4')
).interactive()

st.altair_chart(chart_acesso_eletricidade, use_container_width=True)

st.write('##### 🔎 Análise:')
st.write("""
    - O acesso à eletricidade na Argentina é quase total.
    - Em 1992, 92,8% da população argentina tinha acesso à eletricidade.
    - Em 2010, houve um aumento significativo de 1% no acesso à eletricidade.
    - Em 2017, 100% da população argentina tinha acesso à eletricidade.
    - Observa-se que a melhoria na infraestrutura de eletricidade pode correlacionar-se com o aumento do uso da internet, dado que o 
    histórico de dados mostra que o crescimento da eletricidade precede o crescimento do uso da internet na Argentina.
    - A análise sugere uma relação positiva entre o acesso à eletricidade e o crescimento do uso da internet ao longo dos anos.
    """)

st.write('#### Avanço da Pesquisa e Desenvolvimento 📚')
st.write("""
    A seguir, analisamos a evolução do quantidade de pesquisas e artigos científicos publicados na Argentina.
    Artigos científicos e técnicos referem-se ao número de artigos científicos e de engenharia publicados nos seguintes campos: física, biologia, química, matemática, medicina clínica, pesquisa biomédica, engenharia e tecnologia, e ciências da terra e do espaço.
    A pesquisa e desenvolvimento é um indicador do esforço de um país em inovação e desenvolvimento tecnológico.
""")

df_pesquisa_desenvolvimento = pd.read_csv('https://raw.githubusercontent.com/ThiagoMonica/analytics-challenge/refs/heads/main/evolucao_internet/dados/publicacao_artigos.csv')
df_pesquisa_desenvolvimento_argentina = trata_dados(df_pesquisa_desenvolvimento, 'Research_Development')
df_pesquisa_desenvolvimento_argentina['Research_Development'] = df_pesquisa_desenvolvimento_argentina['Research_Development'].astype(int)

st.line_chart(
    data=df_pesquisa_desenvolvimento_argentina.set_index('Year')['Research_Development'].sort_index(ascending=False),
    x_label='Ano',
    y_label='Quantidade de Publicações',
    color='#6CACE4',
    use_container_width=True
)

st.write('##### 🔎 Análise:')
st.write("""
    - A quantidade de publicações científicas na Argentina aumentou consideravelmente nos últimos anos.
    - Em 1996, a Argentina publicou 3.315 artigos científicos. 13 anos depois, em 2009, a quantidade de publicações mais que dobrou, atingindo a marca de 6.819 artigos publicados.
    - A análise sugere que o aumento da pesquisa e desenvolvimento pode ter contribuído, em para o crescimento do uso da internet na Argentina.
""")

st.divider()

st.write('### Conclusão ✅')
st.write("""
    - O uso da internet na Argentina aumentou consideravelmente nos últimos anos.
    - A partir de 2009, o uso da internet cresceu de forma mais acelerada. O acesso à eletricidade e o avanço em pesquisa e desenvolvimento podem ter contribuído para esse crescimento.
    - Até o ano de 2016, os argentinos investiam em computadores para acessar a internet, mas recentemente a aquisição de celulares tem sido mais comum, resultando em quase 90% de penetração de dispositivos móveis.
    - A melhoria na infraestrutura de internet de alta velocidade e a aquisição de dispositivos eletrônicos também podem ter contribuído para o aumento do uso da internet na Argentina, dado que a quantidade de assinaturas de banda larga fixa de 10 Mbit/s ou mais aumentou significativamente nos últimos anos.
""")
