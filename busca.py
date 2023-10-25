class Via:
    def __init__(self, cod, loc1, loc2, distancia, caracteristicas):
        self.codigo = cod
        self.origem = loc1
        self.destino = loc2
        self.distancia = distancia
        self.caracteristicas = caracteristicas # (piso, portagem, velocidade_media)
    
    def get_localidades(self):
        return (self.origem, self.destino)
    
    def __repr__(self):
        return f"De {self.origem} Para {self.destino} Via {self.codigo} Caracteristicas {self.caracteristicas}"
    
'''
rede = dicionario{
    str localidade: 
        [lista de Via em que via.origem == localidade]
}
'''

def ler_dados(ficheiro):
    vias = []
    localidades = set()
    arrestas = set()
    rede = dict()
    
    linhas = None
    with open(ficheiro) as f:
        linhas = f.readlines()
    
    for linha in linhas:
        linha = linha.strip().split(",")
        if len(linha) == 0:
            continue
        
        codigo = linha[0].strip().lower()
        origem = linha[1].strip().lower()
        destino = linha[2].strip().lower()
        distancia = float(linha[3])
        piso = int(linha[4])
        portagem = float(linha[5])
        velocidade_media = float(linha[6])
        
        vias.append(Via(codigo, origem, destino, distancia, (piso, portagem, velocidade_media)))
        vias.append(Via(codigo, destino, origem, distancia, (piso, portagem, velocidade_media)))
        localidades.add(origem)
        localidades.add(destino)
        
        if origem not in rede:
            rede[origem] = []

        if destino not in rede:
            rede[destino] = []
        
        rede[origem].append(vias[-2])
        rede[destino].append(vias[-1])
        
        arrestas.add((origem, destino))
        
    return vias, localidades, arrestas, rede


    

def dfs(rede, origem, destino, funcao_custo):
    fronteira = [origem]
    visitado = set()
    parentes = {origem: None}
    ordem = []
    
    while fronteira:
        localidade = fronteira.pop(0)
        
        ordem.append(localidade)
        
        if localidade == destino:
            
            solucao = [(destino, None)]
            nodo = destino
            
            while parentes[nodo]:
                solucao.insert(0, parentes[nodo])
                nodo = parentes[nodo][0]
            # solucao.insert(0, parentes[nodo])
            
            return solucao, ordem
        
        visitado.add(localidade)
        
        
        for via in rede[localidade]:
            if not via.destino in visitado:
                fronteira.append(via.destino)
                parentes[via.destino] = (localidade, via.codigo)
        
    return None, ordem # sem solução

