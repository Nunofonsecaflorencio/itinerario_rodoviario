from gui.visualizer import ItinerarioGUI
from search.problem import RoadIteneraryProblem
from search.algorithms import DepthFirstSearch, BreadthFirstSearch

if __name__ == '__main__':
    
    itinerario = RoadIteneraryProblem("dados.txt")
    
    
    functions = {
        'search_algorithms':{
            'Busca em Profundidade': lambda start, end, min_road_quality, cost, do_shuffle: 
                DepthFirstSearch(start, end, lambda node: itinerario.get_neighbors_edges(node, min_road_quality), itinerario.compute_path_cost, do_shuffle),
            'Busca em Largura': lambda start, end, min_road_quality, cost, do_shuffle: 
                BreadthFirstSearch(start, end, lambda node: itinerario.get_neighbors_edges(node, min_road_quality), itinerario.compute_path_cost, do_shuffle)
        },
        'costs': {
            'C1-Distância': lambda via: via.C1(),
            'C2-Duração': lambda via: via.C2(),
            'C3-Custo': lambda via: via.C3(), 
        },
        'get_sucessors': itinerario.get_neighbors_edges
    }
    
    visualizer = ItinerarioGUI(itinerario.graph, functions)
    visualizer.run()

