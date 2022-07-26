# INE5426 - Construção de Compiladores - Analisador Léxico, Sintático, Semântico e GCI

## Integrantes

Artur Ribeiro Alfa [17103919]  
Augusto Vieira Coelho Rodrigues [19100517]  
Leonardo Vieira Nunes [19102923]  
Thainan Vieira Junckes [19100545]

## Requisitos e Instalação

- Utilizamos Python na versão 3.8.10 e 3.10.4, também é necessário ter o pip instalado

- Utilizamos a ferramenta PLY: https://www.dabeaz.com/ply/ply.html
Ela permite dividir o texto de entrada em uma coleção de tokens ao especificar uma coleção de regras de expressão regular, além de outras funções

- Instalação das dependências:  
    `make setup`

## Execução

- Para executar basta inserir o comando a seguir no terminal:
`make run FILE=arquivo.ccc`

- Exemplo: `make run FILE=exemplos/exemplo1.ccc`
