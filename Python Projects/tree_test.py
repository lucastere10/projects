#criar árvore
from turtle import ycor

#strings da árvore
tree_string = "@"
space_string = ' '
base_string = '|'
star_string = "*"

#input de valores
tree_input =  round(float(input("Quantos andares tem sua árvore: ")))
base_input = round(float(input("Qual o tamanho do caule da sua árvore: ")))
tree_list = range(1, tree_input + 1, 1)
base_list = range(1, base_input + 1, 1)

#valores iniciais
space = tree_input - 1  #espaço árvore
tree_leaf = 1 #somatório por andar da árvore
base = tree_input - 2 #tamanho do caule

#estrela no top da árvore
print(space_string * space +  star_string * tree_leaf)

#printar folhas da árvore
for n in tree_list:
    print(space_string * space +  tree_string * tree_leaf)
    #cálculos
    space = space - 1
    tree_leaf = tree_leaf + 2

#print base
for n in base_list:
    print((base * space_string) + base_string * 3)
