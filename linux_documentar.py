#!/usr/bin/python
# -*- coding: UTF8 -*-

import subprocess 
import sys
import ntpath
import datetime


__author__ = "vicente lima @ brasilia.df"
__date__ = "$22/08/2014 10:50:23$"
__version__ = "0.0.1"


def marcasecao(texto):
    print '-------------------------------'
    print '  ' + texto
    print '-------------------------------\n'

def imprime(lista):
    for linha in lista:
        print '   ', linha.strip()

def executacomando(comando):
    p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.readlines()
            
def eh_root():
    resultado = False
    usuario = executacomando('whoami')
    #print 'usuario:', usuario 
    if usuario[0].strip() == 'root':
        resultado = True
        
    return resultado

if __name__ == "__main__":
    
    if not eh_root():
        print '''
    Atenção: Este programa precisa ser executado como root
    por executar os seguintes comandos:
    
     * fdisk -l
     * ifconfig (para debians)
    '''
        
    
    #main()
    print '''
    ------------------------------------------
    -                                        -
    -         Documentador de linux          -
    -                                        -
    ------------------------------------------'''
        
    print '    gerado por :', ntpath.basename(sys.argv[0]) 
    print '    data e hora:', datetime.datetime.now(),'\n\n'
        
    ''' 
    -------------------------------------------
        nome do sistema e versões
    -------------------------------------------
    ''' 
    
    #sistema_operacional = executacomando('uname -a')
    
    
    
    print '    Sistema Oper. :', executacomando('uname -o')[0] 
    print '    kernel        :', executacomando('uname -s')[0]
    print '    kernel release:', executacomando('uname -r')[0]
    print '    kernel versão :', executacomando('uname -v')[0]
    print '    máquina       :', executacomando('uname -n')[0]
    print '    Processador   :', executacomando('uname -p')[0]
    
    
    print '''
    -------------------------------------------
        memoria diponivel
    -------------------------------------------
    '''

    particoes_montadas = executacomando('free -h')
    
    imprime(particoes_montadas)
    
    print '''
    -------------------------------------------
        lista partições montadas (com tipos)
    -------------------------------------------
    '''

    particoes_montadas = executacomando('df -Th')
            
    imprime(particoes_montadas)
    
    print '''
    -------------------------------------------
        HD e partições 
    -------------------------------------------
    '''

    particoes_montadas = executacomando('fdisk -l')
            
    imprime(particoes_montadas)
    
    print '''
    -------------------------------------------
        Interfaces de rede
    -------------------------------------------
    '''
    
    interface_rede = executacomando('ifconfig ')
            
    imprime(interface_rede)
    
    print '''
    -------------------------------------------
        Pasta em /opt
    -------------------------------------------
    '''
    
    pastas_opt = executacomando('ls -lahgo /opt ')
            
    imprime(pastas_opt)

    print '''
    -------------------------------------------
        pacotes instalados
    -------------------------------------------
    '''
    
    pastas_opt = executacomando('dpkg -l ')
    
    imprime(pastas_opt)
    
    exit(0)
    
