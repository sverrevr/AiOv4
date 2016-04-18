import random

class Tree_Class:
    value = 0
    #Siden oppgaven absolutt skulle 1 indeksere blir det første elemtet aldrig brukt
    #Barna kan enten være en annen trenode eller en int hvis vi er på en bladnode
    #denne inten er da klassifiseringen.
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
        return random.randrange(1,2,1)

    
def Same_Classification(examples):
    #tester om alle har samme klassifikasjon
    classification = examples[0][-1];
    for line in examples:
        #siste element er klassifikasjonen
        if(line[-1] != classification):
            return False
    return True

def Find_Most_Important_Attribute(examples, attributes):
    #Det er het vi skal bruke etropi og stuff for å finne den viktigste
    return attributes[0];
    #rand = random.randrange(0,len(attributes),1)
    #return attributes[rand]
    

def Splice_Examples(examples, attribute, value):
    #returerer en list over examples med gitt verdi på gitt atribute
    exs = []
    for row in examples:
        if (row[attribute] == value):
            exs.append(row)
    return exs
    
#Hoved algoritmen:
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
        #Lager en ny trenode som spillet på den viktigste atributen.
        #Disse trenodene sendes oppover i rekusjonsrekke og
        #kobles på noden over.
        tree = Tree_Class()
        tree.value = Find_Most_Important_Attribute(examples,attributes);
        #fjerner attributen vi nå har brukt opp
        attributes.remove(tree.value)
        #Går gjennom alle verdiene attributen kan ha, altså 1 og 2.
        for value in range(1,3):
            #Finner alle eksemplene med denne verdien på rett atribut
            exs = Splice_Examples(examples,tree.value,value);
            #Kjører denne algoritmen igjen med bare disse eksemplene
            subtree = Decision_Tree_Learning(exs, attributes, examples)
            tree.child[value] = subtree
        return tree

#Denne fantastiske print funksjonen skriver nedover mot venstre.
#Når det kommer en blad node (har bokstaven C forran seg og en ekstra newline)
#går treet opp et nivå og så andre veien. Gjør det veldig vannskelig å
#dekode hvordan treet ser ut. 
def Print_Tree(tree):
    print(tree.value)
    for i in range(1,3):
        if(type(tree.child[i]) is int):
            print("C", tree.child[i])
            print()
        else:
            Print_Tree(tree.child[i])

#Kjører testdataen gjennom treeet og returnerer hvilken klassifisering den fikk
def Classify_Data(data, tree_root):
    classification = []
    tree = tree_root
    for elem in data:
        if(type(tree) == int):
            #Vi har nådd en klassifisering
            return tree;
        else:
            tree = tree.child[elem]

def main():
    #Leser emseplene
    examples= []
    f = open("training.txt")
    for line in f:
        number_strings = line.split() # Split the line on runs of whitespace
        numbers = [int(n) for n in number_strings] # Convert to integers
        examples.append(numbers)
        #print(examples)

    #Jeg konverterte attributene til 0 indeksering.
    #Så det ekte attribut navnet er en høyere. 
    attributes = [0,1,2,3,4,5,6]

    tree = Decision_Tree_Learning(examples, attributes, examples)
    Print_Tree(tree);

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
    for line3 in tests:
        cls = Classify_Data(line3,tree)
        if(line3[-1] == cls):
            #om vi fant rett klassifisering
            print(":",line3[-1],",",cls,"\tO")
            right += 1
        else:
            #om vi hadde feil klassifisering
            print(":",line3[-1],",",cls,"\tX")
            wrong += 1
        classes.append(cls)
        
    avrg_right = right / (right+wrong)
    print("On avarage:", avrg_right, "was right");


main()
