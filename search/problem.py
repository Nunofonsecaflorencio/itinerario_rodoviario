from .via import Via

class RoadIteneraryProblem:
    def __init__(self, data_filepath):
        
        self.vias = []
        self.places = set()
        self.graph = dict()
        
        self.fetch_data(data_filepath)
    
    def fetch_data(self, filepath):
        
        with open(filepath) as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip().split(",")
            if len(line) != 7:
                continue
            
            id = line[0].strip().lower()
            start= line[1].strip().lower()
            end = line[2].strip().lower()
            distance = float(line[3])
            road_quality = int(line[4])
            tollgates = float(line[5])
            average_velocity = float(line[6])
            
            self.vias.append(Via(id, start, end, distance, (road_quality, tollgates, average_velocity)))
            self.vias.append(Via(id, end, start, distance, (road_quality, tollgates, average_velocity)))
            
            self.places.add(start)
            self.places.add(end)
            
            if start not in self.graph:
                self.graph[start] = []

            if end not in self.graph:
                self.graph[end] = []
            
            self.graph[start].append(self.vias[-2])
            self.graph[end].append(self.vias[-1])
            
    
    def get_neighbors_edges(self, place, min_road_quality=1):
        neighbors = set()
        for via in self.graph[place]:
            
            if via.properties[0] < min_road_quality:
                continue
            
            if place != via.end:
                neighbors.add((via.id, via.end))
                
            if place != via.end:
                neighbors.add((via.id, via.end))
            
        return neighbors
    
    def compute_path_cost(self, path):
        data = {prop: 0 for prop in ['distance', 'avarage_road_quality', 'tollgates', 'avarage_velocity', 'steps', 'C1', 'C2', 'C3']}
        
        for i in range(len(path)-1):
            start, id = path[i]
            end = path[i+1][0]
            
            for v in self.vias:
                if v.start==start and v.id ==id and v.end==end:
                    via = v
                    break

            data['steps'] += 1
            data['distance'] += via.distance
            data['avarage_road_quality'] += via.properties[0]
            data['tollgates'] += via.properties[1]
            data['avarage_velocity'] += via.properties[2]
            data['C1'] += via.C1()
            data['C2'] += via.C2()
            data['C3'] += via.C3()
        
        data['avarage_road_quality']  /= data['steps']
        data['avarage_velocity'] /= data['steps']

       
        return data