#! /usr/bin/python
# -*- coding: UTF8 -*-

'''

  
  Este programa faz uso do modulo "exifread" (1.4.2)
      (https://pypi.python.org/pypi/ExifRead)
      (Baixe pacote exifread, descompacte e rode o setup.py)
      (python setup.py install)

        
  Exemplo de uso:
      fotorename.py -i /pastacomfotos/
      
  Exemplo de resultado:
      IMG_0001.jpg -> 20140722_124957(IMG_0001).jpg

'''


__author__="vicentelima@gmail.com"
__date__="$16/10/2014$"
__version__ = "1.2"

import exifread
import glob
import os
import re
import sys
import optparse 


def verificaSeJaFoiRenomeado(arquivosjpg):
    '''
    Se houver um arquivo no formato DATA_HORA(NOME).jpg
    emite um aviso, para e informa como forcar renomeacao
    '''
    for nomearquivo in arquivosjpg:
        nomearquivo = os.path.basename(nomearquivo)
        casou =  re.findall(r'\d{8}[_]\d{6}[(].+[)].jpg', nomearquivo)
        if casou != []:
            sys.stderr.write(
                '\nFoi encontrado um arquivo com o formato: DATA_HORA(NOME).jpg\n' +
                '\t'+ nomearquivo + '\n' +
                'o programa parou para evitar a renomeacao de arquivos ja renomeados.\n' +
                'Para continuar assim mesmo, passe o parametro: -f\n'
                )
            print nomearquivo
    
            exit(0)
        
def resolvepastaorgiem(pastaorigem):
    
    if not pastaorigem:
        #nao manda para saida padrao (stdout), mas para strerr
        sys.stderr.write('Erro: E preciso indicar uma pasta com as fotos (jpg).\n' +
                         'Para ajuda use: ' + sys.argv[0] + ' --help\n')
        exit(1)
       
    else:
        if not os.path.isdir(pastaorigem):
            sys.stderr.write('O diretorio nao existe:\n\t' + pastaorigem + '\n')
            exit(2)
            
    if pastaorigem[-1] != '/':
        pastaorigem = pastaorigem + '/'
    
    return pastaorigem
    
    
    
def resolvearquivosjpg(pastadefotos):
    
    arquivosjpg = glob.glob(pastadefotos + '*.JPG')
    # ['/dir/foto01.JPG', '/dir/foto02.JPG']
    arquivosjpg.extend(glob.glob(pastadefotos + '*.jpg'))
    # ['/dir/foto01.JPG', '/dir/foto02.JPG', '/dir/foto03.jpg']
    
    if not arquivosjpg:
        sys.stderr.write('Erro: nao ha fotos (jpg) na pasta indicada:\n\t'+ 
            pastadefotos + '\n')
        exit(3)    
    
    
    return arquivosjpg
    
    
def executarenomeacao(pastadefotos, arquivosjpg, teste):    
    
    arquivoserro = []
    
    print 'Iniciando renomeacao em:\n\t', pastadefotos, '\n'
    
    for arquivo in arquivosjpg:
        f = open(arquivo, 'rb')
        tags = exifread.process_file(f)
        f.close()
        nomeArquivo = os.path.basename(arquivo)
        nomeArquivoSemExt = nomeArquivo[0:(len(nomeArquivo)-4)]
        #print nomeArquivoSemExt
    
        if 'EXIF DateTimeOriginal' in tags.keys():
            datafoto = tags['EXIF DateTimeOriginal']
            datafoto = str(datafoto).replace(':','')
            datafoto = datafoto.replace(' ','_')
            novonome = datafoto + '(' + nomeArquivoSemExt + ').jpg'
            novonomecompleto = pastadefotos + '/' + novonome  
    
            #print '  ->', tags['EXIF DateTimeOriginal']
            if not teste:
                os.rename(arquivo, novonomecompleto)
            print nomeArquivo, ' -> ', novonome
            
        else:
            arquivoserro.append(arquivo)
        
    if len(arquivoserro) > 0:
        print '\narquivos com erro:\n', arquivoserro
        
        
        

if __name__ == "__main__":

    parse = optparse.OptionParser(
        usage='%prog [options]',
        version='>>>>>>  %prog \nVersao: ' + __version__ + '\nAutor:  '+__author__,
        prog=os.path.basename(sys.argv[0]),
        description='    Renomeia fotos usando a data da foto (EXIF).\n' + 
            'Formato: YYYYMMDD_HHMMSS(NOMEORIGINAL).jpg',
        add_help_option=False,
        epilog='Observacoes:'
        )
    
    parse.add_option(
        '-i', '--pastaorigem', 
        action='store', 
        dest='pastaorigem',
        help='Pasta onde as fotos estao. Obrigatorio.'
        )
    
    parse.add_option(
        '-f', '--force', 
        action='store_true', 
        dest='force',
        help='Ignora verificacao do nome das fotos originais. ' + 
             'A verificacao serve para nao renomear fotos ja renomeadas. ' + 
             'Inclua este parametro para forcar a renomeacao.'
        )
    parse.add_option(
        '-t', '--teste', 
        action='store_true', 
        dest='teste',
        help='Nao renomeia as fotos, apenas mostra como vai ficar. '
        )
        

    parse.add_option(
        '-h', '--help', 
        dest='help', 
        action='store_true',
        help='Mostra esta mensagem de ajuda e sai.')
    
    (options, args) = parse.parse_args()
    
    if options.help or (len(sys.argv)==1):
        parse.print_help()
        print __doc__
        exit(0)
    
    pastadefotos = resolvepastaorgiem(options.pastaorigem)
    
    arquivosjpg = resolvearquivosjpg(pastadefotos)
            
   
    if not options.force:
        '''
        se passar -f como parametro, entao ignora verificacao e Forca renomeiacao
        '''
        if not options.teste:
            verificaSeJaFoiRenomeado(arquivosjpg)
        

    executarenomeacao(pastadefotos, arquivosjpg, options.teste)
        
    exit(0)
    
    
    
