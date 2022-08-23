#fatorial

from html.entities import name2codepoint


""" f = int(input('Definir fatorial: '))

i = 1
n = 1

while(n <= f):
    i = i * n
    n = n + 1
    print(i) """

primos = []

for i in range(2, int(input('Numero: ')) + 1):
    if 0 not in [i%x for x in range(2,i)]:
        primos.append(i)

print(primos)