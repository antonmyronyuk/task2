#!/usr/bin/env python3

import timeit
from random import randint
from collections import deque
from argparse import ArgumentParser
# https://docs.python.org/3.6/library/argparse.html


def simulate_random(nodes_num, packages_num=4):
    """
    Each node sends packets to random nodes. If node have already
    received a package it wouldn't sent it to others.
    :return: True if all nodes have received a package else False
    """
    def process_node():
        """
        Process current node in queue: choose random nodes
        to send a package and set it to visited
        """
        # print(q)
        current = q.popleft()  # remove from queue

        for _ in range(packages_num):
            # choose other node
            receiver = randint(0, nodes_num - 2)
            # to avoid sending packages to myself
            receiver += 1 if receiver >= current else 0

            if not nodes[receiver]:
                nodes[receiver] = True
                q.append(receiver)

    q = deque()  # queue contain nodes indexes to process

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited
    while q:
        process_node()

    # check if all nodes have received a package
    return all(nodes)


def simulate_group_random(nodes_num, packages_num=4):
    """
    Each node sends packets to random group of nodes. We choose one
    random node and other nodes are neighbour for this random node.
    If node have received a package it wouldn't sent it to others.
    :return: True if all nodes have received a package else False
    """
    def process_node():
        """
        Process current node in queue: choose random group
        of nodes to send a package and set it to visited
        """
        # print(q)
        current = q.popleft()  # remove from queue

        receiver = randint(0, nodes_num - 1)
        group = ((receiver + i) % nodes_num for i in range(packages_num))
        for node_ind in group:
            if not nodes[node_ind]:
                nodes[node_ind] = True
                q.append(node_ind)

    q = deque()  # queue contain nodes indexes to process

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited
    while q:
        process_node()

    # check if all nodes have received a package
    return all(nodes)


def simulate_random_registry(nodes_num, packages_num=4):
    """
    We will delete visited nodes from registry and send packages
    only to non-visited nodes. It will be really fast and 100% nodes
    will receive a package
    :return: True if all nodes have received a package else False
    """
    def process_node():
        """
        Process current node in queue: choose random nodes to
        send a package set it to visited, delete it from registry
        """
        # print(q)
        q.popleft()  # remove from queue

        for _ in range(packages_num):
            if not nodes_indexes:
                break
            # choose other node
            receiver = randint(0, len(nodes_indexes) - 1)
            q.append(receiver)
            nodes[nodes_indexes[receiver]] = True  # set to visited
            del nodes_indexes[receiver]

    q = deque()  # queue contain nodes indexes to process

    nodes_indexes = list(range(nodes_num))  # registry
    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited
    del nodes_indexes[0]

    while q:
        process_node()

    # check if all nodes have received a package
    return all(nodes)


def repeat(count, func, *args):
    """
    :param count: number of iterations
    :param func: function to iterate
    :param args: function arguments: nodes_num, packages_num
    :return: percent of cases where all nodes have received a package
    """
    start_time = timeit.default_timer()
    res = sum((int(func(*args)) for _ in range(count))) / count * 100
    return res, timeit.default_timer() - start_time


# ############################ ARGS PARSING ###################################

if __name__ == '__main__':
    parser = ArgumentParser(description='Epidemic simulator')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-n', '--nodes', type=int, metavar='N',
                               help='number of nodes (int)', required=True)
    required_args.add_argument('-i', '--iterations', type=int, metavar='I',
                               help='number of iterations (int)', required=True)

    parser.add_argument('--group', action='store_true',
                        help='smart group random algorithm')
    parser.add_argument('--registry', action='store_true',
                        help='algorithm with indexes registry')
    # if you give two parameters: --group and
    # --registry only group will be used
    arguments = parser.parse_args()

    iterations = arguments.iterations
    nodes_count = arguments.nodes

    if arguments.group:
        func = simulate_group_random
    elif arguments.registry:
        func = simulate_random_registry
    else:
        func = simulate_random

    res = repeat(iterations, func, nodes_count, 4)
    print('In {0:0.1f}% cases all nodes received the packet'.format(res[0]))
    print('Time wasted: {0:0.3f}s'.format(res[1]))
