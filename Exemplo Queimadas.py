# Teste da biblioteca de análise de risco.
# Recorte de estudo de indice de queimadas.
# Autor: Carlo Ralph De Musis.
# Data: 31/03/2020.

#%% Carrega bibliotecas.
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import arisco

#%% Cria variáveis do estudo
## Os nomes das variáveis devem corresponder aos rótulos de coluna da planilha de entrada de dados.
area_variavel = arisco.variavel('Area')
area_variavel.setaReferencia(10) # Valor de referencia, o padrão é NaN.
evaporacao_variavel = arisco.variavel('Evaporacao')
evaporacao_variavel.setaReferencia(12)


#%% Cria lista de variaveis.
# Essa será a referência para o estudo.
queimadas_variaveis = arisco.variaveis()
queimadas_variaveis.insereVariavel(area_variavel)
queimadas_variaveis.insereVariavel(evaporacao_variavel)

#%% Cria eventos com distribuicoes e poderadores.
## Evento Chuva.
## A probabilidade de chover é de 50% (evento de Bernoulli).
chuva_evento = arisco.eventoBernoulli(0.5) 
## Se chover a evaporacao aumenta em 20%
chuva_evento.insereVariavel(evaporacao_variavel, 0.20)

## Evento raio.
## O número médio de raios/área: 2 (evento de Poisson).
raio_evento = arisco.eventoPoisson(2)
# A cada raio equivale a uma majoração na área de 15%
raio_evento.insereVariavel(area_variavel, 0.15)

## Evento incendiários.
aux_03_evento = arisco.eventoBernoulli(0.6) 

aux_03_evento.insereVariavel(area_variavel, 0.13)
aux_03_evento.insereVariavel(evaporacao_variavel, 0.23)
