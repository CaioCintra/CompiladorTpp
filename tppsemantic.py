import tppparser
import pandas as pd
import sys
from anytree.exporter import UniqueDotExporter

global dataFrameVar 
dataFrameVar = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'TIPO', 'DIM','TAM_DIM', 'INIT'])
global dataFrameFunc 
dataFrameFunc = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'QTD_PARAM', 'PARAMETROS', 'TIPO', 'RETORNO'])

global blacklist
blacklist = ['ID', 'var', 'lista_variaveis', 'dois_pontos', 'tipo','INTEIRO', 'FLUTUANTE', 'NUM_INTEIRO', 'NUM_PONTO_FLUTUANTE'
            ,'NUM_NOTACAO_CIENTIFICA', 'LEIA', 'abre_parentese', 'fecha_parentese','lista_declaracoes', 'declaracao', 'indice',
            'numero', 'fator','abre_colchete', 'fecha_colchete', 'expressao', 'expressao_logica','expressao_simples',
            'expressao_aditiva', 'expressao_multiplicativa','expressao_unaria', 'inicializacao_variaveis', 'ATRIBUICAO',
            'atribuicao','operador_soma', 'mais', 'chamada_funcao', 'lista_argumentos', 'VIRGULA','virgula', 'fator', 'cabecalho',
            'FIM', 'lista_parametros', 'vazio','(', ')', ':', ',', 'RETORNA', 'ESCREVA', 'SE', 'ENTAO', 'SENAO', 'maior',
            'menor', 'REPITA', 'igual', 'menos', 'menor_igual', 'maior_igual', 'operador_logico','operador_multiplicacao', 'vezes',
            'ABRE_PARENTESE','FECHA_PARENTESE','MAIS','operador_relacional','MAIOR','MENOR','IGUAL','parametro', 'MENOS','id']

def declaredVar(knot):
    global dataFrameVar 
    varExists = -1
    varName = ''
    for node in knot.children:
        if(node.label == 'ID'):
            for ind in range(len(dataFrameFunc)):
                if(node.children[0].label == dataFrameFunc['LEXEMA'][ind]):
                    return
            for ind in range(len(dataFrameVar)):
                if(node.children[0].label == dataFrameVar['LEXEMA'][ind]):
                    varExists = 1
                varName = node.children[0].label

            if(varExists == -1):
                varExists = 0
        declaredVar(node)
    
    if(varExists == 0):
        print('\nErro: Variável',varName,'não declarada')
        return
    return


def treeTravel(root):
    global dataFrameVar 
    global dataFrameFunc
    listNode = ''
    for node in root.children:
        parametros = [ ]
        if (node.label == 'declaracao_variaveis'):
            token = node.children[2].children[0].children[0].label
            lexema = node.children[2].children[0].children[0].children[0].label
            tipo = node.children[0].children[0].label
            varFlag = 0
            if(len(node.children[2].children[0].children)>1):
                dim = 1
                tam_dim = node.children[2].children[0].children[1].children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
            else:
                dim = 0
                tam_dim = 0
            for f in dataFrameVar.index:
                if(lexema == dataFrameVar['LEXEMA'][f]):
                    varFlag = 1
                    print('\nAviso: Variável',lexema,'já declarada anteriormente')
            if(varFlag == 0):
                dataFrameVar = dataFrameVar.append({'TOKEN' : token, 'LEXEMA' : lexema, 'TIPO' : tipo, 'DIM': dim, 'TAM_DIM': tam_dim, 'INIT': 'N'}, ignore_index=True)

        if (node.label == 'atribuicao'):
            declaredVar(node)

            for ind in dataFrameVar.index:
                if(dataFrameVar['LEXEMA'][ind] == node.children[0].children[0].children[0].label):
                    dataFrameVar['INIT'][ind] = node.children[2].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
                    varType = dataFrameVar['TIPO'][ind]
                    for n in dataFrameVar.index:
                        if(dataFrameVar['INIT'][ind] == dataFrameVar['LEXEMA'][n]):
                            if(dataFrameVar['TIPO'][n] != varType):
                                print('\nAviso: Atribuição de tipos distintos',dataFrameVar['LEXEMA'][ind],varType,'e',dataFrameVar['LEXEMA'][n],dataFrameVar['TIPO'][n])  
                    for n in dataFrameFunc.index:
                        if(dataFrameVar['INIT'][ind] == dataFrameFunc['LEXEMA'][n]):
                            if(dataFrameFunc['TIPO'][n] != varType):
                                print('\nAviso: Atribuição de tipos distintos',dataFrameVar['LEXEMA'][ind],varType,'e',dataFrameFunc['LEXEMA'][n],'retorna',dataFrameFunc['TIPO'][n])                    
        if (node.label == 'declaracao_funcao'):
            idx = 1
            tipo = node.children[0].children[0].label
            try: 
                token = node.children[1].children[0].label
                lexema = node.children[1].children[0].children[0].label
            except: 
                token = 'vazio'
                idx = 0
                lexema = node.children[0].children[0].children[0].label
            
            retorno = 'vazio'
            qtd_param = 0
            
            if (node.children[idx].children[2].label == 'lista_parametros'):
                if (node.children[idx].children[2].children[0].label != 'vazio'):
                    if (node.children[idx].children[2].children[0].label == 'lista_parametros'):
                        if (node.children[idx].children[2].children[0].children[0].children[2].children[0].label != None):
                            id = node.children[idx].children[2].children[0].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            qtd_param = qtd_param + 1 
                            son = len(node.children[idx].children[2].children)
                            for i in range (2,son,2):
                                    id = node.children[idx].children[2].children[i].children[2].children[0].label
                                    a = id+' '
                                    parametros.append(a)
                                    qtd_param = qtd_param + 1 
                    else:
                        if (node.children[idx].children[2].children[0].children[2].children[0].label != None):
                            id = node.children[idx].children[2].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            qtd_param = qtd_param + 1 
                            
                else:
                    parametros = 'vazio'
                
            if(node.children[idx].children[4].children[1].children[0].label == 'retorna'):
                if(node.children[idx].children[4].children[1].children[0].children[1].label == 'ABRE_PARENTESE'):
                    retorno = node.children[idx].children[4].children[1].children[0].children[2].label
            dataFrameFunc = dataFrameFunc.append({'TOKEN' : token, 'LEXEMA' : lexema,'QTD_PARAM': qtd_param, 'PARAMETROS' : parametros, 'TIPO' : tipo, 'RETORNO' : retorno}, ignore_index=True)
            

        if (node.label == 'chamada_funcao'):
            funcCalled = node.children[0].children[0].label
            funcExists = 0
            for ind in dataFrameFunc.index:
                if(dataFrameFunc['LEXEMA'][ind] == funcCalled):
                    funcExists = 1
            if(funcExists == 0):
                print('\nErro: Chamada a função',funcCalled,'que não foi declarada')
            else:
                funcParam = ((len(node.children[2].children)-1)/2)+1
                for ind in dataFrameFunc.index:
                    if(dataFrameFunc['LEXEMA'][ind] == funcCalled):
                        if(int(dataFrameFunc['QTD_PARAM'][ind]) > funcParam):
                            print('\nErro: Chamada à função',funcCalled,'com número de parâmetros menor que o declarado')

        listNode = treeTravel(node)       

    return listNode

