#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:59:13 2017

@author: carlos
"""

import requests                       # HTTP 
from bs4 import BeautifulSoup         # Interpretador de código fonte
import pandas as pd                   
from datetime import datetime         

# A função bmf_taxas() toma como entrada as variáveis d = dia, m = mês e y = ano.
def bmf_taxas(d, m, y):              

    # datetime() converte as variáveis de entrada na estrutura datetime
    date = datetime(y, m, d)          
    
    # .strftime() manipula a estrutra para de obter no formato desejado
    date1 = datetime.strftime(date, '%d/%m/%Y')   
    
    date2 = datetime.strftime(date, '%Y%m%d')
    
    # Página de onde serão extraídos os dados:
    url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data='+date1+'&Data1='+date2+'&slcTaxa=PRE'
    
    # .get() faz o request da url para o servidor
    response = requests.get(url)
    
    # A função BeautifulSoup converte o conteúdo da fonte da página requisitada em um objeto bs4, que pode ser manipulado com facilidade
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Cria-se três listas que serão preenchidas com os valores extraídos da página
    dc = []
    di252 = []
    di360 = []
    
    # O código fonte html começa a mostrar os dados na tag número 9, portanto começa-se a incrementar a partir da nona tag
    i = 9
    
    # Variável usada para sinalizar quando parar o loop
    result = None
    
    # O loop ser executado enquanto result = None
    while result is None:
        
        try:
        
            tmp0 = int(soup.find_all('td')[i].get_text())
            tmp1 = soup.find_all('td')[i+1].get_text()[2:]
            tmp2 = soup.find_all('td')[i+2].get_text()[2:]
            
            # os proximos valores requisitados estarão deslocados em três tags na estrutura, portanto incrementa-se 3
            i = i+3
            
            
            dc.append(int(tmp0))
            di252.append(float(tmp1.replace(',','.')))
            di360.append(float(tmp2.replace(',','.')))
        
        # Caso try retorne um erro, result = 1. Isso far com que o loop pare de executar
        except:
            result = 1
        
    # Os dados são armazenados em um dicionário
    dic = {'dias corridos':dc , 'yield_252' : di252 , 'yield_360':di360}
    
    # De um dicionário, os dados são convertidos em uma DataFrame
    data = pd.DataFrame(dic)
    data.index = data['dias corridos']
    del data['dias corridos']
   
    file_name = 'di_' + date2 + '.csv'
   
    # Os dados são armazenados no formato csv, usando-se o método .to_csv()
    data.to_csv(file_name)
    
    return data
