programa
{
	//libs
	inclua biblioteca Matematica --> mat
	
	funcao inicio(){
		//variáveis
		real salario, imposto = 0.00, desconto_dependentes = 0.00
		inteiro n_dependentes = 0 // numero de dependentes
		
		//aliquotas
		const real aliquota1 = .0000
		const real aliquota2 = .0750
		const real aliquota3 = .1500
		const real aliquota4 = .2250
		const real aliquota5 = .2750

		//descontos
		const real descontos1 = 0.00
		const real descontos2 = 158.40
		const real descontos3 = 370.40
		const real descontos4 = 651.73
		const real descontos5 = 884.96
		
		//inputs
		escreva("Qual é o salário do funcionário? ")		leia(salario)
		escreva("quantos dependentes? ")				leia(n_dependentes)
		
		limpa()
		
		escreva("Salário: R$", salario, "\nDependentes: ", n_dependentes)
		escreva("\n\nValor da base de cálculo: R$", salario)

		//lógica
		se(salario <= 2112){
			desconto_dependentes = n_dependentes * descontos1
			imposto = salario * aliquota1 - desconto_dependentes
			escreva("\nAlíquota aplicada: %", mat.arredondar(aliquota1 * 100,2))
		}
		senao se(salario <= 2826.65){
			desconto_dependentes = n_dependentes * descontos2
			imposto = salario * aliquota2 - desconto_dependentes
			escreva("\nAlíquota aplicada: %", mat.arredondar(aliquota2 * 100,2))
		}
		senao se(salario <= 3751.05){
			desconto_dependentes = n_dependentes * descontos3
			imposto = salario * aliquota3 - desconto_dependentes
			escreva("\nAlíquota aplicada: %", mat.arredondar(aliquota3 * 100,2))
		}
		senao se(salario <= 4664.68){
			desconto_dependentes = n_dependentes * descontos4
			imposto = salario * aliquota4 - desconto_dependentes
			escreva("\nAlíquota aplicada: %", mat.arredondar(aliquota4 * 100,2))
		}
		senao se(salario > 4664.68){
			desconto_dependentes = n_dependentes * descontos5
			imposto = salario * aliquota5 - desconto_dependentes
			escreva("\nAlíquota aplicada: %", mat.arredondar(aliquota5 * 100,2))
		} senao { escreva("Valor inválido") }

		//caso imposto negativo
		se (imposto < 0){imposto = 0.00}
		
		escreva("\nDescontos aplicados para ", n_dependentes, " dependentes: R$", desconto_dependentes)
		escreva("\n\nVALOR DO IR: R$", mat.arredondar(imposto, 2))
		escreva("\nSALÁRIO LIQUIDO: R$", salario-imposto)
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 75; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */