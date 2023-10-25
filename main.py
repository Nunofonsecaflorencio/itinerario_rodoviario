from gui import ItinerarioGUI
from busca import dfs, Via, ler_dados

if __name__ == '__main__':
    vias, localidades, arestas, rede =  ler_dados('dados.txt')
    
    visualizer = ItinerarioGUI(rede, {
        'DFS': lambda origem, destino, funcao_custo: dfs(rede, origem, destino, funcao_custo)
    }, {
        'C0': lambda v: 1
    })
    visualizer.run()
    
    