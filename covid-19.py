import arisco
import numpy as np
#
# Cria variáveis para MMC.
#
# O valor de referencia é o inicial.
ce_var = arisco.variavel('Classificacao epidemiológica') # classificacao_epidemiologica.
ce_var.setaReferencia(True)

va_var = arisco.variavel('Velocidade de avanço de casos novos') # n_va.
va_var.setaReferencia(0)

r_var = arisco.variavel('Média móvel do número de reprodução básico') # r_mm7.
r_var.setaReferencia(1)

infectados_var = arisco.variavel('Possui infectados ativos') # infectados.
infectados_var.setaReferencia(False)

# Cria lista de variaveis.
covid_variaveis = arisco.variaveis()

covid_variaveis.insereVariavel(ce_var)
covid_variaveis.insereVariavel(va_var)
covid_variaveis.insereVariavel(r_var)
covid_variaveis.insereVariavel(infectados_var)

# Reinicia as variáveis para o seu valor re referência.
# Redundante.
covid_variaveis.reiniciaVariaveis()

# Cria evento - entrada de infectado de fora.
infectado_evento = arisco.eventoBernoulli(0.0) # p: 0.0

# Inicializa lista de eventos.
covid_eventos = arisco.eventos()

# Insere evento.
covid_eventos.insereEvento(infectado_evento)


# Testa variáveis.
print('Referência')
covid_variaveis.apresentaVariaveis()



#
# Cria Sistema fuzzy com a variável de saída.
#
covid_risco = arisco.sistemaFuzzy(0, 100, n_variavel="Risco")

# Cria variáveis fuzzy.
ce_fuzzy = arisco.variavelFBP(0.5, 'Classificacao epidemiológica')
vc_fuzzy = arisco.variavelFTP(-0.1, 2.1, 'Velocidade de avanço de casos novos')
r_fuzzy = arisco.variavelFTP(0, 2.1, 'Média móvel do número de reprodução básico')
nia_fuzzy = arisco.variavelFBP(0.5, 'Número de infectados ativos')

# Insere variáveis fussy no sistema.
covid_risco.insereVariavel(ce_fuzzy)
covid_risco.insereVariavel(vc_fuzzy)
covid_risco.insereVariavel(r_fuzzy)
covid_risco.insereVariavel(nia_fuzzy)

covid_risco.graficosVariaveis()

# Cria conjunto básico de regras
covid_risco.basicoRegras()

# Inicializa simulação
covid_risco.inicializaSimulacao()


print('--------------')
print(covid_variaveis.obtemVariaveis()[0].obtemReferencia(), ' ', 
      covid_variaveis.obtemVariaveis()[1].obtemReferencia(), ' ',
      covid_variaveis.obtemVariaveis()[2].obtemReferencia(), ' ',
      covid_variaveis.obtemVariaveis()[3].obtemReferencia())

print('- Risco ----')
print(covid_risco.calculaSimulacao([[True, 0, 1, False]]))




# Carrega dados dos municipios.
# mt_municipios = arisco.municipios('2020-06-14 - bi_aglomerados.xlsx', aux_variaveis, aux_eventos, i_01)