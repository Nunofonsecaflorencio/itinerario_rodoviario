import PySimpleGUI as sg
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from time import sleep


def calculate_midpoint(posA, posB, rad):
    # Calculate the control point for the arc
    control = (
        (posA[0] + posB[0]) / 2 + rad * (posA[1] - posB[1]),
        (posA[1] + posB[1]) / 2 + rad * (posB[0] - posA[0])
    )

    # Calculate the midpoint along the arc
    t = 0.5  # Parameter for the Bezier curve (0.5 for midpoint)
    midpoint = (
        (1 - t) ** 2 * posA[0] + 2 * (1 - t) * t * control[0] + t ** 2 * posB[0],
        (1 - t) ** 2 * posA[1] + 2 * (1 - t) * t * control[1] + t ** 2 * posB[1]
    )

    return midpoint

class ItinerarioGUI:
    def __init__(self, network, search_algorithms, costs):
        
        self.network = network
        self.search_algorithms = search_algorithms
        self.costs = costs
        
        layout = [
            [sg.Canvas(key="-CANVAS-")],
            [
                sg.T("Origem"), sg.Combo(list(network.keys()), key="-ORIGEM-"),
                sg.T("Destino"), sg.Combo(list(network.keys()), key="-DESTINO-"),
            ],
            [
                sg.T("Critério"), sg.Combo(list(costs), default_value=list(costs)[0], key="-CRITERIO-"),
                sg.T("Algoritmo"), sg.Combo(list(search_algorithms), default_value=list(search_algorithms)[0], key="-ALGORITMO-"),
            ],
            [sg.Button("Buscar", key='-BUSCAR-'), sg.Button("Limpar", key='-LIMPAR-')]
        ]
        self.window = sg.Window("Itinerário Rodoviário", layout, finalize=True)
        
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(15, 6)
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.window['-CANVAS-'].TKCanvas)
        self.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        self.initialize(network)
    
    def initialize(self, network):
        self.graph = nx.MultiGraph()
        
        dont_add = set()
        for loc, vias in network.items():
            for via in vias:
                if (loc, via.destino, via.distancia) not in dont_add:
                    self.graph.add_edge(loc, via.destino, label=f"{via.distancia}km {via.codigo}")
                    dont_add.add((via.destino, loc, via.distancia))
            
        self.graph_pos = nx.spring_layout(self.graph, seed=1)
        print(self.graph)

    def draw(self):
        G = self.graph
        pos = self.graph_pos
        
        self.fig.clf()
         # nodes
        nx.draw_networkx_nodes(self.graph, self.graph_pos)
        nx.draw_networkx_labels(self.graph, self.graph_pos, font_size=10, font_family="sans-serif")
        
        
        #edges
        ax = plt.gca()
        for normal, with_data in zip(G.edges, G.edges(data=True)):
            u, v, i = normal
            w = with_data[2]['label']
            rad = 1 * i
            
            ax.annotate("",
                xy=pos[u],
                xytext=pos[v],
                arrowprops=dict(
                    arrowstyle="-", color="0.2",
                    # shrinkA=5, shrinkB=5,
                    # patchA=None, patchB=None,
                    connectionstyle="arc3,rad=rrr".replace('rrr',str(rad)))
                )
            
            ax.annotate(
                w,
                xy=pos[u],
                xytext=calculate_midpoint(pos[u], pos[v], rad)
            )
 

        
        ax.axis('off')
        self.figure_canvas_agg.draw()
        self.window.Refresh()

        
    def run(self):
        self.draw()
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break      
            
            if event == '-BUSCAR-':
                if values['-ORIGEM-'] == values['-DESTINO-']:
                    sg.popup_error("Origem e destino não podem ser iguais")
                    continue
                
                solucao, ordem = self.search_algorithms[values['-ALGORITMO-']](
                    values['-ORIGEM-'], values['-DESTINO-'], 
                    self.costs[values['-CRITERIO-']]
                )
                
                
                if solucao:
                    self.draw()
                    sg.popup(f"SOLUÇÃO: {solucao} \nORDEM DE VISITA: {ordem}", title="Solução")
                else:
                    sg.popup_error("Solução não encontrada\n" + f"SOLUÇÃO: {solucao} \nORDEM DE VISITA: {ordem}")
                    
            
        self.window.close()