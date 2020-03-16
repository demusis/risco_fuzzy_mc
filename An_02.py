# Teste da biblioteca de análise de risco
# Autor: Carlo Ralph De Musis

import sys
import pandas as pd
import numpy as np
import seaborn as sns
import arisco

# Cria variáveis
area_variavel = arisco.variavel('Area')
area_variavel.setaReferencia(10)

evaporacao_variavel = arisco.variavel('Evaporacao')
evaporacao_variavel.setaReferencia(12)


# Cria lista de variaveis
aux_variaveis = arisco.variaveis()

aux_variaveis.insereVariavel(area_variavel)
aux_variaveis.insereVariavel(evaporacao_variavel)

aux_variaveis.reiniciaVariaveis()


# Cria eventos associados a municípios do Mato Grosso
## Evento 01 Cuiabá
cuiaba_01_evento = arisco.eventoBernoulli(0.5) # p: 0.1

cuiaba_01_evento.insereVariavel(area_variavel, 0.11)
cuiaba_01_evento.insereVariavel(evaporacao_variavel, 0.21)

## Evento 02 Cuiabá
cuiaba_02_evento = arisco.eventoPoisson(2) # l: 2 

cuiaba_02_evento.insereVariavel(area_variavel, 0.12)
cuiaba_02_evento.insereVariavel(evaporacao_variavel, 0.22)

## Evento 03 Cuiabá
cuiaba_03_evento = arisco.eventoBernoulli(0.6) # p: 0.3

cuiaba_03_evento.insereVariavel(area_variavel, 0.13)
cuiaba_03_evento.insereVariavel(evaporacao_variavel, 0.23)

# Inicializa lista de eventos associada a Cuiaba.
cuiaba_eventos = arisco.eventos()

# Insere eventos
cuiaba_eventos.insereEvento(cuiaba_01_evento)
cuiaba_eventos.insereEvento(cuiaba_02_evento)
cuiaba_eventos.insereEvento(cuiaba_03_evento)

print('Referência')
aux_variaveis.apresentaVariaveis()

print('\r\nApós processar os eventos')
cuiaba_eventos.processaEventos()
aux_variaveis.apresentaVariaveis()

print('\r\nApós processar os eventos novamente')
cuiaba_eventos.processaEventos()
aux_variaveis.apresentaVariaveis()

print('\r\nReinicializa as variáveis')
aux_variaveis.reiniciaVariaveis()
aux_variaveis.apresentaVariaveis()

print('\r\nApós processar os eventos')
cuiaba_eventos.processaEventos()
aux_variaveis.apresentaVariaveis()


"""
Fuzzy
"""


# Carrega dados
df = pd.read_excel('Dados_brutos.xlsx', sheet_name='TOTAL') # Carrega a planilha com os dados
print(df.head())


# Cria Sistema fuzzy com a variável de saída "Impacto"
i_01 = arisco.sistemaFuzzy(0, 100, n_variavel="Impacto")


# Cria a variável de entrada "Área"
## Estatísticas descritivas
print(df.Km2.mean(), df.Km2.std(), 0, df.Km2.max())
print(df.Km2.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))
# sns.distplot(df.Km2) # histograma

## Cria variável fuzzy triangular
Area = arisco.variavelFTP(0, df.Km2.max(), 'Area', dados=df.Km2)

## Insere variável no sistema fuzzy
i_01.insereVariavel(Area)


# Cria a variável de entrada "Evaporacao"
## Estatísticas descritivas
print(df.Evaporacao.mean(), df.Evaporacao.std(), 0, df.Evaporacao.max())
print(df.Evaporacao.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))
# sns.distplot(df.Evaporacao) # histograma

## Cria variável fuzzy gaussiana
Evaporacao = arisco.variavelFGP(df.Evaporacao.min(), df.Evaporacao.max(), 'Evaporacao', dados=df.Evaporacao)
i_01.insereVariavel(Evaporacao)

# Cria conjunto básico de regras
i_01.basicoRegras()

# Inicializa simulação
i_01.inicializaSimulacao()

# Calculos de teste
print('--------------')
print(aux_variaveis.obtemVariaveis()[0].obtemReferencia(), ' ', aux_variaveis.obtemVariaveis()[1].obtemReferencia())
print('- Impacto ----')
# Área e evaporação.
aux_i = np.array([[aux_variaveis.obtemVariaveis()[0].obtemReferencia(), 
                   aux_variaveis.obtemVariaveis()[1].obtemReferencia()]])
print(i_01.calculaSimulacao(aux_i))
print('--------------')

print('--------------')
print(aux_variaveis.obtemVariaveis()[0].obtemValor(), ' ', aux_variaveis.obtemVariaveis()[1].obtemValor())
print('- Impacto ----')
# Área e evaporação.
aux_i = np.array([aux_variaveis.obtemValores()])
print(i_01.calculaSimulacao(aux_i))
print('--------------')

# Cálculo
# Cria município
cuiaba_municipio = arisco.municipios('Cuiaba', aux_variaveis, cuiaba_eventos, i_01)
print(cuiaba_municipio.calculaSimulacao())

print(cuiaba_municipio.calculaMC(n=500))