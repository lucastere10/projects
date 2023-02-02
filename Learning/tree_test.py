#criar árvore
from turtle import ycor

#strings da árvore
tree_string = "@"
space_string = ' '
base_string = '|'
star_string = "*"

#input de valores
tree_string = input('Qual string utilizar para criar sua árvore: ')
tree_input =  round(float(input("Qual é o tamanho da sua árvore: ")))
base_input = round(float(input("Qual o tamanho do tronco da sua árvore: ")))
star_input = bool(input('Deseja adicionar uma estrela no topo da sua árvore? (Deixar vazio caso negativo): '))

tree_list = range(1, tree_input + 1, 1)
base_list = range(1, base_input + 1, 1)

#valores iniciais
n_space = tree_input - 1  #espaço árvore
n_leaf = 1 #somatório por andar da árvore
n_base = tree_input - 2 #tamanho do caule

#estrela no top da árvore
if star_input == True:
    print(space_string * n_space +  star_string * n_leaf)

#printar folhas da árvore
for n in tree_list:
    print(space_string * n_space +  tree_string * n_leaf)
    #cálculos
    n_space = n_space - 1
    n_leaf = n_leaf + 2

#print base
if tree_input >= 3:   
    for n in base_list:
        print((n_base * space_string) + base_string * 3)

print('Árvore criada com sucesso!')