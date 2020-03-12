#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import numpy as np
import arisco
import seaborn as sns

sns.set_style('darkgrid')
# Teste

# In[2]:


print(sys.version)


# In[3]:


print(np.version.version) # É necessário a versão >1.16.2


# In[4]:


df = pd.read_excel('Dados_brutos.xlsx', sheet_name='TOTAL') # Carrega a planilha com os dados
df.head()


# In[5]:


i_01 = arisco.SF(0, 100, n_variavel="Impacto")
# p_01 = arisco.SF(0.5, 0.25, 0, 1, "Probabilidade")


# In[6]:


print(df.Km2.mean(), df.Km2.std(), 0, df.Km2.max())

print(df.Km2.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))

sns.distplot(df.Km2)

Area = arisco.VFTP(df.Km2, 0, df.Km2.max(), 'Area')

i_01.insere_var(Area)


# In[7]:


print(df.Combustivel.mean(), df.Combustivel.std(), 0, 1)

print(df.Combustivel.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))

sns.distplot(df.Combustivel)

Combustivel = arisco.VFTP(df.Combustivel, 0, 1, 'Combustivel')

i_01.insere_var(Combustivel)


# In[8]:


print(df.Vizinhanca.mean(), df.Vizinhanca.std(), 0, df.Vizinhanca.max())

print(df.Vizinhanca.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))

sns.distplot(df.Vizinhanca)

Vizinhanca = arisco.VFTP(df.Vizinhanca, 0, 1, 'Vizinhanca', likert=2)

i_01.insere_var(Vizinhanca)


# In[9]:


print(df.Gestao.mean(), df.Gestao.std(), 0, df.Gestao.max())

print(df.Gestao.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))

sns.distplot(df.Gestao)

Gestao = arisco.VFTP(df.Gestao, 0, 1, 'Gestao')

i_01.insere_var(Gestao)


# In[10]:


print(df.Relevo.mean(), df.Relevo.std(), df.Relevo.min(), df.Relevo.max())

# relevo = arisco.VFGP(df.Relevo.mean(), df.Relevo.std(), df.Relevo.min(), df.Relevo.max(), 'relevo')
# i_01.insere_var(relevo)


# In[11]:


print(df.Renda.mean(), df.Renda.std(), 0, df.Renda.max())

print(df.Renda.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))

sns.distplot(df.Renda)

Renda = arisco.VFTP(df.Renda, 0, 1, 'Renda')

i_01.insere_var(Renda)


# In[12]:


print(df.Vento.mean(), df.Vento.std(), df.Vento.min(), df.Vento.max())

#vento = arisco.VFGP(df.Vento.mean(), df.Vento.std(), df.Vento.min(), df.Vento.max(), 'vento')
#i_01.insere_var(vento)


# In[13]:


print(df.Precipitacao.mean(), df.Precipitacao.std(), df.Precipitacao.min(), df.Precipitacao.max())

# precipitacao = arisco.VFGP(df.Precipitacao.mean(), df.Precipitacao.std(), df.Precipitacao.min(), df.Precipitacao.max(), 'precipitacao')
# i_01.insere_var(precipitacao)


# In[14]:


print(df.Pressao.mean(), df.Pressao.std(), df.Pressao.min(), df.Pressao.max())

Pressao = arisco.VFGP(df.Pressao.min(), df.Pressao.max(), 'Pressao', dados=df.Pressao)
i_01.insere_var(Pressao)


# In[15]:


print(df.Evaporacao.mean(), df.Evaporacao.std(), 0, df.Evaporacao.max())

print(df.Evaporacao.quantile(q=[0.05, 0.25, 0.50, 0.75, 0.95], interpolation='linear'))

sns.distplot(df.Evaporacao)

Evaporacao = arisco.VFGP(df.Evaporacao.min(), df.Evaporacao.max(), 'Evaporacao', dados=df.Evaporacao)

i_01.insere_var(Evaporacao)


# In[16]:


i_01.graficos_var()


# In[17]:


i_01.basico_regras()


# In[18]:


i_01.inicializa_simulacao()


# In[19]:


print('- Impacto ----')
# Área, combustível, vizinhança, gestão, renda, pressão e evaporação.
aux_i = np.array([[10, 0.3, 0.2, 0.2, 0.4, 992, 12]])
print(i_01.calcula_simulacao(aux_i))
print('-----')


# In[20]:


# MC
ic_i_01 = i_01.ic_mc_simulacao()

print(ic_i_01)

