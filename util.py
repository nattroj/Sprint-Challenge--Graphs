import sys

OPPOSITE_DIRECTIONS = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def enqueue(self, value):
        node = Node(value)

        if not self.head:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = self.tail.next
        
        self.size += 1
    
    def dequeue(self):
        if not self.head:
            return None

        node = self.head

        self.head = self.head.next

        self.size -= 1

        return node.value

    def __len__(self):
        return self.size

class Graph:
    def __init__(self):
        self.verticies = {}
        self.size = 0
    
    def vertex_exists(self, vertex_id):
        return vertex_id in self.verticies

    def add_vertex(self, vertex_id):
        if not self.vertex_exists(vertex_id):
            self.verticies[vertex_id] = set()
            self.size += 1

    def add_edge(self, v1, v2):
        self.verticies[v1].add(v2)
    
    def __str__(self):
        r_string = ''
        for item in self.verticies.items():
            key, value = item
            r_string += f'{key}: {value}\n'
        
        return r_string
    
    def __len__(self):
        return self.size

class TraversalGraph(Graph):
    def __init__(self):
        super().__init__()
    
    def map_rooms(self, player):
        queue = Queue()
        queue.enqueue(player.current_room)
        visited = set()

        while len(queue):
            current_room = queue.dequeue()

            if current_room.id in visited:
                continue
            
            self.add_vertex(current_room.id)

            for new_room in (current_room.n_to, current_room.s_to, current_room.e_to, current_room.w_to):
                if new_room:
                    self.add_vertex(new_room.id)
                    self.add_edge(current_room.id, new_room.id)
                    self.add_edge(new_room.id, current_room.id)

                    queue.enqueue(new_room)

            visited.add(current_room.id)
    
    def explore_recurse(self, current_room, path, came_from=None, visited=None):
        # initial cases
        
        if not visited:
            visited = set()
        
        if not current_room.id in visited:
            visited.add(current_room.id)
        
        if came_from:
            path.append(came_from)

        # when all rooms have been visited, stop recursing
        if len(visited) == self.size:
            return path
        
        possible_directions = [direction for direction in current_room.get_exits() if direction != OPPOSITE_DIRECTIONS.get(came_from)]

        results = None
        for direction in possible_directions:
            next_room = current_room.get_room_in_direction(direction)

            if next_room.id in visited:
                continue

            results = self.explore_recurse(next_room, path, direction, visited)

            if results is not None:
                return results
        
        if came_from == 'n':
            path.append('s')

        elif came_from == 's':
            path.append('n')

        elif came_from == 'e':
            path.append('w')

        elif came_from == 'w':
            path.append('e')