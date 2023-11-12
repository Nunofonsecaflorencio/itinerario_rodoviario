class Via:
    def __init__(self, id, loc1, loc2, distance, properties):
        self.id = id
        self.start = loc1
        self.end = loc2
        self.distance = distance
        self.properties = properties # (piso, portagem, velocidade_media)
    
    def get_places(self):
        return (self.start, self.end)
    
    def __repr__(self):
        return f"De {self.start} Para {self.end} Via {self.codigo} características {self.properties}"

    
    def C1(self):
        return self.distance

    def C2(self):
        # C2 - Menor duração prevista
        distance = self.distance
        average_velocity = self.properties[2]  # Índice 2 é a velocidade média
        return distance / average_velocity

    def C3(self):
        # C3 - Menor custo
        distance = self.distance
        road_quality = self.properties[0]  # indice 0 = piso
        tollgates = self.properties[1]  # indice 1 =portagem
        average_velocity = self.properties[2]  # indice 2 = velocidade média

        peso_distancia = 1
        peso_piso = 0.5
        peso_portagem = 2
        peso_vel_med = 0.2

        custo_total = (
            peso_distancia * distance +
            peso_piso * (5 - road_quality) +
            peso_portagem * tollgates +
            peso_vel_med * (1 / average_velocity)
        )


        return custo_total