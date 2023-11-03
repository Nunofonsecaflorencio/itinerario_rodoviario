from random import shuffle

def DepthFirstSearch(start, end, get_neighbors_edges, compute_path_proprieties, do_shuffle=True):
    frontier = [start]
    visited = set()
    
    parents = {start: None}
    order = list()
    
    while frontier:
        node = frontier.pop()

        order.append(node)

        if node == end:
            path = reconstruct_path(parents, end)
            return {
                'solution': path,
                'order': order, 
                'computations': compute_path_proprieties(path)
            }
        
        visited.add(node)
        
        edges = list(get_neighbors_edges(node))
        if do_shuffle:
            shuffle(edges)
            
        for edge_id, neighbor in edges:
            if neighbor not in visited:
                frontier.append(neighbor)
                parents[neighbor] = (node, edge_id)

    return {
            'solution': None,
            'order': order,
            'computations': {}
            }


def BreadthFirstSearch(start, end, get_neighbors_edges, compute_path_proprieties, do_shuffle=True):
    frontier = [start]
    visited = set()
    
    parents = {start: None}
    order = list()
    
    while frontier:
        node = frontier.pop(0)

        order.append(node)

        if node == end:
            path = reconstruct_path(parents, end)
            return {
                'solution': path,
                'order': order, 
                'computations': compute_path_proprieties(path)
            }
        
        visited.add(node)
        
        edges = list(get_neighbors_edges(node))
        if do_shuffle:
            shuffle(edges)
            
        for edge_id, neighbor in edges:
            if neighbor not in visited:
                frontier.append(neighbor)
                parents[neighbor] = (node, edge_id)

    return {
            'solution': None,
            'order': order,
            'computations': {}
            }

def reconstruct_path(parents, to):
    path = [(to, None)]
    node = to
    while parents[node]:
        path.insert(0, parents[node])
        node = parents[node][0]
    return path


