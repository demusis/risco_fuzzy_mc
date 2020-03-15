# Teste da biblioteca de análise de risco
# Autor: Carlo Ralph De Musis

import sys
import pandas as pd
import numpy as np
import seaborn as sns
import arisco

# Cria variáveis
aux_1_variavel = arisco.variavel('v1')
aux_1_variavel.setaReferencia(1)

aux_2_variavel = arisco.variavel('v2')
aux_2_variavel.setaReferencia(2)

aux_3_variavel = arisco.variavel('v3')
aux_3_variavel.setaReferencia(3)

# Cria lista de variaveis
aux_variaveis = arisco.variaveis()

aux_variaveis.insereVariavel(aux_1_variavel)
aux_variaveis.insereVariavel(aux_2_variavel)
aux_variaveis.insereVariavel(aux_3_variavel)

aux_variaveis.reiniciaVariaveis()

# Cria eventos
## Evento 01
aux_01_evento = arisco.eventoBernoulli(0.99) # p: 0.1


# aux_01_evento.insereVariavel(aux_variaveis.obtemVariavel(1), 0.11)
aux_01_evento.insereVariavel(aux_1_variavel, 0.11)
aux_01_evento.insereVariavel(aux_2_variavel, 0.21)
aux_01_evento.insereVariavel(aux_3_variavel, 0.31)

## Evento 02
aux_02_evento = arisco.eventoPoisson(20) # l: 2 

aux_02_evento.insereVariavel(aux_1_variavel, 0.12)
aux_02_evento.insereVariavel(aux_2_variavel, 0.22)
aux_02_evento.insereVariavel(aux_3_variavel, 0.32)

## Evento 03
aux_03_evento = arisco.eventoBernoulli(0.99) # p: 0.3

aux_03_evento.insereVariavel(aux_1_variavel, 0.13)
aux_03_evento.insereVariavel(aux_2_variavel, 0.23)
aux_03_evento.insereVariavel(aux_3_variavel, 0.33)


# Teste do ponderador
# aux_01_evento.ponderaVariaveis()
# aux_01_evento

aux_eventos = arisco.eventos()

# Insere eventos
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

# Carrega dados
df = pd.read_excel('Dados_brutos.xlsx', sheet_name='TOTAL') # Carrega a planilha com os dados
print(df.head())


# Cria Sistema fuzzy com a variável de saída "Impacto"
i_01 = arisco.sistemaFuzzy(0, 100, n_variavel="Impacto")


# Cria a variável de entrada "Área"
## Estatísticas descritivas
print(df.Km2.mean(), df.Km2.std(), 0, df.Km2.max())
print(df.Km2.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))
sns.distplot(df.Km2)

## Cria variável fuzzy triangular
Area = arisco.variavelFTP(0, df.Km2.max(), 'Area', dados=df.Km2)

## Insere variável no sistema fuzzy
i_01.insereVariavel(Area)


# Cria a variável de entrada "Área"
## Estatísticas descritivas
print(df.Evaporacao.mean(), df.Evaporacao.std(), 0, df.Evaporacao.max())
print(df.Evaporacao.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))
sns.distplot(df.Evaporacao)

## Cria variável fuzzy gaussiana
Evaporacao = arisco.variavelFGP(df.Evaporacao.min(), df.Evaporacao.max(), 'Evaporacao', dados=df.Evaporacao)
i_01.insereVariavel(Evaporacao)
