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
aux_01_evento = arisco.eventoBernoulli(0.1) # p: 0.1

aux_01_evento.insereVariavel(aux_1_variavel, 0.11)
aux_01_evento.insereVariavel(aux_2_variavel, 0.21)
aux_01_evento.insereVariavel(aux_3_variavel, 0.31)

## Evento 02
aux_02_evento = arisco.eventoPoisson(2) # l: 2 

aux_02_evento.insereVariavel(aux_1_variavel, 0.12)
aux_02_evento.insereVariavel(aux_2_variavel, 0.22)
aux_02_evento.insereVariavel(aux_3_variavel, 0.32)

## Evento 03
aux_03_evento = arisco.eventoBernoulli(0.3) # p: 0.3

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

# Processa eventos
aux_eventos.processaEventos()
