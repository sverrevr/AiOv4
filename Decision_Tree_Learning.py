import random

class Node:
    def __init__(self):
        self.value = -1
        self.children = {}

def Plurality_Value(examples):
    classcount = {1:0, 2:0}
    #Skriver ned antallet av hver klassifikasjon
    for line in examples:
        classcount[line[-1]] += 1
    #Returnerer den største
    if(classcount[1] == classcount[2]):
        return random.randrange(1,2,1)
    else:
        return max(classcount, key=lambda i: classcount[i])

    
def Same_Classification(examples):
    #tester om alle har samme klassifikasjon
    classification = examples[0][-1];
    for element in examples:
        #siste element er klassifikasjonen
        if(element[-1] != classification):
            return False
    return True

def Find_Most_Important_Attribute(examples, attributes):
    gains = []
    # defining class 1 as positive
    p = 0
    for elem in examples:
        if elem[-1]==1:
            p+=1
    n = len(examples)-p
    
    for A in attributes:
        gain = B(p/(p+n)) - Remainder(A)
        gains.append((gain, A))

    gains.sort()
    return gains[-1]

def B(q):
    return (q-1)*log(1-q, 2) - q*math.log(q, 2)

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

    return (p1+n1)*B(p1/(p1+n1))/len(examples) + (p2+n2)*B(p2/(p2+n2))/len(examples)

def Random_Attribute(attributes):
    #for testing purposes:
    return attributes[0]
    #rand = random.randrange(0,len(attributes),1)
    #return attributes[rand] 

def Filter_Examples(examples, attribute, value):
    #returerer en list over examples med gitt verdi på gitt attribute
    exs = []
    for element in examples:
        if (element[attribute] == value):
            exs.append(element)
    return exs
    
#Hovedalgoritmen:
def Decision_Tree_Learning(examples, attributes, parent_examples):
    if not examples:
        #print("No more examples")
        return Plurality_Value(parent_examples)
    elif Same_Classification(examples):
        #print("Same class on examples")
        return examples[0][-1]
    elif not attributes:
        #print("No attributes")
        return Plurality_Value(examples)
    else:
        tree = Node()
        tree.value = Random_Attribute(attributes)
        attributes.remove(tree.value)
        
        for value in range(1,3):
            exs = Filter_Examples(examples, tree.value, value)
            subtree = Decision_Tree_Learning(exs, attributes, examples)
            tree.children[value] = subtree
            #print('Child of A', tree.value, '=', value, ' is: ',sep='',end='')
            #if type(tree.children[value]) is int:
                #print('C', tree.children[value], sep='')
            #else:
                #print('A',tree.children[value], sep='')
                
        #print('Children of A', tree.value, tree, tree.children)
        return tree


def Print_Tree(node, tab):
    print(('').ljust(20*tab), end='')
    for i in range(1,3):
        print(('Attribute '+str(node.value)+' = '+str(i)+':').ljust(20), end='')
        if(type(node.children[i]) is int):
            print('Class =',node.children[i])
        else:
            Print_Tree(node.children[i], tab+1)


def Print_Tree_List(tree):
    for value in range(1,3):
        subtree = tree.children[value]
        print('Child of A', tree.value, '=', value, ' is: ',sep='',end='')
        if type(subtree) is int:
            print('C', subtree, sep='')
        else:
            print('A', subtree.value, sep='')
            Print_Tree_List(subtree)
            

#Kjører testdataen gjennom treet og returnerer hvilken klassifisering den fikk
def Classify_Data(data, tree_root):
    node = tree_root
    while not(type(node)==int):
        node = node.children[data[node.value]]
    return node


def main():
    #Leser emseplene
    examples= []
    f = open("training.txt")
    for line in f:
        number_strings = line.split() # Split the line on runs of whitespace
        numbers = [int(n) for n in number_strings] # Convert to integers
        examples.append(numbers)
    #print(examples, "Examples end")

    #Jeg konverterte attributene til 0 indeksering.
    #Så det ekte attribut navnet er en høyere. 
    attributes = [0,1,2,3,4,5,6]

    tree = Decision_Tree_Learning(examples, attributes, examples)

    Print_Tree_List(tree)
    Print_Tree(tree, 0)

    #Leser testene
    tests = []
    f2 = open("test.txt")
    for line2 in f2:
        number_strings2 = line2.split() # Split the line on runs of whitespace
        numbers2 = [int(n) for n in number_strings2] # Convert to integers
        tests.append(numbers)

    classes = []
    wrong = 0
    right = 0
    for elem in tests:
        cls = Classify_Data(elem, tree)
        if(elem[-1] == cls):
            #om vi fant rett klassifisering
            #print(":",elem[-1],",",cls,"\tO")
            right += 1
        else:
            #om vi hadde feil klassifisering
            #print(":",elem[-1],",",cls,"\tX")
            wrong += 1
        classes.append(cls)
        
    percent_right = right / (right+wrong)
    print(percent_right, "of all elements were classified right");


main()
