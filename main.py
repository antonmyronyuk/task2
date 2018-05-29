#!/usr/bin/env python3

from random import randint
from collections import deque
from argparse import ArgumentParser
# https://docs.python.org/3.6/library/argparse.html


def simulate_random(nodes_num, packages_num=4):
    """
    Each node sends packets to random nodes. If node have already
    received a package it wouldn't sent it to others. Also node
    may send package to yourself (it simply wasted package)

    """
    def process_node():
        """
        Process current node in queue: set it to visited,
        choose random nodes to send a package
        """
        print(q)
        current = q.popleft()  # remove from queue

        if nodes[current]:
            # already visited, go to next
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
    while q:
        process_node()

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
nodes_count = args.nodes

res = repeat(iterations, nodes_count, 4)
print('In {0}% cases all nodes received the packet'.format(res))
