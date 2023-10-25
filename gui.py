import PySimpleGUI as sg
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from time import sleep

class ItinerarioGUI:
    def __init__(self, graph=nx.complete_graph(5)):
        
        layout = [
            [sg.Canvas(key="-CANVAS-", size=(400, 300))]
        ]
        self.window = sg.Window("Itinerário Rodoviário", layout, finalize=True, element_justification='center')
        
        self.fig, self.ax = plt.subplots()
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.window['-CANVAS-'].TKCanvas)
        self.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        self.graph = graph
        self.graph_pos = nx.spring_layout(self.graph)
    
    
    
    def animate(self):
        for i in range(5):
            self.fig.clf()
            node_colors = ['g' if node == i else 'r' for node in self.graph.nodes]
            nx.draw(self.graph, self.graph_pos, with_labels=True, node_color=node_colors)
            
            # self.figure_canvas_agg.get_tk_widget().forget()
            self.figure_canvas_agg.draw()
            self.window.Refresh()
            print("Drawing")
            sleep(1)
        
    def run(self):
        self.animate()
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break      
            
        self.window.close()