import random

class Tree_Class:
    value = 0
    #Siden oppgaven absolutt skulle 1 indeksere blir det første elemtet aldrig brukt
    child = [None, None, None]

def Plurality_Value(examples):
    class1 = 0
    class2 = 0
    #Skriver ned antallet av hver klassifikasjon
    for line in examples:
        if(line[-1] == 1):
            class1 += 1
        else:
            class2 += 1
    #Returnerer den største
    if(class1 > class2):
        return 1
    if(class2 > class1):
        return 2
    else: #Om de er like returneres en tilfeldig 
        if(random.randrange(0,2,1) == 1):
            return 1
        else:
            return 2

    
def Same_Classification(examples):
    classification = examples[0][-1];
    for line in examples:
        if(line[-1] != classification):
            return 0
    return 1

def Find_Most_Important_Attribute(examples, attributes):
    return attributes[0];
    #rand = random.randrange(0,len(attributes),1)
    #return attributes[rand]
    

def Splice_Examples(examples, attribute, value):
    exs = []
    for row in examples:
        if (row[attribute] == value):
            exs.append(row)
    return exs
    

def Decision_Tree_Learning(examples, attributes, parent_examples):
    if not examples:
        print("No more exapmles")
        return Plurality_Value(parent_examples)
    elif Same_Classification(examples):
        print("Same class on examples")
        return examples[0][-1]
    elif not attributes:
        print("Used all atributes")
        return Plurality_Value(examples)
    else:
        tree = Tree_Class()
        tree.value = Find_Most_Important_Attribute(examples,attributes);
        attributes.remove(tree.value)
        for value in range(1,3):
            exs = Splice_Examples(examples,tree.value,value);        
            subtree = Decision_Tree_Learning(exs, attributes, examples)
            tree.child[value] = subtree
        return tree

def Print_Tree(tree):
    print(tree.value)
    for i in range(1,3):
        if(type(tree.child[i]) is int):
            print("C", tree.child[i])
            print()
        else:
            Print_Tree(tree.child[i])

def Classify_Data(data, tree_root):
    classification = []
    tree = tree_root
    for elem in data:
        if(type(tree) == int):
            return tree;
        else:
            tree = tree.child[elem]

def main():
    examples= []
    f = open("training.txt")
    for line in f:
        number_strings = line.split() # Split the line on runs of whitespace
        numbers = [int(n) for n in number_strings] # Convert to integers
        examples.append(numbers)
        #print(examples)
    
    attributes = [0,1,2,3,4,5,6]

    tree = Decision_Tree_Learning(examples, attributes, examples)
    
    Print_Tree(tree);
    tests = []
    f2 = open("test.txt")
    for line2 in f2:
        number_strings2 = line2.split() # Split the line on runs of whitespace
        numbers2 = [int(n) for n in number_strings2] # Convert to integers
        tests.append(numbers)
    
    classes = []
    wrong = 0
    right = 0
    for line3 in tests:
        cls = Classify_Data(line3,tree)
        if(line3[-1] == cls):
            print(":",line3[-1],",",cls,"\tO")
            right += 1
        else:
            print(":",line3[-1],",",cls,"\tX")
            wrong += 1
        classes.append(cls)
        
    avrg_right = right / (right+wrong)
    print("On avarage:", avrg_right, "was right");


main()
