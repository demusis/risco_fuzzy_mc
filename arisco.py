import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Varíável Fuzzy Gaussiana Padronizada -
class variavelFGP:
    # Inicializa VFGP
    def __init__(self, minm, maxm, n_variavel, media=None, dp=None, dados=None, passo=0.01, likert=3, tipo='antecedente'):
        # dados: vetor de dados de referência.
        # minm: valor mínimo.git init.
        # maxm: valor máximo.
        # n_variavel: nome da variavel.
        # passo: nível de discretização da variável fuzzy.
        # tipo: tipo de variável fuzzy.
        # likert: tamanho da escala.
    
        self.min = minm
        self.max = maxm

        # Calcula a média e desvio padrão a partir dos dados fornecidos,
        # caso contrário os estima a partir dos valores mínimo e máximo.
        try:
           self.media = dados.mean()
           self.dp = dados.std()
           media = self.media
           dp = self.dp
        except Exception:
           try: 
              self.media = media*1
              self.dp = dp*1
           except Exception:
              self.media = (minm+maxm)/2
              self.dp = ((maxm - minm)**2/12)**0.5
              media = self.media
              dp = self.dp

        
        if tipo == 'consequente':
            self.vf = ctrl.Consequent(np.arange(minm, maxm, passo), n_variavel)
        else:
            self.vf = ctrl.Antecedent(np.arange(minm, maxm, passo), n_variavel)

        if (likert==5):
            self.vf['muito baixo'] = fuzz.zmf(self.vf.universe, media - 5 * dp, media - 2 * dp)
            self.vf['baixo'] = fuzz.gaussmf(self.vf.universe, media - 2 * dp, dp)
            self.vf['medio'] = fuzz.gaussmf(self.vf.universe, media, dp)
            self.vf['alto'] = fuzz.gaussmf(self.vf.universe, media + 2 * dp, dp)
            self.vf['muito alto'] = fuzz.smf(self.vf.universe, media + 2 * dp, media + 5 * dp)
        elif (likert==3):
            self.vf['baixo'] = fuzz.zmf(self.vf.universe, minm, media)
            self.vf['medio'] = fuzz.gaussmf(self.vf.universe, media, dp)
            self.vf['alto'] = fuzz.smf(self.vf.universe, media, maxm)
        else: raise RuntimeError("Utilize escalas tipo likert com 3 ou 5 categorias.")

    # Apresenta o gráfico da variável fuzzy.
    def grafico(self):
        self.vf.view()

    # Retorna a média dos dados fornecidos na inicialização.
    def calculaMedia(self):
        return self.media

    # Retorna o desvio padrão dos dados fornecidos na inicialização.
    def calculaDP(self):
        return self.dp

    # Categorias linguísticas.
    def chaves(self):
        return list(self.vf.terms)


# Varíável Fuzzy Binomial Padronizada
class variavelFBP:
    # Inicializa VFBP
    def __init__(self, p, n_variavel, tipo='antecedente'):
        # p: probabilidade de evento favorável.
        # n_variavel: nome da variavel.
        # tipo: tipo de variável fuzzy.
        
        self.min = 0
        self.max = 1

        # Estima a média e o desvio padrão.
        self.media = p
        self.dp = (p * (1 - p)) ** 0.5

        if tipo == 'consequente':
            # O passo foi padronizado em 0.01.
            self.vf = ctrl.Consequent(np.arange(0, 1, 0.01), n_variavel)
        else:
            self.vf = ctrl.Antecedent(np.arange(0, 1, 0.01), n_variavel)

        # Escala Likert padronizada por 3 categorias para uma binomial normalizada.
        self.vf['baixo'] = fuzz.zmf(self.vf.universe, 0, p)
        self.vf['medio'] = fuzz.gaussmf(self.vf.universe, p, self.dp)
        self.vf['alto'] = fuzz.smf(self.vf.universe, p, 1)

    # Apresenta o gráfico da variável fuzzy.
    def grafico(self):
        self.vf.view()

    # Categorias linguísticas.
    def chaves(self):
        return list(self.vf.terms)

