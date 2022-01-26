import copy

import numpy as np, pandas as pd
import sys, threading

sys.setrecursionlimit(10000)  # max depth of recursion
threading.stack_size(2 ** 20)
# Terminal set U [0-9]
terminal_set = ['X', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Function set
function_set = ['+', '-', '*', '%']
# Population size
population_size = 500
# Testing period
x = np.linspace(-1, 1, 100)
# Target polynomial
y_true = x ** 3 - x ** 2 + x - 3
# Max depth
max_depth = 5
# elite_size
elite_size = int(population_size * 0.1)


class Node:
    def __init__(self, value, type):
        self.left = None
        self.data = value
        self.type = type
        self.parent = None  # must be operator or null
        self.right = None
        self.id = np.random.rand() * 1000000

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented

        return self.id == other.id


class Tree:
    def __init__(self, root):
        self.root = root
        self.fitness = 0


def inorder(node: Node):
    if node:
        inorder(node.left)
        print(node.data, end="")
        inorder(node.right)


def getDepth(node: Node):
    if node is None:
        return 0
    else:
        ldepth = getDepth(node.left)
        rdepth = getDepth(node.right)

        if ldepth > rdepth:
            return ldepth + 1
        else:
            return rdepth + 1


def randomOperatorOrOperand(depth):
    if depth == 1:
        value = terminal_set[int(np.random.rand() * 12) % 11]
        data_type = 'operand'
        return value, data_type
    else:
        rnd = np.random.rand()
        if rnd <= 0.5:
            value = terminal_set[int(np.random.rand() * 12) % 11]
            data_type = 'operand'
            return value, data_type
        else:
            value = function_set[int(np.random.rand() * 5) % 4]
            data_type = 'operator'
            return value, data_type


def isOperator(value):
    if value in function_set:
        return True
    return False


def getFirstFreeOperatorLeafNode(root):
    res = None
    if root is None:
        return None
    elif root.type == 'operator':
        if root.right is None or root.left is None:
            return root
        if root.left is not None:
            res = getFirstFreeOperatorLeafNode(root.left)
        if res is None and root.right is not None:
            res = getFirstFreeOperatorLeafNode(root.right)
    return res


def addLeafNode(root: Node, node: Node):
    if root.type == 'null':
        root.type = node.type
        root.data = node.data
        node.parent = None
        node.right = None
        node.left = None
    else:
        last_operator_leaf = getFirstFreeOperatorLeafNode(root)
        if last_operator_leaf is not None:
            if last_operator_leaf.left is None:
                last_operator_leaf.left = node
                node.parent = last_operator_leaf.left
            else:
                if last_operator_leaf.right is None:
                    last_operator_leaf.right = node
                    node.parent = last_operator_leaf.right


def generateRandomExprTree(tree):
    value, data_type = randomOperatorOrOperand((getDepth(tree) + 1 >= max_depth))
    addLeafNode(tree, Node(value, data_type))
    while getFirstFreeOperatorLeafNode(tree) is not None:
        value, data_type = randomOperatorOrOperand((getDepth(tree) + 1 >= max_depth))
        addLeafNode(tree, Node(value, data_type))
    return tree


def generateRandomForest():
    forest_ = []
    for i in range(0, population_size):
        tree = Node('0', 'null')
        forest_.append(generateRandomExprTree(tree))

    return forest_


# safe division
def div(x, y):
    try:
        return x / y
    except ZeroDivisionError as e:
        return 1


def calculateExpressionTree(root: Node):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        if root.data == 'X':
            return x
        else:
            return int(root.data)

    left_sum = calculateExpressionTree(root.left)
    right_sum = calculateExpressionTree(root.right)

    if root.data == '+':
        return left_sum + right_sum
    if root.data == '-':
        return left_sum - right_sum
    if root.data == '*':
        return left_sum * right_sum
    if root.data == '%':
        return div(left_sum, right_sum)


def calculateFitness(forest):
    t_list = []
    fitness_sum = 0
    for i in range(0, len(forest)):
        t = Tree(forest[i])
        fx = calculateExpressionTree(t.root)
        err = 0
        if type(fx) is int or type(fx) is float:
            for j in range(0, 100):
                err += (fx - y_true[j]) ** 2
        else:
            for j in range(0, 100):
                err += (fx[j] - y_true[j]) ** 2
        fitness_sum += err
        t.fitness = err
        t_list.append(t)

    return t_list, fitness_sum


def key(e):
    return e.fitness


def selection(elite_size, fitness_sum, calculatedFitnessList):
    calculatedFitnessList.sort(key=key, reverse=True)
    pool = []
    res = []
    for i in range(0, elite_size):
        pool.append(calculatedFitnessList[i])
        res.append(calculatedFitnessList[i])
    for i in range(0, len(calculatedFitnessList) - elite_size):
        pick = int(np.random.rand() * 100)
        for tree in calculatedFitnessList:
            rnd = int(np.random.rand() * 100)
            if div(pick, rnd) > 1:
                pool.append(tree)
                break

    for i in pool:
        if i not in res:
            res.append(i)
    return res


def getNode(root, value):
    if root is None:
        return None
    if root.data == value:
        return root
    n = getNode(root.left, value)
    if n is not None:
        return n
    return getNode(root.right, value)


def inorderString(root, s):
    if root:
        inorderString(root.left, s)
        s.append(root.data)
        inorderString(root.right, s)


def getRandomNode(root):
    s = []
    inorderString(root, s)
    # print(len(s))
    index = int(np.random.rand() * len(s))
    n = getNode(root, s[index])
    return n


def swapSubtrees(root: Node, subtree1: Node, subtree2: Node):
    current = root
    stack = []
    while True:
        if current is not None:
            stack.append(current)
            current = current.left
        elif stack:
            current = stack.pop()
            if current.__eq__(subtree1):
                current.data = subtree2.data
                current.left = subtree2.left
                current.right = subtree2.right
                break

            current = current.right
        else:
            break


def breed(root1: Node, root2: Node):
    g1 = getRandomNode(root1)
    g2 = getRandomNode(root2)
    copy_root = copy.deepcopy(root1)
    # inorder(root1)
    # print()
    # inorder(root2)
    # print()
    # print('*************')
    # inorder(g1)
    # print()
    # inorder(g2)
    # print()
    # print('***************')
    swapSubtrees(copy_root, g1, g2)
    # inorder(copy_root)
    # print()
    # inorder(root2)
    # print()
    return copy_root


def breedPopulation(elite_size, fitness_sum, calculatedFitnessList):
    children = []
    matingpool = selection(elite_size, fitness_sum, calculatedFitnessList)
    length = len(matingpool) - elite_size
    for i in range(0, elite_size):
        children.append(matingpool[i].root)
        # inorder(matingpool[i].root)
        # print()
    for i in range(0, length):
        child = breed(matingpool[i].root, matingpool[len(matingpool) - i - 1].root)
        children.append(child)
    print('********')
    return children


def mutate(root, mutationRate):
    # inorder(root)
    # print()
    if np.random.rand() < mutationRate:
        node = getRandomNode(root)
        # inorder(node)
        # print()
        new_node = Node('0', 'null')
        mutateNode = generateRandomExprTree(new_node)
        # inorder(mutateNode)
        # print()
        swapSubtrees(root, node, mutateNode)
        # inorder(root)
    return root


def mutatePopulation(population):
    mutatePop = []
    for i in range(0, len(population)):
        mutate_child = mutate(population[i], 0.5)
        mutatePop.append(mutate_child)
    return mutatePop


def nextgenaration(forest):
    calculatedFitnessList, fitness_sum = calculateFitness(forest)
    childrens = breedPopulation(elite_size, fitness_sum, calculatedFitnessList)
    nextGen = mutatePopulation(childrens)
    return nextGen


def geneticProgramming():
    forest = generateRandomForest()
    forest = nextgenaration(forest)
    final, sum_fit = calculateFitness(forest)
    tree = copy.deepcopy(final[0])
    for i in range(0, 5000):
        forest = nextgenaration(forest)
        final , sum_fit = calculateFitness(forest)
        if tree.fitness > final[0].fitness:
            tree = tree = copy.deepcopy(final[0])

    inorder(tree.root)
    print()
    print("final fitness: " + str(tree.fitness))

geneticProgramming()


# inorder(forest[0])
# print()
# inorder(forest[1])
# print()

# childrens = breedPopulation(2)
# for t in childrens:
#     inorder(t)
#     print()

# for tree in forest:
#     inorder(tree)
#     print('\n')
#     h = int(np.random.rand() * getDepth(tree))
#     print(h)
#     node = getRandomNode(tree, h)
#     inorder(node)

# for i in calculatedFitnessList:
#     print(i.fitness)
# print("******")
# p = selection(2, fitness_sum)
# for r in p:
#     print(r.fitness)
