#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Uso:

    python pesquisa.py -i /pastacomarquivos/ -p palavra1:palavra2

    Pesquisa recursivamente a pasta de origem por arquivos que contenham as palavras
    informadas.

Parametros:

    -i    pasta onde estão os arquivos que serão pesquisados.
    -p    uma ou mais palavras para pesquisa. Separar palavras por ":"
    -m    quantidade de palavras que devem ser encontradas. Se não informado,
          o valor padrão é 1 (um).

Exemplos:

    python pesquisa.py -i /meustextos/ -p shell:dicas -m 2
    python pesquisa.py -i /meustextos/ -p carro:automovel:veiculo -m 1

'''

__author__ = 'Vicente Lima'
__version__ = '0.1'

import sys
import os


def paramPalavras(num):
    '''
    lista de palavras separadas por 2 pontos
    '''
    listaPalavras = sys.argv[num + 1]
    #print 'listapalavras: ', listaPalavras
    return listaPalavras.split(':')


def paramString(num):
    '''
    path do local onde estao os arquivos
    '''
    return sys.argv[num + 1]


def paramTipoMatch(num):
    '''
    '''
    retorno = 1
    try:
        retorno = int(sys.argv[num + 1])
    except:
        print 'erro -> o parametro (-m) não é um inteiro:', sys.argv[num + 1]
        exit(1)

    return retorno


parametros = {'-i': paramString,
              '-p': paramPalavras,
              '-m': paramTipoMatch
              }


def pesquisarNoArquivo(path, file, listapalavras, matchminimo):
    arq = open(path + '/' + file, 'r')
    achou = []
    conteudo = arq.read().upper()
    arq.close()

    for palavra in listapalavras:
        if conteudo.find(palavra.upper()) > 0:
            achou.append(palavra)

    arq.close()
    if len(achou) >= matchminimo:
        print 'arquivo: ', achou , arq.name


def verificarValidarParametros():
    #assegura que "-m" (quantidade minima de match) eh ao menos igual a quantidade de palavras
    if parametros['-m'] > len(parametros['-p']):
        parametros['-m'] = len(parametros['-p'])

    #verifica se "-i" (caminho de entrada) eh valido
    if not os.path.isdir(parametros['-i']):
        print 'erro -> caminho informado nao existe: ', parametros['-i']
        exit()


if __name__ == '__main__':

    if '-h' in sys.argv:
        print __doc__
        exit(0)

    for num, arg in enumerate(sys.argv):
        if parametros.keys().__contains__(arg):
            retorno = parametros[arg](num)
            parametros[arg] = retorno

    verificarValidarParametros()

    # mostrar parametros que serão usados
    for param in parametros.keys():
        print param, ' : ', parametros[param]

    palavras = parametros['-p']
    origem = parametros['-i']
    matchminimo = parametros['-m']

    #print parametros
    print '-------------'

    # if len(sys.argv) == 1:
    #     print 'Informar caminho para pesquisa'
    #     exit(1)
    #
    # else:
    #     origem = sys.argv[1]

    #exit()



    for raiz, subpastas, arquivos in os.walk(origem):
        #print 'raiz:', raiz
        #print 'subpastas: ', subpastas
        for arquivo in arquivos:
            #print 'arquivo: ', raiz, arquivo
            pesquisarNoArquivo(raiz, arquivo, palavras, matchminimo)

