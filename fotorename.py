#! /usr/bin/python
# -*- coding: UTF8 -*-

'''

  Este programa faz uso do modulo "PIL" Python Imaging Library.


  Tabela para configurar data (-d):
  
      %Y   ano no formato YYYY     (1970, 2014)
      %m   mes no formato mm       (01-12)
      %d   dia no formato dd       (01-31)
      %H   hora no formato HH      (00-23)
      %M   minuto no formato MM    (00-59)
      %S   segundo no formato SS   (00-59)
       
      (obs. cuidado ao usar caracteres especiais: &/|\?$) 
        
  Exemplo de uso:
      fotorename.py -i /pastacomfotos/
      fotorename.py -i /pastafoto/ -d "%Y-%m-%d_%H%M"
      fotorename.py -i /pastafoto/ -d "BonitoMS_%Y-%m-%d_%H%M"
      
  Exemplo de resultado:
      IMG_0001.jpg -> 20140722_124957(IMG_0001).jpg
      img-0123.jpg -> 2014-05-28_2200(img-0123).jpg
      GPRO0001.jpg -> BonitoMS_2014-01-08_1323(GPRO0001).jpg

'''


__author__="vicentelima@gmail.com"
__date__="$16/10/2014$"
__version__ = "1.4"

#import exifread
import glob
import os
import re
import sys
import optparse 
import datetime
import time
from PIL import Image
from PIL.ExifTags import TAGS



class Fotorename:

    def __init__(self, pastadeFotos, dataformato):
        self.pastadefotos = pastadeFotos
        self.listafotos = self.carregarArquivos()
        self.__dataformatoPadrao = '%Y%m%d_%H%M%S'
        self.dataformato = self.resolvedataformato(dataformato)


    def carregarArquivos(self):
        '''
           obtem a lista de arquivos da pasta
        '''

        retorno = []

        if not os.path.isdir(self.pastadefotos):
            sys.stderr.write('O diretorio nao existe:\n\t' + self.pastadefotos + '\n')
            exit(2)

        arquivosjpg = glob.glob(self.pastadefotos + '/*.JPG')
        # ['/dir/foto01.JPG', '/dir/foto02.JPG']
        arquivosjpg.extend(glob.glob(self.pastadefotos + '/*.jpg'))
        # ['/dir/foto01.JPG', '/dir/foto02.JPG', '/dir/foto03.jpg']

        if not arquivosjpg:
            sys.stderr.write('Erro: nao ha fotos (jpg/JPG) na pasta indicada:\n\t'+
                self.pastadefotos + '\n')
            exit(3)

        for arquivo in arquivosjpg:
            foto = self.Foto(arquivo)
            retorno.append(foto)

        return retorno


    def resolvedataformato(self, dataformatousr):
        '''
        Verifica se o formato passado nao vai dar erro na execucao
        '''
        retorno = self.__dataformatoPadrao
        if dataformatousr:

            try:
                data =  datetime.datetime.strptime('2014:12:31 23:59:59', '%Y:%m:%d %H:%M:%S')
                #print dataformato
                datateste = datetime.datetime.strftime(data, str(dataformatousr))#'%Y%m%d_%H%M%S')
                retorno = dataformatousr
            except:
                sys.stderr.write('Erro: Nao foi possivel utilizar o formato de data indicado.\n\t' + dataformato + '\n')
                exit(4)

        #print datateste
        #exit(0)
        return retorno


    def geranovonomeComAnterior(self):
        retorno = True
        for foto in self.listafotos:
            nomeArquivo = foto.nomearquivo()
            nomeArquivoParenteses = ''
            try:
                nomeArquivoParenteses = nomeArquivo.split('(')[1]
                nomeArquivoParenteses = nomeArquivoParenteses.split(')')[0]
            except:
                retorno = False

            if nomeArquivoParenteses:
                foto.novonome = nomeArquivoParenteses +'.jpg'
            else:
                return False
                #novonomecompleto = pastadefotos + '/' + novonome
        return retorno


    def geranovonomeComData(self):
        '''
        percorre a lista de fotos
        busca data no exif de cada foto (dependendo da quantidade de fotos, pode melhorar)
        guarda o novo nome da foto para renomecao futura
        '''

        total = len(self.listafotos)
        for conta, foto in enumerate(self.listafotos):
            sys.stderr.write('\rConsultado datas das fotos... ' + str(conta) + ' de ' + str(total))
            foto.datafoto = foto.get_exif(foto.arquivofoto)
            #print foto.arquivofoto, '', foto.datafoto
            if foto.datafoto: #datafoto:
                data = datetime.datetime.strptime(str(foto.datafoto), '%Y:%m:%d %H:%M:%S')
                datanome = datetime.datetime.strftime(data, self.dataformato) #'%Y%m%d_%H%M%S')
                novonome = datanome + '(' + foto.nomearquivoSemExt() + ').jpg'
                foto.novonome = novonome
            else:
                foto.novonome =''
                #print '  ->', tags['EXIF DateTimeOriginal']


    def verificaDuplicidadeNomeArquivo(self):
        listaunica = []
        listarepetidos = []
        for foto in self.listafotos:
            nome = foto.novonome
            if nome in listaunica:
                listarepetidos.append(foto)
            listaunica.append(foto.novonome)
        return listarepetidos


    class Foto:

        def __init__(self, nomecompletoarq):
            self.arquivofoto = nomecompletoarq
            self.novonome = ''
            self.datafoto = ''
            self.exif_ok = False

        def nomearquivo(self):
            return os.path.basename(self.arquivofoto)

        def nomearquivoSemExt(self):
            return self.nomearquivo()[0:(len(self.nomearquivo()) - 4)]

        def get_exif(self, fn):
            ret = {}
            try:
                i = Image.open(fn)
                info = i._getexif()

                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
            except:
                #print 'Nao foi possivel recuperar data (exif):',fn
                return ''

            return ret.get('DateTimeOriginal')




