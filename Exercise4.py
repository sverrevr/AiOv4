import random
import math

class Node:
    def __init__(self):
        self.value = -1
        self.children = {}

def Plurality_Value(examples):
    classcount = {1:0, 2:0}
    for line in examples:
        classcount[line[-1]] += 1
    # ties are broken randomly as specified
    if(classcount[1] == classcount[2]):
        return random.randrange(1,2,1)
    else:
        return max(classcount, key=lambda i: classcount[i])

    
def Same_Classification(examples):
    classification = examples[0][-1];
    for element in examples:
        if(element[-1] != classification):
            return False
    return True

def Find_Most_Important_Attribute(examples, attributes, tiebreak):
    gains = []
    # defining class 1 as positive
    p = 0
    for elem in examples:
        if elem[-1]==1:
            p+=1
    n = len(examples)-p
    
    for A in attributes:
        gain = B(p/(p+n)) - Remainder(A,examples,p)
        gains.append((gain, A))
        
    if tiebreak == 'random':    
        best = (-1, -1)
        #find strict maximum, if equal, change with 50% chance
        for tup in gains:
            if tup[0] > best[0]:
                best = tup
            elif tup[0] == best[0]:
                random.seed()
                chance = random.random()
                if chance > 0.5:
                    best = tup
        return best[1]
    elif tiebreak == 'low':
        # sort first by attribute value in reverse, then infomation gain
        # last elemnt is lowest attribute with highest information gain
        gains = sorted(gains, key=lambda tup: tup[1], reverse=True)
        gains = sorted(gains, key=lambda tup: tup[0])
    else:
        # breaks ties on highest attribute
        gains.sort()
    return gains[-1][1]
            
        

def B(q):
    # avoid logarithm of 0:
    if q == 1 or q == 0:
        return 0
    return (q-1)*math.log(1-q, 2) - q*math.log(q, 2)

def Remainder(attribute, examples, p):
    p1 = 0
    n1 = 0
    for elem in examples:
        if elem[attribute] == 1:
            if elem[-1] == 1:
                p1 += 1
            else:
                n1 += 1
    p2 = p-p1
    n2 = len(examples)-p-n1
    # catch and override division by zero:
    if not p1+n1:
        return (p2+n2)*B(p2/(p2+n2))/len(examples)
    if not p2+n2:
        return (p1+n1)*B(p1/(p1+n1))/len(examples)
    return (p1+n1)*B(p1/(p1+n1))/len(examples) + (p2+n2)*B(p2/(p2+n2))/len(examples)

def Random_Attribute(examples,attributes):
    random.seed()
    rand = random.randrange(0,len(attributes),1)
    return attributes[rand] 

def Filter_Examples(examples, attribute, value):
    # this could probably be done using a single list comprehension
    exs = []
    for element in examples:
        if (element[attribute] == value):
            exs.append(element)
    return exs

    
# importance is a flag of how importance of attributes is determined:
# random
# info-low - information gain, breaks ties by preferring the lowest attribute name
# info-high - information gain, tiebreaking on highest attribute name
# info-random - information gain, random tiebreaking
def Decision_Tree_Learning(examples, attributes, parent_examples, importance):
    if not examples:
        return Plurality_Value(parent_examples)
    elif Same_Classification(examples):
        return examples[0][-1]
    elif not attributes:
        return Plurality_Value(examples)
    else:
        tree = Node()
        if importance == 'random':
            tree.value = Random_Attribute(examples,attributes)
        else:
            tree.value = Find_Most_Important_Attribute(examples,attributes,(importance.split('-')[1]))
        
        attributesRem = [x for x in attributes if x!=tree.value]
        for value in range(1,3):
            exs = [ex for ex in examples if ex[tree.value] == value]
            subtree = Decision_Tree_Learning(exs, attributesRem, examples, importance)
            tree.children[value] = subtree
        return tree

# courtesy of stack overflow
def Print_Tree(node, indent, pathkey, last):
    print(indent, pathkey, '-', end ='', sep='')
    if last:
        indent += '  '
    else:
        indent += '| '
    if (type(node)) is int:
        print('Class',node)
    else:
        print('Attribute',node.value)

        childCount = len(node.children)
        for key in node.children:
            childCount -= 1
            Print_Tree(node.children[key], indent, key, childCount==0)
            

def Classify_Data(data, tree_root):
    node = tree_root
    while not(type(node)==int):
        node = node.children[data[node.value]]
    return node


def main():
    examples= []
    f = open("training.txt")
    for line in f:
        number_strings = line.split() # Split the line on runs of whitespace
        numbers = [int(n) for n in number_strings] # Convert to integers
        examples.append(numbers)

    # attributes are now zero-indexed:
    attributes = range(7)

    tree = Decision_Tree_Learning(examples, attributes, examples, 'info-low')

    Print_Tree(tree, '', ' ', True)
    print()

    tests = []
    f = open("test.txt")
    for line in f:
        number_strings = line.split() # Split the line on runs of whitespace
        numbers = [int(n) for n in number_strings] # Convert to integers
        tests.append(numbers)
        
    wrong = 0
    right = 0
    for elem in tests:
        cls = Classify_Data(elem, tree)
        if(elem[-1] == cls):
            right += 1
        else:
            wrong += 1
        
    percent_right = right /(right+wrong)
    print("{0:.3f} of all elements were classified right".format(percent_right));


main()
