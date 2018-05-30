#!/usr/bin/env python3

import sys
import timeit
from random import randint
from collections import deque  # deque is faster than Queue
from argparse import ArgumentParser
# https://docs.python.org/3.6/library/argparse.html


# ############################ HELP FUNC ###################################
def start_epidemic(queue, nodes, func_process_node, *args, **kwargs):
    """
    Process all nodes in queue. Stop process when queue is empty
    or all nodes have already received a package
    :param queue: nodes indexes to process
    :param nodes: bool array which stores if node received package
    :param func_process_node: func which sends packages to other nodes
    :param args: args for func_process_node
    :param kwargs: kwargs for func_process_node
    :return: number of iterations
    """
    it_num = 0  # iterations number
    # stop loop if all nodes already received package
    while queue and not all(nodes):
        it_num += 1
        func_process_node(*args, **kwargs)
    return it_num


# ############################ ALGORITHM 1 ###################################
def simulate_random(nodes_num, packages_num=4):
    """
    Each node sends packages to random nodes. If node have already
    received a package it wouldn't sent it to others.
    There node may send packages more than once to other node.
    For example it may choose such nodes: 5, 8, 8, 3
    :return: True if all nodes have received a package else False
    and iterations number
    """
    def process_node():
        """
        Process current node in queue: choose random nodes
        to send a package and set current node to visited
        """
        # also I have checked variant with shuffle:
        # receivers = list(range(nodes_num))
        # shuffle(receivers)

        # it helps to avoid sending packages from one node more
        # than one time to other node and gives nearly 75% success
        # but it is VERY slow (~0.45s) and use a lot of memory

        current = q.popleft()  # remove from queue

        for _ in range(packages_num):
            # choose other node from all (except of myself)
            receiver = randint(0, nodes_num - 2)
            # offset receiver to avoid sending packages to myself
            # receiver += 1 if receiver >= current else 0
            if receiver >= current:  # it is faster than line above
                receiver += 1

            # let nodes_num = 20, packages_num = 4
            # for example: (current = 0, receiver = 18) => receiver = 19
            # for example: (current = 10, receiver = 5) => receiver = 5
            # for example: (current = 5, receiver = 8) => receiver = 9
            # for example: (current = 5, receiver = 4) => receiver = 4
            # for example: (current = 5, receiver = 5) => receiver = 5

            # following this rules we will avoid sending of package
            # from current to current (to itself)

            if not nodes[receiver]:
                # if not visited, visit it and add to queue
                nodes[receiver] = True
                q.append(receiver)

    q = deque()  # queue contain nodes indexes to process

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited

    it_num = start_epidemic(q, nodes, process_node)  # main process

    # check if all nodes have received a package
    return all(nodes), it_num


# ############################ ALGORITHM 1_1 ###################################
def simulate_random_unique(nodes_num, packages_num=4):
    """
    Each node sends packets to unique random nodes. If node have
    already received a package it wouldn't sent it to others.=
    :return: True if all nodes have received a package else False
    and iterations number
    """
    def process_node():
        """
        Process current node in queue: choose random nodes
        to send a package and set current node to visited
        """

        current = q.popleft()  # remove from queue
        # choose only unique nodes
        lst = list(range(nodes_num))  # like registry

        # to avoid sending packages from node to itself we just
        # delete it from registry
        del lst[current]

        for _ in range(packages_num):
            if not lst:
                # exit if all were visited
                break

            receiver = randint(0, len(lst) - 1)

            if not nodes[lst[receiver]]:
                # if not visited, visit it and add to queue
                nodes[lst[receiver]] = True
                q.append(lst[receiver])

            del lst[receiver]  # delete from registry

    q = deque()  # queue contain nodes indexes to process

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited

    it_num = start_epidemic(q, nodes, process_node)  # main process

    # check if all nodes have received a package
    return all(nodes), it_num


# ############################ ALGORITHM 2 ###################################
def simulate_group_random(nodes_num, packages_num=4):
    """
    Each node sends packets to random group of nodes. We choose one
    random node and other nodes are neighbours for this random node.
    If node have received a package it wouldn't sent it to others.
    :return: True if all nodes have received a package else False
    and iterations number
    """
    def process_node():
        """
        Process current node in queue: choose random group
        of nodes to send a package and set it to visited
        """
        current = q.popleft()  # remove from queue
        receiver = randint(0, nodes_num - 1)  # first element in group

        # to avoid sending packages from node to itself we choose not 4
        # but 5 elements in group and if current node is in group, we
        # just remove it, else we remove last element in group

        group = [(receiver + i) % nodes_num for i in range(packages_num + 1)]

        if current in group:
            group.remove(current)
        else:
            group.pop()

        # let nodes_num = 20, packages_num = 4, current = 6
        # for example: receiver = 5, so we have a group = [5, 7, 8, 9]
        # for example: receiver = 18, so we have a group = [18, 19, 0, 1]

        for node_ind in group:
            if not nodes[node_ind]:
                # if not visited, visit it and add to queue
                nodes[node_ind] = True
                q.append(node_ind)

    q = deque()  # queue contain nodes indexes to process

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited

    it_num = start_epidemic(q, nodes, process_node)  # main process

    # check if all nodes have received a package
    return all(nodes), it_num


