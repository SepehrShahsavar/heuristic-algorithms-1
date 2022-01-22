import numpy as np, random

# Terminal set U [0-9]
terminal_set = ['X', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Function set
function_set = ['+', '-', '*', '%']
# Population size
population_size = 5
# Testing period
x = np.linspace(-1, 1, 100)
# Target polynomial
y_true = x ** 3 - x ** 2 + x - 3
# Max depth
max_depth = 5


class Node:
    def __init__(self, value, type):
        self.left = None
        self.data = value
        self.type = type
        self.parent = None  # must be operator or null
        self.right = None


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


def generateRandomForest():
    forest_ = []
    for i in range(0, population_size):
        for i in range(0, 5):
            tree = Node('0', 'null')
            value, data_type = randomOperatorOrOperand((getDepth(tree) + 1 >= max_depth))
            addLeafNode(tree, Node(value, data_type))
            while getFirstFreeOperatorLeafNode(tree) is not None:
                value, data_type = randomOperatorOrOperand((getDepth(tree) + 1 >= max_depth))
                addLeafNode(tree, Node(value, data_type))
            forest_.append(tree)

    return forest_


# safe division
def div(x, y):
    try:
        return x / y
    except ZeroDivisionError:
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


def calculateFitness():
    t_list = []
    for i in range(0, population_size):
        t = Tree(forest[i])
        fx = calculateExpressionTree(t.root)
        err = 0
        if type(fx) is int or type(fx) is float:
            for j in range(0, 100):
                err += (fx - y_true[j]) ** 2
        else:
            for j in range(0, 100):
                err += (fx[j] - y_true[j])**2
        t.fitness = err
        t_list.append(t)
    return t_list

forest = generateRandomForest()
inorder(forest[0])
print('\n')
print(calculateExpressionTree(forest[0]))
calculatedFitnessList = calculateFitness()
for i in calculatedFitnessList:
    print(i.fitness)