# Varíável Fuzzy Triangular Padronizada
class variavelFTP:
    # Inicializa VFTP.
    def __init__(self, minm, maxm, n_variavel, passo=0.01, tipo='antecedente', likert=3, dados=None):
        # dados: vetor de dados de referência.
        # minm: valor mínimo.
        # maxm: valor máximo.
        # n_variavel: nome da variavel.
        # passo: nível de discretização da variável fuzzy.
        # tipo: tipo de variável fuzzy.
        # likert: tamanho da escala.

        self.min = minm
        self.max = maxm

        # Calcula a média e desvio padrão a partir dos dados fornecidos,
        # caso contrário os estima a partir dos valores mínimo e máximo.        
        try:
           self.media = dados.mean()
           self.dp = dados.std()
        except Exception:
           self.media = (minm+maxm)/2
           self.dp = ((maxm - minm)**2/12)**0.5        
        
        if (tipo == 'consequente'):
            self.vf = ctrl.Consequent(np.arange(minm, maxm, passo), n_variavel)
        else:
            self.vf = ctrl.Antecedent(np.arange(minm, maxm, passo), n_variavel)

        if (likert==5):
            self.vf['muito baixo'] = fuzz.trimf(self.vf.universe, [minm, minm, dados.quantile(q=0.25, interpolation='linear')])
            self.vf['baixo'] = fuzz.trimf(self.vf.universe, np.asarray(dados.quantile(q=[0.05, 0.25, 0.50], interpolation='linear')))
            self.vf['medio'] = fuzz.trimf(self.vf.universe, np.asarray(dados.quantile(q=[0.25, 0.50, 0.75], interpolation='linear')))
            self.vf['alto'] = fuzz.trimf(self.vf.universe, np.asarray(dados.quantile(q=[0.50, 0.75, 0.95], interpolation='linear')))
            self.vf['muito alto'] = fuzz.trimf(self.vf.universe, [dados.quantile(q=0.75, interpolation='linear'), maxm, maxm])
        elif (likert==3):
            self.vf['baixo'] = fuzz.trimf(self.vf.universe, [minm, minm, dados.quantile(q=0.50, interpolation='linear')])
            self.vf['medio'] = fuzz.trimf(self.vf.universe, [minm, dados.quantile(q=0.50, interpolation='linear'), maxm])
            self.vf['alto'] = fuzz.trimf(self.vf.universe, [dados.quantile(q=0.50, interpolation='linear'), maxm, maxm])
        elif (likert==2):
            self.vf['baixo'] = fuzz.trimf(self.vf.universe, [minm, minm, maxm])
            self.vf['alto'] = fuzz.trimf(self.vf.universe, [minm, maxm, maxm])
        else: raise RuntimeError("Utilize escalas tipo likert com 2, 3 ou 5 categorias.")

    # Apresenta o gráfico da variável fuzzy.
    def grafico(self):
        self.vf.view()

    # Retorna a média dos dados fornecidos na inicialização.
    def calculaMedia(self):
        return self.media

    # Retorna o desvio padrão dos dados fornecidos na inicialização.
    def calculaDP(self):
        return self.dp

    # Categorias linguísticas.
    def chaves(self):
        return list(self.vf.terms)


