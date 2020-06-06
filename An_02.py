# Teste da biblioteca de análise de risco
# Autor: Carlo Ralph De Musis

#%% Carrega bibliotecas
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import arisco

#%% Cria variáveis
# O valor de referencia é o inicial
area_variavel = arisco.variavel('Area')
area_variavel.setaReferencia(10)

evaporacao_variavel = arisco.variavel('Evaporacao')
evaporacao_variavel.setaReferencia(12)


#%% Cria lista de variaveis
aux_variaveis = arisco.variaveis()

aux_variaveis.insereVariavel(area_variavel)
aux_variaveis.insereVariavel(evaporacao_variavel)

aux_variaveis.reiniciaVariaveis()


#%% Cria eventos associados a municípios do Mato Grosso.
## Evento 01: Bernoulli.
# Evento com probabilidade de ocorrer um evento favorável.
aux_01_evento = arisco.eventoBernoulli(0.5) # p: 0.5
# Os ponderadores multiplicam o valor das variáveis no caso de evento favorável.
aux_01_evento.insereVariavel(area_variavel, 0.11) 
aux_01_evento.insereVariavel(evaporacao_variavel, 0.21)

## Evento 02: Poisson.
# Média do número de eventos favoráveispor unidade de tempo/espaço.
aux_02_evento = arisco.eventoPoisson(2) # lambda: 2.
# Os ponderadores multiplicam o valor das variáveis para cada evento favorável.
aux_02_evento.insereVariavel(area_variavel, 0.12)
aux_02_evento.insereVariavel(evaporacao_variavel, 0.22)

## Evento 03: Bernoulli.
aux_03_evento = arisco.eventoBernoulli(0.6) # p: 0.3.

aux_03_evento.insereVariavel(area_variavel, 0.13)
aux_03_evento.insereVariavel(evaporacao_variavel, 0.23)

#%% Cria variáveis Inicializa lista de eventos.
aux_eventos = arisco.eventos()

#%% Cria variáveis Insere eventos
aux_eventos.insereEvento(aux_01_evento)
aux_eventos.insereEvento(aux_02_evento)
aux_eventos.insereEvento(aux_03_evento)

print('Referência')
aux_variaveis.apresentaVariaveis()

print('\r\nApós processar os eventos')
aux_eventos.processaEventos()
aux_variaveis.apresentaVariaveis()

print('\r\nApós processar os eventos novamente')
aux_eventos.processaEventos()
aux_variaveis.apresentaVariaveis()

print('\r\nReinicializa as variáveis')
aux_variaveis.reiniciaVariaveis()
aux_variaveis.apresentaVariaveis()

print('\r\nApós processar os eventos')
aux_eventos.processaEventos()
aux_variaveis.apresentaVariaveis()


"""
Fuzzy
"""


#%% Cria variáveis Carrega dados.
df = pd.read_excel('Dados_brutos.xlsx', sheet_name='TOTAL') # Carrega a planilha com os dados.
print(df.head())


#%% Cria variáveis Cria Sistema fuzzy com a variável de saída "Impacto".
i_01 = arisco.sistemaFuzzy(0, 100, n_variavel="Impacto")


#%% Cria a variável de entrada "Área".
## Estatísticas descritivas.
print(df.Km2.mean(), df.Km2.std(), 0, df.Km2.max())
print(df.Km2.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))
sns.distplot(df.Km2) # histograma.

## Cria variável fuzzy triangular.
Area = arisco.variavelFTP(0, df.Km2.max(), 'Area', dados=df.Km2)

## Insere variável no sistema fuzzy.
i_01.insereVariavel(Area)


#%% Cria a variável de entrada "Evaporacao".
## Estatísticas descritivas.
print(df.Evaporacao.mean(), df.Evaporacao.std(), 0, df.Evaporacao.max())
print(df.Evaporacao.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))
sns.distplot(df.Evaporacao) # histograma.

## Cria variável fuzzy gaussiana.
Evaporacao = arisco.variavelFGP(df.Evaporacao.min(), df.Evaporacao.max(), 'Evaporacao', dados=df.Evaporacao)
i_01.insereVariavel(Evaporacao)


#%% Cria conjunto básico de regras
i_01.basicoRegras()

#%% Inicializa simulação
i_01.inicializaSimulacao()

#%% Calculos de teste
print('-Inicial ----------------------')
print(aux_variaveis.obtemVariaveis()[0].obtemReferencia(), ' ', aux_variaveis.obtemVariaveis()[1].obtemReferencia())
print('- Impacto ----')

## Área e evaporação.
aux_i = np.array([[aux_variaveis.obtemVariaveis()[0].obtemReferencia(), 
                   aux_variaveis.obtemVariaveis()[1].obtemReferencia()]])
print(i_01.calculaSimulacao(aux_i))

print('-Após ponderadores-------------')
print(aux_variaveis.obtemVariaveis()[0].obtemValor(), ' ', aux_variaveis.obtemVariaveis()[1].obtemValor())
print('- Impacto ----')

## Área e evaporação.
aux_i = np.array([aux_variaveis.obtemValores()])
print(i_01.calculaSimulacao(aux_i))
print('--------------')


#%% Cria objetos
cuiaba_municipio = arisco.municipio('Cuiaba', aux_variaveis, aux_eventos, i_01)
sinop_municipio = arisco.municipio('Sinop', aux_variaveis, aux_eventos, i_01)
primavera_municipio = arisco.municipio('Primavera', aux_variaveis, aux_eventos, i_01)

## ------ ##
## Criar municípios a partir de arquivo


#%% Teste
print(cuiaba_municipio.calculaSimulacao())

print('--------------')
cuiaba_municipio.setaReferencias([11, 12])
print(cuiaba_municipio.obtemValores())
print(cuiaba_municipio.calculaMC(n=5))

#%% Cria conjunto de municipios e carrega dataframe
mt_municipios = arisco.municipios('municipios.xlsx', aux_variaveis, aux_eventos, i_01)

print(mt_municipios.obtemDadoMunicipio('Cuiaba'))

print('--------------')
print(mt_municipios.obtemDadosMunicipios())
mt_municipios.calculaSimulacoes()
print(mt_municipios.obtemDadosMunicipios())

print('--------------')
mt_municipios.calculaMC()
print(mt_municipios.obtemDadosMunicipios())

mt_municipios.gravaResultados('resultados.xlsx')
