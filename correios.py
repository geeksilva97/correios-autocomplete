import urllib3
import json
from bs4 import BeautifulSoup


def get_localidades(query):
    localidades = {
    'localidades': [],
    'total': 0
    }

    if len(query) < 5:
        return localidades


    try:
        http = urllib3.PoolManager()
        # query = 'Rua Professor Osorio Uchoa'
        r = http.request('POST', 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm', fields={'relaxation': query, 'semelhante': 'N', 'tipoCEP': 'LOG'})
        soup = BeautifulSoup(r.data, 'html.parser')
        table = soup.find('table', {'class': 'tmptabela'})

        trs = table.find_all('tr')[1:]


        for tr in trs:
            td = tr.find_all('td')
            data = {}
            data['logradouro'] = td[0].text
            data['bairro'] = td[1].text
            data['cidade'] = td[2].text
            data['cep'] = td[3].text

            localidades['localidades'].append(data)
        localidades['total'] = len(localidades['localidades'])
        return localidades
    except:
        return localidades