def cutTree(root):
    global blacklist
    for node in root.children:
        cutTree(node)

    if root.label in blacklist:
        dad = root.parent
        aux = []
        for children in dad.children:
            if children != root:
                aux.append(children)
        for children in root.children:
            aux.append(children)
        root.children = aux
        dad.children = aux

    if root.label == 'declaracao_funcao':
        corpo = root.children[1]
        aux = []
        for children in root.children:
            if children.label == 'fim':
                aux.append(corpo)
            if children != corpo:
                aux.append(children)
        root.children = aux

    if root.label == 'corpo' and len(root.children) == 0:
        dad = root.parent
        aux = []
        for children in dad.children:
            if children != root:
                aux.append(children)
        for children in root.children:
            aux.append(children)
        root.children = aux
        dad.children = aux
    return root

def newTree(root):
    for node in root.children:
        newTree(node)

    dad = root.parent
    aux = []

    if root.label == 'repita' and len(root.children) > 0:
        for children in root.children:
            if children.label != 'repita':
                aux.append(children)
        root.children = aux
        aux = []

    if root.label == 'e' and root.children[0].label == '&&':
        root.children = []
        root.label = '&&'
        root.name = '&&'

    if root.label == 'ou' and root.children[0].label == '||':
        root.children = []
        root.label = '||'
        root.name = '||'


    if root.label == 'se' and len(root.children) > 0:
        for children in root.children:
            if children.label != 'se':
                aux.append(children)

        root.children = aux
        aux = []

    if root.label == 'ATE':
        root.children = []
        root.label = 'até'
        root.name = 'até'

    if root.label == 'leia' or root.label == 'escreva' or root.label == 'retorna':
        if len(root.children) == 0:
            for children in dad.children:
                if children != root:
                    aux.append(children)

            dad.children = aux
    return root

def main():
    print ('\n\n')
    tree = tppparser.main()
    treeCall = treeTravel(tree)
    global dataFrameVar
    global dataFrameFunc
    for ind in dataFrameVar.index:
        if(dataFrameVar['INIT'][ind] == 'N'):
            print('\nAviso: Variável',dataFrameVar['LEXEMA'][ind],'declarada e não utilizada')
        if(dataFrameVar['TAM_DIM'][ind] != 0 and float(dataFrameVar['TAM_DIM'][ind]) % 1 != '0'):
            print('\nErro: índice de array',dataFrameVar['LEXEMA'][ind],'não inteiro')
    for ind in dataFrameFunc.index:
        if(dataFrameFunc['RETORNO'][ind] == 'vazio'):
            print('\nErro: Função',dataFrameFunc['LEXEMA'][ind],'deveria retornar',dataFrameFunc['TIPO'][ind],', mas retorna vazio')
    if (len(dataFrameFunc) == 0):
        print('\nErro: Função principal não declarada')

    if (len(dataFrameVar) != 0):
        print ('\nTabela de Símbolos')
        print (dataFrameVar)
        print ('\n')

    if (len(dataFrameFunc) != 0):
        print ('\nTabela de Funções')
        print (dataFrameFunc)
        print ('\n')

    print ('\n')
    tree = cutTree(tree)
    tree = newTree(tree)
    UniqueDotExporter(tree).to_picture(f"{sys.argv[1]}.cut.unique.ast.png")
    return tree
    
if __name__ == "__main__":
    main()