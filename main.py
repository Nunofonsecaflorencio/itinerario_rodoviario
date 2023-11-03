from gui import ItinerarioGUI
from search.problem import RoadIteneraryProblem
from search.algorithms import DepthFirstSearch, BreadthFirstSearch

if __name__ == '__main__':
    
    itinerario = RoadIteneraryProblem("dados.txt")
    
    
    functions = {
        'search_algorithms':{
            'Busca em Profundidade': lambda start, end, _, do_shuffle: DepthFirstSearch(start, end, itinerario.get_neighbors_edges, itinerario.compute_path_cost, do_shuffle),
            'Busca em Largura': lambda start, end, _, do_shuffle: BreadthFirstSearch(start, end, itinerario.get_neighbors_edges, itinerario.compute_path_cost, do_shuffle)
        },
        'costs': {
            'C0': lambda v: 1
        },
        'get_sucessors': itinerario.get_neighbors_edges
    }
    
    visualizer = ItinerarioGUI(itinerario.graph, functions)
    visualizer.run()

