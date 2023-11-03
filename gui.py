import PySimpleGUI as sg
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from time import sleep

# sg.theme_previewer() 
sg.theme('DarkTeal9') 
sg.set_options(font=("Comic Sans",16))

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

def remove_duplicates(input_list):
    seen = set()
    output_list = []

    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)

    return output_list


def draw_arrow(ax, posA, posB, radius, c='0.4', tickness=0.1):
    
  
    ax.annotate("",
                xy=posA,
                xytext=posB,
                arrowprops=dict(
                    arrowstyle="-", color=c,
                    connectionstyle="arc3,rad=rrr".replace('rrr',str(radius)),
                    linewidth=tickness
                )
            )

def draw_label(ax, label, posA, posB,radius):
    ax.annotate(
                label,
                xy=posA,
                xytext=calculate_midpoint(posA, posB, radius),
                fontsize=6
            )

def plot_pointer(ax, pos, size):
    # Define the points of the arrow/triangle
    x = pos[0]
    y = pos[1]
    arrow_points = [(x - size, y - size), (x + size, y - size), (x, y + size)]

    ax.annotate(
        "",
        xy=pos, xytext=(x, y - size),
        arrowprops=dict(
                    arrowstyle="->", color="gold",
                    linewidth=5
                )
    )



class ItinerarioGUI:
    def __init__(self, network, functions):
        
        self.network = network
        self.functions = functions
        
        layoutA = [[
            sg.Col([
                [sg.T("Origem", size=(1, 1), expand_x=True), sg.Combo(list(network.keys()), key="-ORIGEM-", expand_x=True)],
                [sg.T("Destino", size=(1, 1), expand_x=True), sg.Combo(list(network.keys()), key="-DESTINO-", expand_x=True)],
            ], expand_x=True),
            sg.Col([
                [sg.T("Critério", size=(1, 1), expand_x=True), sg.Combo(list(functions['costs']), default_value=list(functions['costs'])[0], key="-CRITERIO-", expand_x=True)],
                [sg.T("Algoritmo", size=(1, 1), expand_x=True), sg.Combo(list(functions['search_algorithms']), default_value=list(functions['search_algorithms'])[0], key="-ALGORITMO-", expand_x=True)],
            ], expand_x=True)
        ]]
        
        layoutB = [
            [sg.Button("Buscar", key='-BUSCAR-', button_color='lime green', size=(16, 2), expand_x=True)],
            [sg.Button("Rearranjar", key='-REARRANJAR-', expand_x=True), sg.Button("Reset", key='-LIMPAR-', expand_x=True)],
        ]
        
        layout = [
            [sg.Canvas(key="-CANVAS-", background_color='black', expand_x=True)],
            [sg.Column(layoutA, expand_x=True), sg.VSeparator(), sg.Column(layoutB, expand_x=True)]
        ]
        
        
        self.window = sg.Window("Itinerário Rodoviário", layout, finalize=True)
        

        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(12, 7)
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.fig.set_facecolor('lightcyan')
        
        self.figure_canvas_agg = FigureCanvasTkAgg(self.fig, self.window['-CANVAS-'].TKCanvas)
        self.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        self.initialize(network)
    
    def initialize(self, network):
        self.graph = nx.MultiGraph()
        
        dont_add = set()
        for loc, vias in network.items():
            for via in vias:
                if (loc, via.destino, via.distancia) not in dont_add:
                    self.graph.add_edge(loc, via.destino,
                                        label=f"{via.codigo.upper()}",
                                        via=via.codigo
                                        )
                    dont_add.add((via.destino, loc, via.distancia))
            
        self.graph_pos = nx.spring_layout(self.graph)
        
        
        

    def draw(self, highlights={}):
        G = self.graph
        pos = self.graph_pos
        
        self.fig.clf()
        
        #edges
        ax = plt.gca()
        for normal, with_data in zip(G.edges, G.edges(data=True)):
            u, v, i = normal
            w = with_data[2]['label']
            code = with_data[2]['via']
            rad = 1 * i
            
            # arrow
            k = (u, code, v)
            color = highlights[k]['color'] if k in highlights else None
            k = (v, code, u)
            color = highlights[k]['color'] if k in highlights else color
            
            if not color:
                draw_arrow(ax, pos[u], pos[v], rad)
            else:
                draw_arrow(ax, pos[u], pos[v], rad, color, tickness=3)
                
            # label
            draw_label(ax, w, pos[u], pos[v], rad*2)
 
         # nodes
        colors = [highlights[node]['color'] if node in highlights else 'skyblue' for node in G.nodes ]
        nx.draw_networkx_nodes(self.graph, self.graph_pos, node_color=colors, node_size=1500)
        labels = labels = {node: node.title() for node in G.nodes()}
        nx.draw_networkx_labels(self.graph, self.graph_pos, labels=labels, font_size=12, font_family="sans-serif", font_weight="bold", font_color="black")
        
        
        if highlights.get('point_to'):
            plot_pointer(ax, pos[highlights['point_to']], size=0.2)
        
        ax.axis('off')
        self.figure_canvas_agg.draw()
        self.window.Refresh()
    
    def animate(self, nodes, solution, speed):
        highlights = {} 
        nodes = remove_duplicates(nodes)
        
        for node in nodes:
            highlights[node] = {'color': 'orange'}
            highlights['point_to'] = node
            self.draw(highlights)
            sleep(speed*0.01)
            
            for sucessor, _ in self.functions['get_sucessors'](node):
                if highlights.get(sucessor):
                    continue
                highlights[sucessor] = {'color':'gray'}
                # self.draw(highlights)
                # sleep(speed * 0)
            
            sleep(speed / 4)
            
            
            
        # Solution
        for i in range(len(solution)):
            node, via_cod = solution[i]
            highlights[node] = {'color': 'green'}
            
            self.draw(highlights)
            sleep(speed / 5)
            
            if i < len(solution) - 1:
                highlights[(node, via_cod, solution[i+1][0])] = {'color': 'green'}
            
            
            self.draw(highlights)
            sleep(speed / 6)
            
        
    def run(self):
        self.draw()
        
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break      
            
            if event == '-LIMPAR-':
                self.draw()

            if event == '-REARRANJAR-':
                self.initialize(self.network)
                self.draw()
            
            if event == '-BUSCAR-':
                if values['-ORIGEM-'] == values['-DESTINO-']:
                    sg.popup_error("Origem e destino não podem ser iguais")
                    continue
                
                solucao, ordem = self.functions['search_algorithms'][values['-ALGORITMO-']](
                    values['-ORIGEM-'], values['-DESTINO-'], 
                    self.functions['costs'][values['-CRITERIO-']]
                )
                
                
                if solucao:
                    self.animate(ordem, solucao, speed=0.5)
                    # sg.popup(f"SOLUÇÃO: {solucao} \nORDEM DE VISITA: {ordem}", title="Solução")
                else:
                    sg.popup_error("Solução não encontrada\n" + f"SOLUÇÃO: {solucao} \nORDEM DE VISITA: {ordem}")
                    
            
        self.window.close()