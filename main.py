from gui import ItinerarioGUI
from busca import dfs, Via, ler_dados

if __name__ == '__main__':

    vias, localidades, arrestas, rede =  ler_dados('dados.txt')
    solucao = dfs(rede, localidades[0], localidades[-1], lambda via: 1)
    print(solucao)
    # TODO
    
    