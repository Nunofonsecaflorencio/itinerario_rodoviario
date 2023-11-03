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