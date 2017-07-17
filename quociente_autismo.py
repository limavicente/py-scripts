# -*- coding: utf-8 -*-

#Created on Thu Jul 13 11:55:38 2017
#
#@author: Vicente Lima 
#@version: 1.0

class Questionario_avaliacao():
    
    
    def __init__(self, medidas, cabecalho, avaliacao, perguntas, ajuda):
        self.medidas = medidas
        self.cabecalho = cabecalho
        self.avaliacao = avaliacao
        self.perguntas = perguntas
        self.qtdePerguntas = len(self.perguntas) #5
        self.ajuda = ajuda
    
    
    def calcularPontos(self, dicRespostas):
        pontos = 0
        for item in dicRespostas.keys():
            if dicRespostas[item] in self.medidas[item]:
                pontos += 1;
        return pontos
    
    
    def iniciarQuestionario(self):
        
        self.limparTela()
        print(self.cabecalho)
        print(self.ajuda)
        nomeUsuario = resposta = raw_input("Favor informar seu nome: ")
        blocoDeSaidaTxt = ''
        dicRespostas = {}
        numPergunta = 1
        while numPergunta <= self.qtdePerguntas:
            blocoDeSaidaTxt = '\n -------------\n  Pergunta '+ str(numPergunta) + "\n -------------\n"
            blocoDeSaidaTxt = blocoDeSaidaTxt + '\n ' + perguntas[numPergunta] + '\n'
            print(blocoDeSaidaTxt)
            resposta = raw_input("Responda: 1, 2, 3, 4 (use: ?=Ajuda) ")
            if resposta in ['1','2','3','4']:
                dicRespostas[numPergunta] = int(resposta)
                numPergunta += 1
            elif resposta == '?':
                print(ajuda)
            elif resposta == 's':
                print('\nTecla "s" pressionada. Saindo do questionario.')
                break
            else:
                print(' --> Valor digitado nao tem significado: '+ resposta)
                
        pontos = self.calcularPontos(dicRespostas)
        
        
        if len(dicRespostas) != self.qtdePerguntas:
            print('Questionario incompleto, nenhum resultado serah apresentado.')
            print('-------------------------------------------------------------')
        else:
            self.gravarResultadoEmDisco(nomeUsuario, dicRespostas)
            #print("Respostas: ", dicRespostas)
            print('\n\n\n---------------------------------------')
            print('   Resultado')
            print('---------------------------------------')
            print("\n  Pontuacao para {}: {}".format(nomeUsuario,str(pontos)))
            print(avaliacao) 
    
    
    def limparTela(self):
        print('\n' * 100)
        
        
    def gravarResultadoEmDisco(self, nomeUsuario, dicRespostas):
        import codecs
        
        with codecs.open(nomeUsuario + '.txt', 'w') as saida:
            saida.write(self.cabecalho)
            for item in dicRespostas.keys():
                saida.write('  Resposta da Pergunta {}: {} \n'.format(item,dicRespostas[item]))
    
            pontos = self.calcularPontos(dicRespostas)
            saida.write('\n  Total de pontos: {} \n'.format(pontos))
            saida.write(avaliacao)



