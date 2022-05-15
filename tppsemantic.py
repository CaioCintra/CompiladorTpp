import tppparser
import pandas as pd

global dataFrame 
dataFrame = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'TIPO'])

def treeTravel(root):
    global dataFrame 
    listNode = ''
    for node in root.children:
        #print(node.label)
        if (node.label == 'declaracao_variaveis'):
            token = node.children[2].children[0].children[0].label
            lexema = node.children[2].children[0].children[0].children[0].label
            tipo = node.children[0].children[0].label
            dataFrame = dataFrame.append({'TOKEN' : token, 'LEXEMA' : lexema, 'TIPO' : tipo}, ignore_index=True)

        listNode = treeTravel(node)
    return listNode

def main():
    tree = tppparser.main()

    treeCall = treeTravel(tree)
    print (dataFrame)

if __name__ == "__main__":
    main()