#verificador cpf

from audioop import mul

cpf = input('Digite o seu cpf: ')
cpf = int(''.join(c for c in cpf if c.isdigit()))

if len(str(cpf)) == 11:
    cpf_list = [int(a) for a in str(cpf)]
    print(cpf_list)    

    #algoritmo cpf
    #primeiro dígito
    multiplier = 1
    y_sum = 0
    for x in cpf_list[0:9]:
        y = x * multiplier
        y_sum = y_sum + y
        multiplier = multiplier + 1
    verify_01 = y_sum%11
    if verify_01 == 10:
        verify_01 == 0

    #segundo dígito
    multiplier = 0
    y_sum = 0
    for x in cpf_list[0:10]:
        y = x * multiplier
        y_sum = y_sum + y
        multiplier = multiplier + 1
    verify_02 = y_sum%11
    if verify_02 == 10:
        verify_02 == 0

    #verificar validade
    if verify_01 == cpf_list[9] and verify_02 == cpf_list[10]:
        print('CPF Válido')
    else:
        print('CPF Inválido')

else:
    print('número de cpf incorreto')

