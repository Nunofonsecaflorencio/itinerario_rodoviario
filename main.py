from gui import ItinerarioGUI
from busca import *

if __name__ == '__main__':
    vias, localidades, arestas, rede =  ler_dados('dados.txt')
    
    
    functions = {
        'search_algorithms':{
            'DFS': lambda origem, destino, funcao_custo: dfs(rede, origem, destino, funcao_custo)
        },
        'costs': {
            'C0': lambda v: 1
        },
        'get_sucessors': lambda node: sucessores(rede, node)
    }
    
    visualizer = ItinerarioGUI(rede, functions)
    visualizer.run()
    
    