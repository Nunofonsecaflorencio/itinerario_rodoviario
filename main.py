from gui import ItinerarioGUI
from busca import dfs, Via, ler_dados

if __name__ == '__main__':
    vias, localidades, arestas, rede =  ler_dados('dados.txt')
    print(vias)
    print(localidades)
    print(arestas)
    print(rede)
    print()

    solucao, ordem = dfs(rede, 'mozal', 'baixa', lambda via: 1)
    print(solucao)
    print(ordem)
    # TODO
    
    