if __name__ == "__main__":

    parse = optparse.OptionParser(
        usage='%prog [options] /dir_imagens/',
        version='>>>>>>  %prog \nVersao: ' + __version__ + '\nAutor:  '+__author__,
        prog=os.path.basename(sys.argv[0]),
        description='    Renomeia fotos usando a data da foto (EXIF).\n' + 
            'Formato padrao: YYYYmmdd_HHMMSS(NOMEORIGINAL).jpg',
        add_help_option=False,
        epilog='Observacoes:'
        )
    
    parse.add_option(
        '-i', '--pastaorigem', 
        action='store', 
        dest='pastaorigem',
        help='Pasta onde as fotos estao. Obrigatorio.'
        )
    
    # parse.add_option(
    #     '-f', '--force',
    #     action='store_true',
    #     dest='force',
    #     help='Ignora verificacao do nome das fotos originais. ' +
    #          'A verificacao serve para nao renomear fotos ja renomeadas. ' +
    #          'Inclua este parametro para forcar a renomeacao.'
    #     )
    parse.add_option(
        '-d', '--dataformato', 
        action='store', 
        dest='dataformato',
        help='Formata a data do nome do arquivo. Opcional.' + 
             'Veja abaixo a tabela com os simbolos aceitos. ' + 
             'Se nao informado o padrao eh "%Y%m%d_%H%M%S"' + 
             ' (YYYYmmdd_HHMMSS) -> (20141231_2359)'
        )
    parse.add_option(
        '-t', '--teste', 
        action='store_true', 
        dest='teste',
        help='Nao renomeia as fotos, apenas mostra como vai ficar. '
        )

    parse.add_option(
        '-r', '--reverter',
        dest='reverter',
        action='store_true',
        help='Reverte uma renomeacao realizada (caso no nome original esteja presente).')

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


    fr = Fotorename(options.pastaorigem, options.dataformato)


    if options.reverter:
        if not fr.geranovonomeComAnterior():
            print 'Erro: a tentativa de reverter renomeacao anterior nao foi bem sucedida.'
            exit(1)
    else:
        fr.geranovonomeComData()


    listarepetidos = fr.verificaDuplicidadeNomeArquivo()
    if listarepetidos:
        print 'Existem arquivos com nomes repetidos na mesma pasta:'
        for foto in listarepetidos:
            print foto.nomearquivo(), ' -> ', foto.novonome
        print 'Nao eh possivel realizar a renomeacao.'
        exit(1)


    for foto in fr.listafotos:
        if not options.teste:
            #print 'Iniciando renomeacao em:\n\t'+ pastadefotos + '\n'
            os.rename(foto.arquivofoto, fr.pastadefotos + foto.novonome)
        # else:
        #     print 'Iniciando teste de renomeacao em:\n\t' + fr.pastadefotos + '\n'

        print foto.nomearquivo(), ' -> ', foto.novonome

    exit(0)


    if not options.force:
        '''
        se passar -f como parametro, entao ignora verificacao e Forca renomeiacao
        '''
        if not options.teste:
            resultado = verificaSeJaFoiRenomeado(arquivosjpg)
            if resultado:
                exit(0)
        
    if options.reverter:
        executarenomeacaoComReversao(pastadefotos, arquivosjpg, options.teste)
    # else:
    #     executarenomeacaoComData(pastadefotos, arquivosjpg, options.teste)
        
    exit(0)

