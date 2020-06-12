"""
Import Statements:
"""
from util import Stack, Queue  # These may come in handy
from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


"""
UPER
understand and make a plan:

Dictionary to keep track of all of our exits to each room:

    traversal_path = []
    graph = {}
    number_of_rooms = 500  # 500 entries (0-499)
    +----------------+
{
    0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
    coordinates = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops.

Hints:
This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.
"""

"""
You can find the path to the shortest unexplored room by using a breadth-first search for a room with a '?' for an exit. If you use the bfs code from the homework, you will need to make a few modifications.
"""
# our unexplored exits in adventure:


def adventure_exits(graph, current_room):
    return [key for key, value in graph[current_room].items() if value == '?']


def bft(graph, player):
    # Create an empty queue and enqueue the starting vertex ID
    q = Queue()
    q.enqueue([(player.current_room.id, None)])
    # Create a set to store visited
    visited = set()
    # While the queue is not empty...
    while q.size() > 0:
        # Dequeue the first path
        path = q.dequeue()
        # lets grab the last vertex from our path
        v = path[-1][0]
        # lets check if it's the target
        # searching for an exit with a '?' as the value.
        """
        Hints:
        If an exit has been explored, you can put it in your BFS queue like normal.

        BFS will return the path as a list of room IDs.

        """
        if '?' in graph[v].values():
            # if so, will return the path
            return [i[1] for i in path[1:]]
            # if that vertex has not been visited...
        if v not in visited:  # vertices aka nodes
            visited.add(v)
            for key, value in graph[v].items():
                # make a copy of the path before adding
                path_copy = path.copy()
                # print(f"Path copy: {path_copy}")
                path_copy.append((value, key))
                q.enqueue(path_copy)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

"""
Minimum Viable Product
1: Tests do not pass
2: Tests pass with len(traversal_path) <= 2000
3: Tests pass with len(traversal_path) < 960
+--------------------+

Rubric
Student is able to produce a valid traversal path between 960 and 2000
"""

our_counter = 0
score = 2000
lowest_score = 2000

while score > 1500:
    player = Player(world.starting_room)

    """
    You know you are done when you have exactly 500 entries (0-499) in your graph and no '?' in the adjacency dictionaries. to do this, you will need to write a traversal algorithm that logs the path into traversal_path as it walks.
    """

    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']
    """
    BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.
    """
    traversal_path = []
    graph = {}
    number_of_rooms = 500  # 500 entries (0-499)
    """
    {
  0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
}
    """
    coordinates = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

    '''
    Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops.

    '''
    source = None
    previous_room = None
    reverse = True
    visited = set()  # set to keep track of visited nodes.

    while len(visited) < number_of_rooms:
        # let's get a list of all of the exits in our current room
        current_room = player.current_room.id
        # print(f"You are currently in room: {current_room}")

        visited.add(current_room)

        exits = player.current_room.get_exits()  # returns list of exits
        # print(f"The exits are {exits}")

        if current_room not in graph:
            # print(f"This room {current_room} is not in our graph.")
            graph[current_room] = {}
            # print("It was added!")
            # print(f"Our graph length is: {len(graph)}")
            for exit in exits:
                graph[current_room][exit] = '?'
                # compare if equal too, then our condition is true
        if len(visited) == number_of_rooms:
            # increment counter by 1
            our_counter += 1
            if our_counter % 2000 == 0:  # Modulus: + checks if even
                print(f"Attempted: #{our_counter}. Our lowest score is: {lowest_score}.")
            break

        # print(f"length of graph: {len(graph)}")
        if source and reverse:
            graph[current_room][source] = previous_room
        reverse = True
        # print(graph[current_room])
        # our unxplored exits:
        adventure_list = adventure_exits(graph, current_room)
        # print(f"untraversed exits: {adventure_list}")

        # lets record our network/connections:
        # now we randomly select an exit and will move in that general direction:
        #   0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        if len(adventure_list) > 0:
            # select an item from our list:
            direction = random.choice(adventure_list)
            player.travel(direction)
            graph[current_room][direction] = player.current_room.id
            source = coordinates[direction]
            previous_room = current_room

            # print(f'Our travelled directions: {direction}')
            traversal_path.append(direction)
            # print(f"Our traversal path is: {traversal_path}")
        else:
            # We are starting to backtrack: print statment:
            # print("WARNING:You're heading the wrong way!")
            bft_list = bft(graph, player)
            # print(f"Backtracking list: {bft_list}")
            # Avoid duplicates
            for d in bft_list:
                player.travel(d)
                traversal_path.append(d)
            reverse = False
    score = len(traversal_path)
    if score < lowest_score:
        lowest_score = score


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
