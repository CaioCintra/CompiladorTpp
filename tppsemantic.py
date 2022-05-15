import tppparser

def treeTravel(root):
    list_node = ''
    for node in root.children:
        print(node.label)
        list_node = treeTravel(node)
    return list_node

def main():
    tree = tppparser.main()

    treeCall = treeTravel(tree)
    


if __name__ == "__main__":
    main()