# Sistema Fuzzy.
class sistemaFuzzy:
    # Inicializa sistema fuzzy.
    def __init__(self, minm, maxm, n_variavel, likert=3):
        self.min = minm
        self.max = maxm

        # Lista vazia de variáveis fuzzy.
        self.l_v_f = []

        # Define variável consequente.
        self.c_v_f = variavelFGP(minm, maxm, n_variavel, tipo='consequente', likert=likert)

        # Lista vazia de regras fuzzy.
        self.l_r_f = []

    # Insere variável.
    def insereVariavel(self, v_f):
        self.l_v_f.append(v_f)

    # Insere regra
    def insereRegra(self, r_f):
        self.l_r_f.append(r_f)

    # Apresenta gráficos de fuzificação das variáveis.
    def graficosVariaveis(self):
        for aux_v_f in self.l_v_f:
            aux_v_f.grafico()
        self.c_v_f.grafico()

    # Cria e insere conjunto básico de regras.
    def basicoRegras(self):
        for aux_v_f in self.l_v_f:
            for chave in aux_v_f.chaves():
                self.insereRegra(ctrl.Rule(aux_v_f.vf[chave],
                                           self.c_v_f.vf[chave]))
        # print(self.l_r_f)

    # Inicializa sistema e simulação.
    def inicializaSimulacao(self):
        self.ctrl_v_f = ctrl.ControlSystem(self.l_r_f)
        self.sim_v_f = ctrl.ControlSystemSimulation(self.ctrl_v_f) # Cria simulação
        # self.ctrl_v_f.view()

    # Lista variáveis antecedentes.
    def listaAntecedentes(self):
        aux = []
        for aux_v_f in self.l_v_f:
            aux.append(aux_v_f.vf.label)
        return aux

    # Calcula a simulaçção para um vetor de entrada.
    def calculaSimulacao(self, reg): 
        res = []
        for aux_reg in reg:
            aux = dict(zip(self.listaAntecedentes(), aux_reg))
            self.sim_v_f.inputs(aux) # Fornece valores
            self.sim_v_f.compute() # Calcula
            aux_res = self.sim_v_f.output[self.c_v_f.vf.label]
            if aux_res < self.c_v_f.min:
                aux_res = self.c_v_f.min
            elif aux_res > self.c_v_f.max:
                aux_res = self.c_v_f.max
            res.append(aux_res)
        return res
    
    # Efetua n simulações e retorna o resultado.
    def mcSimulacao(self, r=None, n=500, media=None): 
        # r: matriz de correlações.
        # n: número de simulações.
        # Vetor de médias.
        
        aux_media = []
        aux_s = []
        
        # Caso não seja fornecido r utiliza uma matriz unitária.
        if r is None:
            r = np.eye(len(self.l_v_f), dtype=np.int64) # Matriz unitária.

        for aux_v_f in self.l_v_f: # varre todas as variáveis fuzzy.
            
            # Se não for fornecido um vetor de médias compile uma lista através das
            # variáveis fuzzy.
            if media is None:
                aux_media.append(aux_v_f.media)
            aux_s.append(aux_v_f.dp) # Compila vetor de DPs.

        if media is None:
            aux_media = np.array(aux_media) # Converte lista de médias para array.
        else:
            aux_media = np.array(media)

        # Cria matriz com n elementos considerando a distribuição normal e a matriz 
        # de covariâncias.
        aux_s = np.diagflat(aux_s)
        cov = aux_s @ r @ aux_s
        aux_mc = np.random.multivariate_normal(aux_media, cov, size=n)

        return self.calculaSimulacao(aux_mc)

    # Efetua simulação e retorna percentís bilaterais para um determinado alfa.
    def icMCSimulacao(self, r=None, n=500, alfa=0.05):
        ic = np.quantile(self.mcSimulacao(r, n),
                         [alfa / 2, .5, 1 - alfa / 2])
        return ic


# Variável
class variavel:
    # Inicializa variável
    def __init__(self, n_variavel):
        # n_variavel: nome da variavel.
        self.n_variavel = n_variavel
        self.referencia_valor = float('nan')   # NaN ("not a number")
        self.valor = float('nan')   # NaN ("not a number")

    # Altera valor corrente
    def setaValor(self, valor):
        self.valor = valor

    # Altera valor de referência
    def setaReferencia(self, valor):
        self.referencia_valor = valor
        self.valor = valor

    # Retorna referência.
    def obtemReferencia(self):
        return self.referencia_valor

    # Retorna valor corrente.
    def obtemValor(self):
        return self.valor

    # Reinicia o valor corrente
    def reiniciaValor(self):
        self.valor = self.referencia_valor

    # Apresenta variável
    def apresentaVariavel(self):
        print('Variável: ', self.n_variavel, ', Ref.: ', self.obtemReferencia(), ', Valor: ', self.obtemValor())   


class variaveis:
    # Inicializa lista de variaveis.
    def __init__(self):
        self.l_variaveis = []
        self.dados = None

    # Insere variavel.
    def insereVariavel(self, variavel):
        self.l_variaveis.append(variavel)

    # Reinicia variaveis
    def reiniciaVariaveis(self):
        for aux_variavel in self.l_variaveis:
            aux_variavel.reiniciaValor()

    # Seta referências
    def setaReferencias(self, referencias):
        for aux_n, aux_variavel in enumerate(self.l_variaveis):
            aux_variavel.setaReferencia(referencias[aux_n])

    # Obtêm variáveis
    def obtemVariaveis(self):
        return self.l_variaveis

    # Obtêm variável
    def obtemVariavel(self, num_variavel):
        return self.l_variaveis[num_variavel]

    # Obtêm valor
    def obtemValor(self, num_variavel):
        return self.l_variaveis[num_variavel].obtemValor()

    # Obtêm valores
    def obtemValores(self):
        aux_valores = []
        for aux_variavel in self.l_variaveis:
            aux_valores.append(aux_variavel.obtemValor())
        return aux_valores

    # Apresenta variaveis
    def apresentaVariaveis(self):
        for aux_variavel in self.l_variaveis:
            aux_variavel.apresentaVariavel()


