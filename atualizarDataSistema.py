#!/usr/bin/python
# -*- coding: UTF8 -*-

'''
Uso: atualizarDataSistema.py
     ou python atualizarDataSistema.py
     
  Atualiza a hora do sistema (linux), usando comando (date),
  obtendo a data e hora atual no site (www.horacerta.com.br),
  usando proxy.
  Para alterar a data o programa deve ser executado como root.
  
Argumentos:  
  
  -v        Verificar data do sistema e data do site.
            Não altera a data do sitema.
            
    --help  mostra esta ajuda e finaliza
    
  
Status de Saida:

  (0) OK
  (1) erro no formato da data obtida no site
  (2) erro ao tentar alterar a hora local do sistema
  (123) erro ao acessar o site horacerta
'''

__author__ = "vicente lima @ brasilia.df"
__date__ = "$6/05/2014 16:21:11$"

import sys
import urllib2
import string
import subprocess
import datetime
import logging
import time


log = logging.getLogger('atualizarDataSistema')
#log.setLevel(logging.DEBUG)
log.setLevel(logging.ERROR)
#formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)



def obterDataHoraNoSite(url='http://www.horacerta.com.br/index.php?city=sao_paulo'):
    '''
    ==================================================
    Configurar proxy para chamada na internet
    consultar site da hora certa
    Procurar uma linha especifica com a data/hora atual
    Retornar a data e hora
    ==================================================
    '''
    
    ''' este proxy foi implementado com cntlm que ja' resolve a autenticação.'''
    proxy = ['http','127.0.0.1:8108']
    ''' Pagina retornada pelo site '''
    pagina = ''
    
    
    proxy = urllib2.ProxyHandler({proxy[0] : proxy[1]})
    opener = urllib2.build_opener(proxy)
    
    
    try:
        f = opener.open(url)
        data_sistema = datetime.datetime.today()
        log.debug('Site acessado: ' + url)
        # ler linha a linha da resposta
        pagina = f.readlines()
    except Exception, e:
        log.error('Problema ao acessar o site ' + url)
        #print '\n Um erro foi encontrado:', url
        log.error(str(e))
        exit(123)
        
    
    log.debug('Procurar data no retorno do site')
    ''' String com a data, como retornado pelo site '''
    codigo_data = ''
    
    for l in pagina:
        # procurar uma linha com a data atual  
        indice = string.find(l, '<input name="initial_date" type="hidden"')
        #<input name="initial_date" type="hidden" value="2014 5 6 15 38 48" />
        #                                                2014 5 12 10 03 11
        if indice != -1:
            log.debug('Linha retornada com a data: '+ l)
            # pegar apenas a data
            codigo_data = l[indice+48:len(l)-6]
            break
            #2014 5 6 15 46
            #print len(codigo_data)
    
    ''' lista com partes da data (ano,mes,dia,hora,minuto,segundo) '''
    list_data = codigo_data.split(' ')
    log.debug('String obtida no site: ' + str(list_data))
    try:
        #datetime.datetime.strptime('2011-07-15 13:00:00', '%Y-%m-%d %H:%M:%S')
        dataYMDHMS = list_data[0]+'-'+ list_data[1]+'-'+list_data[2]+ ' '+ list_data[3]+':'+ list_data[4] + ':' + list_data[5] 
        data_site = datetime.datetime.strptime(dataYMDHMS, '%Y-%m-%d %H:%M:%S')
        log.debug('A data recebida eh valida')
        #print 'data correta: ', d
        #raise Exception('Teste')
    except Exception, e:
        log.error('Falha no formato da data obtida: (Y-m-D H:M:S) '+ dataYMDHMS)
        log.error(str(e))
        raise e

    
    #print 'print', d
    #return data_site
    return [data_site, data_sistema]
    
    


def main():
    '''
    ==================================================
    Montar a data para uso distintos: 
    Testar se a data é válida. (se erro, mostra e sai)
    Obter data do sistema.
    Executar comando para alterar data do sistema.
    ==================================================
    '''

    try:
        datas = obterDataHoraNoSite('http://www.horacerta.com.br/index.php?city=sao_paulo')
        data_site = datas[0]
        data_sistema = datas[1]
    except Exception, erro:
        exit(1)
    
    log.debug('Obter data do sistema')

    #time.sleep(3)

    #data_sistema = datetime.datetime.today()
    
    print '\n  Data/hora do sistema:', data_sistema
    print '  Data/hora do site...:', data_site, '\n'
    
        
    if data_site > data_sistema:
        diferenca = data_site - data_sistema
    else:
        diferenca = data_sistema - data_site
        
    print '  Diferença em segundos: ' + str(diferenca.seconds)
    
    if '-v' in sys.argv:
        exit(0)

    # @type data_site 
    log.debug('Executando o comando: date -s '+ data_site.strftime('%Y-%m-%d %H:%M:%S'))

    print '\nAlterando a data do sistema -------------'
    resultado = subprocess.call(['date', '-s', ''+ data_site.strftime('%Y-%m-%d %H:%M:%S')])
    print '-----------------------------------------\n'
    
    if resultado == 0:
        print 'Data alterada com sucesso'
        print '  Nova data do sistema: ', datetime.datetime.today()
    else:
        log.error('Não foi possível alterar a data do sistema')
        log.error(' Verifique permissão do usuário logado.')
        exit(2)
    
#        log.error('Verificar padrão no retorno do site horacerta')
#        #print '------------------------------------------------------------'
#        #print pagina
#        #print '------------------------------------------------------------'
#        log.error( 'Resposta obtida: '+ codigoData)
            


    exit(0)


if __name__ == "__main__":

    for arg in sys.argv:
        if arg == '--help':
            print __doc__
            exit(0)
        
    main()

# todo:
# verificar diferenca entre data local e horacerta: alterar apenas se diferente
# 
