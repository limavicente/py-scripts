#! /usr/bin/python
# -*- coding: UTF8 -*-

'''

   Este programa faz uso do imagemagic

   exemplos de uso: 
       fotodiminuir.py -i /pastacomfotos/ 
       fotodiminuir.py -p 20 -i /pastacomfotos/ -o /pastacomfotos/20porc/


'''


__author__="vicentelima@gmail.com"
__date__="$17/10/2014$"
__version__ = "1.2"


#import exifread
import glob
import os
#import re
import sys
import subprocess 
import optparse 




def executacomando(comando):
    p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.readlines()


def executarconversaodasfotos(diretorio, pastadestino, porcentagem):
    
    arquivosjpg = glob.glob(diretorio + '*.JPG')
    arquivosjpg.extend(glob.glob(diretorio + '*.jpg'))
    
    if not arquivosjpg:
        sys.stderr.write('Erro: Nao ha arquivos (jpg) na pasta indicada:\n' + \
              '\t' + diretorio 
              )
        exit(3)
    
    
    arquivoserro = []
    
    print 'Iniciando a conversao em:\n\t', diretorio
    print 'Para:\n\t', pastadestino, '\n'
    
    if not os.path.lexists(pastadestino):
        resultado = executacomando('mkdir ' + pastadestino)
         
        for linharesultado in resultado:
            print linharesultado
            
    for arquivo in arquivosjpg:
         
        nomeArquivo = os.path.basename(arquivo)
 
        resultado = executacomando(
            'convert -resize ' + str(porcentagem) + '% "' + arquivo + '" "' + \
            pastadestino + nomeArquivo + '"'
            )
        #print 'convert -resize ' + str(porcentagem) + '% "' + arquivo + '" "' + \
        #    pastadestino + nomeArquivo + '"'
        print nomeArquivo
        
        
def resolvepastaorigem(pastaorigem):
    
    if not pastaorigem:
        #nao manda para saida padrao (stdout), mas para strerr
        sys.stderr.write('\nErro: E preciso indicar uma pasta com as fotos (jpg).\n' +
                         'Para ajuda use: ' + sys.argv[0] + ' --help\n\n')
        exit(1)
        'exemplo: fotodiminuir.py /home/vicente/fotos/'

    if not os.path.isdir(pastaorigem):
        sys.stderr.write('Erro: O diretorio nao existe:\n\t' + options.pastaorigem)
        exit(2)
        
    if pastaorigem[-1] != '/':
        pastaorigem = pastaorigem + '/'   
            
    return pastaorigem     


def resolveporcentagem(porcentagem):
    
    if not porcentagem:
        porcentagem = 50 # porcentagem padrao - default
        
    return porcentagem


def resolvepastadestino(pastaorigem, pastadestino):
    
    if not pastadestino:
        pastadestino = pastaorigem + 'temp/'
    else:
        if pastadestino[-1] != '/':
            pastadestino = pastadestino + '/'

    return pastadestino




if __name__ == "__main__":

    parse = optparse.OptionParser(
        usage='%prog [options]',
        version='>>>>>>  %prog \nVersao: ' + __version__ + '\nAutor:  '+ __author__,
        prog=os.path.basename(sys.argv[0]),
        description='    Redimensiona fotos (jpg) em uma pasta menor. Nao' + 
            ' altera dos dados de EXIF. Mantem a mesma proporcao (alt x larg).',
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
        '-o', '--pastadestino', 
        action='store', 
        dest='pastadestino',
        help='Pasta de destino para fotos menores. Opcional - ' + 
             'Caso nao seja informado sera criado um diretorio chamado (temp) na ' + 
             'pasta de origem.'
        )
        
    parse.add_option(
        '-p', '--porcentagem', 
        action='store', 
        type='int',
        dest='porcentagem',
        help='Porcentagem para o tamanho da foto convertida (diminuida). ' + 
            'Opcional - Caso nao informe sera usado 50%.'
        )

    parse.add_option(
        '-h', '--help', 
        dest='help', 
        action='store_true',
        help='show this help message and exit')
    
    
    (options, args) = parse.parse_args()

    if options.help or (len(sys.argv)==1):
        parse.print_help()
        print __doc__
        exit(0)

    
    pastaorigem = resolvepastaorigem(options.pastaorigem)

    porcentagem = resolveporcentagem(options.porcentagem)
        
    pastadestino = resolvepastadestino(pastaorigem, options.pastadestino)
    
    executarconversaodasfotos(pastaorigem, pastadestino, porcentagem)
    
    exit(0)