if __name__ == '__main__':

    cabecalho = """
    
    -------------------------------------------------------------
           Teste de QA - Quociente do Espectro de Autismo  
    -------------------------------------------------------------
    
        Simon BaronCohen (psicologo) e seus colegas do Centro 
        de pesquisa em Autismo da Universidade de Cambridge, 
        elaboraram este teste no intuito de revelar tracos 
        autistas em adultos.
        
        Este teste nao subistitui um diagnostico, que deve ser
        realizado por um profissional, mas pode servir como um
        indicativo para a procura deste especialista.
    
        O questionario eh composto de 50 perguntas que devem ser 
        respondidas com valores numericos de 1 ate 4.
    
        O valores 1,2 significam que voce CONCORDA com o enunciado, 
          valores 3,4 significam que voce DISCORDA.
    
    """
    
    avaliacao = """
    
    16,4 pontos foi a pontuacao media no grupo de controle, no primeiro 
         ensaio principal usando este teste. 
    
    32 pontos ou mais foi o resultado obtido por 80% das pessoas 
        diagnosticadas com autismo ou disturbios relacionados.
     
    Muitos que pontuam acima de 32 pontos e ate mesmo venham a atender aos 
    criterios de diagnostico de autismo leve ou sindrome de Asperger podem levar 
    uma vida comum, sem grandes dificuldades, respeitando suas limitacoes.
     
    """
    
    perguntas = {
     1:"Eu prefiro fazer as coisas com os outros, em vez de sozinho.",
     2:"Eu prefiro fazer as coisas da mesma maneira sempre.",
     3:"Se eu tentar imaginar algo, acho que eh muito facil criar uma imagem em \nminha mente.",
     4:"Eu frequentemente fico tao fortemente concentrado em uma coisa que eu \nignoro outras coisas.",
     5:"Costumo observar pequenos sons quando os outros nao os percebem.",
     6:"Eu costumo observar placas de carros, numeros ou sequencias similares \nde informacoes.",
     7:"Outras pessoas frequentemente me corrigem, dizendo que o que falo eh \nfalta de educacao, mesmo quando eu acho que eh educado.",
     8:"Quando eu estou lendo uma historia, eu posso facilmente imaginar o que \nos personagens estao fazendo.",
     9:"Sou fascinado por datas.",
    10:"Em um grupo social, eu posso facilmente manter conversacao com diferentes\n pessoas.",
    11:"Acho facil conviver socialmente.",
    12:"Eu percebo detalhes que outros nao percebem tao facilmente.",
    13:"Prefiro ir a uma biblioteca do que uma festa.",
    14:"Acho inventar historias algo muito facil.",
    15:"Sou atraido mais fortemente para as pessoas do que para coisas.",
    16:"Quando tenho interesse muito forte num determinado assunto, fico muito \nchateado se nao consigo levar adiante meus pensamentos sobre este assunto.",
    17:"Eu gosto de fofoca social.",
    18:"Quando eu falo, nem sempre eh facil para os outros entenderem claramente o\n que quero dizer.",
    19:"Sou fascinado por numeros.",
    20:"Quando eu estou lendo uma historia, acho dificil entender as intencoes \ndos personagens.",
    21:"Eu particularmente nao gosto de ler ficcao.",
    22:"Acho que eh dificil fazer novos amigos.",
    23:"Percebo padroes nas coisas o tempo todo.",
    24:"Prefiro ir ao teatro do que um museu.",
    25:"Eu nao me chateio se minha rotina diaria eh perturbada.",
    26:"Eu frequentemente tenho dificuldade em manter uma conversa.",
    27:"Consigo facilmente ""ler nas entrelinhas"" quando alguem estah falando \ncomigo.",
    28:"Eu costumo me concentrar mais numa imagem por inteiro do que nos \npequenos detalhes.",
    29:"Eu nao sou muito bom em lembrar numeros de telefone.",
    30:"Eu nao costumo perceber pequenas mudancas em uma situacao ou na \naparencia de uma pessoa.",
    31:"Eu percebo se alguem que estah me ouvindo estah ficando entediado.",
    32:"Acho facil fazer mais de uma coisa ao mesmo tempo.",
    33:"Quando eu falo ao telefone, tenho dificuldade de saber quando eh a \nminha vez de falar.",
    34:"Eu gosto de fazer as coisas de forma espontanea.",
    35:"Muitas vezes sou o ultimo a entender uma piada.",
    36:"Consigo perceber o que uma pessoa estah pensando ou sentindo so de olhar \npara seu rosto.",
    37:"Se houver uma interrupcao, eu posso voltar para o que eu estava fazendo \nmuito rapidamente.",
    38:"Eu sou bom em conversa social.",
    39:"Muitas vezes as pessoas me dizem que eu continuo falando repetidamente \nsobre a mesma coisa.",
    40:"Quando eu era jovem, eu gostava de jogar jogos de imaginacao com outras \ncriancas.",
    41:"Eu gosto de coletar informacoes sobre categorias de coisas (por exemplo, \nos tipos de carros, passaros, trens, plantas).",
    42:"Para mim, eh muito dificil imaginar-me sendo outra pessoa.",
    43:"Eu gosto de planejar cuidadosamente qualquer atividade que eu irei \nparticipar.",
    44:"Gosto de ocasioes (reunioes) sociais.",
    45:"Acho dificil detectar as reais intencoes das pessoas.",
    46:"Situacoes novas me deixam ansioso.",
    47:"Eu gosto de conhecer novas pessoas.",
    48:"Eu sou um bom diplomata.",
    49:"Eu nao sou muito bom em lembrar da data de nascimento das pessoas.",
    50:"Gosto de brincar de jogos imaginarios com as criancas."}

    """
    Regras para pontuacao:
    
    Se voce respondeu "Concordo definitivamente" ou "concordo um pouco" as perguntas 
    2, 4, 5, 6, 7, 9, 12, 13, 16, 18, ​​19, 20, 21, 22, 23, 26, 33, 35, 39, 41, 42, 
    43, 45, 46, 
    marque 1 ponto. As demais nao marcam pontos.  
    
    Se voce respondeu "Discordo definitivamente" ou "Discordo um pouco" as perguntas 
    1, 3, 8, 10, 11, 14, 15, 17, 24, 25, 27 , 28, 29, 30, 31, 32, 34, 36, 37, 38, 
    40, 44, 47, 48, 49, 50, 
    marque 1 ponto. As demais nao marcam pontos.
    """
    medidas = {
     1:[3,4],
     2:[1,2],
     3:[3,4],
     4:[1,2],
     5:[1,2],
     6:[1,2],
     7:[1,2],
     8:[3,4],
     9:[1,2],
    10:[3,4],
    11:[3,4],
    12:[1,2],
    13:[1,2],
    14:[3,4],
    15:[3,4],
    16:[1,2],
    17:[3,4],
    18:[1,2],
    19:[1,2],
    20:[1,2],
    21:[1,2],
    22:[1,2],
    23:[1,2],
    24:[3,4],
    25:[3,4],
    26:[1,2],
    27:[3,4],
    28:[3,4],
    29:[3,4],
    30:[3,4],
    31:[3,4],
    32:[3,4],
    33:[1,2],
    34:[3,4],
    35:[1,2],
    36:[3,4],
    37:[3,4],
    38:[3,4],
    39:[1,2],
    40:[3,4],
    41:[1,2],
    42:[1,2],
    43:[1,2],
    44:[3,4],
    45:[1,2],
    46:[1,2],
    47:[3,4],
    48:[3,4],
    49:[3,4],
    50:[3,4]}
    
    ajuda = """
        -----------------------------------------
        As perguntas devem ser respondidas com os
        seguintes valores [1,2,3,4]:
        - - - - - - - - - - - - - - - - - - - - -
        concordo ---------> 1
        concordo pouco ---> 2
        
                            3 <--- discordo pouco
                            4 <--------- discordo
        - - - - - - - - - - - - - - - - - - - - -
        Para sair do questionario, digite "s"
        -----------------------------------------
    """
    quest = Questionario_avaliacao(medidas, cabecalho, avaliacao, perguntas, ajuda)
    quest.iniciarQuestionario()
    

    
    