# ############################ ALGORITHM 3 ###################################
def simulate_random_registry(nodes_num, packages_num=4):
    """
    We will delete visited nodes from registry and send packages
    only to non-visited nodes. It will be really fast and 100% nodes
    will receive a package
    :return: True if all nodes have received a package else False
    and iterations number
    """
    def process_node():
        """
        Process current node in queue: choose random nodes to
        send a package, set it to visited, delete it from registry
        """
        q.popleft()  # remove from queue

        for _ in range(packages_num):
            if not nodes_indexes:
                # exit if all were visited
                break

            # choose other node from nodes_indexes
            receiver = randint(0, len(nodes_indexes) - 1)
            q.append(nodes_indexes[receiver])  # add to queue
            nodes[nodes_indexes[receiver]] = True  # set to visited
            del nodes_indexes[receiver]  # delete from registry

    q = deque()  # queue contain nodes indexes to process

    # registry of non-visited nodes (it is not very good to use list
    # there because we need to delete single-items from there but if we
    # used non-list there, we would get problem with random generating)
    nodes_indexes = list(range(nodes_num))

    # False - node is not visited (hasn't received a package earlier)
    # True - visited (already have received a package)
    nodes = [False] * nodes_num

    q.append(0)  # start from 0 node
    nodes[0] = True  # set it to visited
    del nodes_indexes[0]  # delete visited node from registry

    it_num = start_epidemic(q, nodes, process_node)  # main process

    # check if all nodes have received a package
    return all(nodes), it_num


# ############################## REPEATER #####################################
def repeat(count, func, *args, **kwargs):
    """
    Repeat 'func' executing 'count' times
    :param count: number of iterations
    :param func: function to iterate
    :param args: func arguments: nodes_num, packages_num
    :return: percent of cases where all nodes have received a package,
    time wasted (sec), iterations number (average for one func call)
    """
    start_time = timeit.default_timer()
    results = [func(*args, **kwargs) for _ in range(count)]
    finish_time = timeit.default_timer()

    percent = sum(int(item[0]) for item in results) / count * 100
    avg_iterations = sum(item[1] for item in results) / count

    return percent, finish_time - start_time, avg_iterations


if __name__ == '__main__':

    # ############################ ARGS PARSING ###################################
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
    parser.add_argument('--unique', action='store_true',
                        help='algorithm with unique random')
    # if you give two parameters: --group and
    # --registry only group will be used
    arguments = parser.parse_args()

    iterations = arguments.iterations
    nodes_count = arguments.nodes
    if iterations <= 0 or nodes_count <= 0:
        print('Iterations number and nodes number should be greater than 0')
        sys.exit()

    if arguments.group:
        func = simulate_group_random
    elif arguments.registry:
        func = simulate_random_registry
    elif arguments.unique:
        func = simulate_random_unique
    else:
        func = simulate_random

    # ############################ REPEATING ###################################
    res = repeat(iterations, func, nodes_count, 4)
    print('\nIn {0:0.1f}% cases all nodes received the packet'.format(res[0]))
    print('Time wasted: {0:0.3f}s'.format(res[1]))
    print('Average number of iterations (in queue): {0:0.3f}'.format(res[2]))

    # we count only processing of node as single iteration
    # in fact: number of iterations = number of popleft's from queue

    # algorithm 1 is slow because it generates
    # packages_num=4 random receivers for each iteration and
    # choose a lot of already visited nodes

    # algorithm 1_1 is the most slowest because it should delete
    # already visited nodes from list-registry and should generate
    # packages_num=4 random numbers for each iteration

    # algorithm 2 is faster, because it generate only 1 random value
    # other values are neighbours for this value; also random group is more
    # effective than single random values; as we can see, results
    # of executing algorithm 2 are better than algorithm 1 and 1_1 results

    # algorithm 3 is the best and the fastest because it knows which
    # nodes haven't received a package yet and sends packages to them
    # but, of course, it requires additional memory to store indexes
    # of nodes which haven't received a package yet (registry)
