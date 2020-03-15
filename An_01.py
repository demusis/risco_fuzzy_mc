import sys
import pandas as pd
import numpy as np
import seaborn as sns

import arisco

# Cria variáveis
aux_1_variavel = arisco.variavel('v1')
aux_1_variavel.setaValor(1)

aux_2_variavel = arisco.variavel('v2')
aux_2_variavel.setaValor(2)

aux_3_variavel = arisco.variavel('v3')
aux_3_variavel.setaValor(3)

# Cria eventos
aux_evento = arisco.eventoBernoulli(0.5)

aux_evento.insereVariavel(aux_1_variavel, 0.1)
aux_evento.insereVariavel(aux_2_variavel, 0.2)
aux_evento.insereVariavel(aux_3_variavel, 0.3)


# Roda ponderador
aux_evento.ponderaVariaveis()
aux_evento