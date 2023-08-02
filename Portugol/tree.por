programa
{
	funcao inicio(){
		//variáveis
		inteiro x, y, n_espaco, n_base, n_folhas, arvore_input, folha
		caracter caracter_arvore
		
		//input
		escreva("Qual é o tamanho da sua árvore? -> ")
		leia(arvore_input)
		escreva("Escolha o caracter da sua árvore (ex: @): -> ")
		leia(caracter_arvore)
		escreva("Árvore com ", arvore_input, " linhas.\n\n")

		//valores iniciais
		n_espaco = arvore_input - 1  //espaço árvore
		n_folhas = 1 //somatório por andar da árvore
		//n_base = arvore_input - 2 //tamanho do caule

		//printar arvore
		para (x = 1; x < (arvore_input + 1); x++){	
			//printar espaco em branco
			para (y = 1; y < n_espaco+1; y++){
				 escreva(" ")
			}
			
			//printar as folhas
			para (y = 1; y < n_folhas+1; y++){
				 escreva(caracter_arvore)
			}
			
			//atualizar valores das variáveis
			n_folhas = n_folhas + 2
			n_espaco = n_espaco - 1
			escreva("\n")
		}
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 683; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */