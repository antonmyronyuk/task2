#!/usr/bin/env python3

from random import randint
from collections import deque, namedtuple
from argparse import ArgumentParser
# https://docs.python.org/3.6/library/argparse.html

# Node = namedtuple('Node', ['pos', 'visited'])


def simulate_random(nodes_num, packages_num=4):
    """
    Each node sends packets to random nodes only once
    """
    def process_package():
        """
        Process current node in queue: set it to visited,
        choose random nodes to send a package
        """
        current = q.popleft()  # remove from queue
        if nodes[current]:
            # already visited, exit
            return
        nodes[current] = True  # set to visited
        for _ in range(packages_num):
            receiver = randint(0, nodes_num - 1)
            q.append(receiver)

    q = deque()  # queue nodes to process

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False for _ in range(nodes_num)]

    q.append(0)  # start from 0 node
    while len(q):
        process_package()

    # check if all nodes received a package
    return all(nodes)


def repeat(count, nodes_num, packages_num):
    return sum(
        (int(simulate_random(nodes_num, packages_num)) for _ in range(count))
    ) / count * 100

# ############################ ARGS PARSING ###################################

parser = ArgumentParser(description='Epidemic simulator')
required_args = parser.add_argument_group('required arguments')
required_args.add_argument('-n', '--nodes', type=int, metavar='N',
                           help='number of nodes (int)', required=True)
required_args.add_argument('-i', '--iterations', type=int, metavar='I',
                           help='number of iterations (int)', required=True)

args = parser.parse_args()

iterations = args.iterations
nodes = args.nodes

res = repeat(iterations, nodes, 4)
print('In {0}% cases all nodes received the packet'.format(res))
