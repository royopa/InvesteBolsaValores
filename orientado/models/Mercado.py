from utils import data_utils
from utils import downloader

import numpy as np


class Mercado(object):

    def __init__(self, nome):
        self.nome = nome
        self.codigo = 'INDEX_BVSP'
        self.acoes = self.get_composicao()
        self.pontuacoes = self.get_pontuacoes()
        self.retorno_diario = self.calcular_retorno_diario()
        self.retorno_esperado = self.get_retorno_esperado()

    def get_pontuacoes(self):
        pontuacoes = data_utils.ler_arquivo_csv(self.codigo)
        if not pontuacoes:
            print('Baixando ' + self.codigo)
            pontuacoes = downloader.baixar_pontuacoes_mercado(self.codigo)
            data_utils.escrever_csv(self.codigo, pontuacoes)
        return pontuacoes

    '''
    Retornando uma lista com os nomes das acoes
    '''
    def get_composicao(self):
        if self.nome == 'IBOVESPA':
            composicao = data_utils.ler_arquivo_txt('COMPOSIÇÃO IBOVESPA')
            if not composicao:
                print('Baixando Composição Ibovespa')
                composicao = scrapper.baixar_composicao_carteira_ibovespa()
                data_utils.escrever_lista_em_txt('COMPOSIÇÃO IBOVESPA', composicao)
        return composicao

    def calcular_retorno_diario(self):
        retorno_diario = np.zeros(len(self.pontuacoes)-1)
        for i in range(len(self.pontuacoes)-1):
            retorno_diario[i] = (self.pontuacoes[i+1] - self.pontuacoes[i])/self.pontuacoes[i]
        return retorno_diario

    def get_retorno_esperado(self):
        retorno_esperado_diario = np.mean(self.retorno_diario)
        return (1 + retorno_esperado_diario)**30