class evento:
    # Inicialisa evento base
    def __init__(self):
        # Lista de variáveis
        self.l_variaveis = []

    # Insere na lista uma variável afetada pelo evento.
    def insereVariavel(self, variavel, ponderador):
        aux_evento_ponderado = {'variavel': variavel, 'ponderador': ponderador}
        self.l_variaveis.append(aux_evento_ponderado)        

    # Simula um evento
    def simulaEvento(self):
        return 0 # Padrão: evento impossível

    # Simula o evento e pondera o seu efeito nas variáveis inseridas
    def ponderaVariaveis(self):
        oc_evento = self.simulaEvento()
        if oc_evento!=0: 
            for aux_variavel in self.l_variaveis:
                aux_variavel['variavel'].setaValor(aux_variavel['variavel'].obtemValor()*
                                                   (1 + aux_variavel['ponderador'])*
                                                   oc_evento)


# Evento aleatório conforme a distribuição de Bernoulli.
class eventoBernoulli(evento):
    # Inicializa evento
    def __init__(self, p):
        # p: probabilidade de um evento favorável.
        super().__init__()
        self.p = p
    
    # Simula evento binomial
    def simulaEvento(self):
        return np.random.binomial(1, p=self.p)


# Evento aleatório conforme a distribuição de Poisson.
class eventoPoisson(evento):
    # Inicializa evento.
    def __init__(self, l):
        # l: média de eventos por episódio.
        super().__init__()
        self.l = l
    
    # Simula o número de eventos favoráveis
    def calculaF(self):
        return np.random.poisson(self.l, 1)


# Lista de eventos.
class eventos:
    # Inicializa lista de eventos.
    def __init__(self):
        self.l_eventos = []

    # Insere evento.
    def insereEvento(self, evento):
        self.l_eventos.append(evento)

    # Processa eventos
    def processaEventos(self):
        for aux_evento in self.l_eventos:
            aux_evento.ponderaVariaveis()

class municipio:       
    # Inicializa um município
    def __init__(self, nome, variaveis, eventos, sistema_fuzzy):
        self.nome = nome
        self.eventos = eventos
        self.sistema_fuzzy = sistema_fuzzy
        self.variaveis = variaveis

    # Seta referências
    def setaReferencias(self, x):
        self.variaveis.setaReferencias(x)

    # Obtêm valores
    def obtemValores(self):
        return self.variaveis.obtemValores()

    # Calcula uma simulação
    def calculaSimulacao(self):
        aux_sf = np.array([self.variaveis.obtemValores()])
        return self.sistema_fuzzy.calculaSimulacao(aux_sf)

    # Monte Carlo
    def calculaMC(self, n=500, alfa=0.05):
        res_mc = []
        for r in range(n+1):
            self.variaveis.reiniciaVariaveis()
            self.eventos.processaEventos()
            res_mc.append(self.calculaSimulacao())
        return np.quantile(res_mc,
                           [alfa / 2, .5, 1 - alfa / 2])


class municipios:
    # Carrega a planilha com os dados
    def __init__(self, arquivo):
        self.dados_municipios = pd.read_excel(arquivo)
        self.dados_municipios.set_index('nome', inplace=True)
        self.l_municipios = []

    # Obtêm dados de um município
    def obtemDadoMunicipio(self, nome_municipio):
        return self.dados_municipios.loc[nome_municipio].values.flatten().tolist()

    # Obtêm dados dos municípios
    def obtemDadosMunicipios(self):
        return self.dados_municipios

    #  Insere município
    def insereMunicipio(self, municipio):
        self.l_municipios.append(evento)

    # Calcula uma coluna nova
    def calculaSimulacao(self):
        def soma(row):
            return row['area'] + row['evaporacao']
        self.dados_municipios['soma'] = self.dados_municipios.apply(lambda row: soma(row), axis=1)

