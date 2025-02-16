#!/usr/bin/env python
# coding: utf-8

# In[34]:


# html.parser traduz o HTML bruto em uma árvore de objetos Python que pode ser navegada e manipulada.
from bs4 import BeautifulSoup
import requests
import re

# conectar com o site
link = "https://coinmarketcap.com/"
requisicao = requests.get(link)
site = BeautifulSoup(requisicao.text, "html.parser") 
#print(site.prettify()) # o método prettify organiza a visualização das informações

tbody = site.find("tbody") # tbody é o elemento dentro da estrutura html onde contem a tabela com as informações que iremos extrair.
linhas = tbody.find_all("tr") # tr = linha em uma tbody
moedas = {}
for linha in linhas:
    try:
        nome = linha.find(class_="iPbTJf").text
        codigo = linha.find(class_="coin-item-symbol").text
        valores = linha.find_all(string=re.compile("\$")) # aqui ele pegou todos os valores da linha que começam com $, usando regular expressions.
        preco = valores[0] # indice 0 pois é o retorno do print(valores), uma lista, onde indice 0 corresponde ao preço.
        percentuais = linha.find_all(string=re.compile("%"))
        
        for i, percentual in enumerate(percentuais): # MUITO IMPORTANTE - condição para detecção de números negativos.
            if "ivvJzO" in percentual.parent["class"]: # a classe ivvJzO é quando o preço está negativo
                percentuais[i] = "-" + str(percentual) # atribui o sinal de negativo na string do percentual, para transformá-lo em negativo.

        var_1h = percentuais[0] # indice de acordo com a lista retornada através do print(percentuais).
        var_24h = percentuais[1]
        var_7d = percentuais[2]
        
        market_cap = valores[2]
        volume = valores[3]
        dic = {"nome": nome, "codigo": codigo, "preco": preco, "market_cap": market_cap, "volume": volume,
              "var_1h": var_1h, "var_24h": var_24h, "var_7d": var_7d} # construção de nosso dicionário para ser o padrão de entega da requisição.
        moedas[nome] = dic # cria o item pelo nome caso não exista em nosso dicionário.
    except AttributeError:
        break
print(moedas)


import pandas as pd

# Remover a chave "nome" de cada dicionário interno (pois já está como chave principal)
for moeda in moedas:
    moedas[moeda].pop("nome", None)  # Remove "nome" se existir

# Criar DataFrame sem duplicação
df_moedas = pd.DataFrame.from_dict(moedas, orient="index").reset_index()

# Renomear a coluna "index" para "nome" (já que a chave do dicionário é o nome da moeda)
df_moedas.rename(columns={"index": "nome"}, inplace=True)

display(df_moedas)


# In[ ]:




