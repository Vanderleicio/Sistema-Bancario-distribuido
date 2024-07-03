# Sistema-Bancario-distribuido
Projeto para desenvolver um sistema de comunicação entre bancos de maneira distribuída, solução do problema 2 da TEC502 MI - Concorrência e Conectividade.

### Sumário 
------------
+ [Como Executar](#como-executar-a-solução)
+ [Introdução](#introdução)
+ [Discussão sobre produto](#Discussão-sobre-produto)
+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Comunicação](#Comunicação)
+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Funcionamento dos componentes](#Funcionamento-dos-componentes)
+ [Conclusão](#conclusão)

## Como executar a solução:
Certifique-se de ter o [Python](https://www.python.org) 3.12 instalado na sua máquina, ou faça o download. É crucial também ter o Docker instalado, porque é através dele que as imagens dos componentes do sistema serão obtidas.

### Obtendo as imagens:
Execute os seguintes comandos para baixar as imagens:
```
docker pull vanderleicio/banco:latest
```

### Executando as imagens obtidas:
Após a obtenção das imagens será necessário executá-las. A quantidade de bancos a que serão instanciados fica a seu critério, mas é importante criar um arquivo "Consorcio.txt" contendo os nomes e o endereço do servidor de cada um dos bancos, da mesma forma que na Figura 1.

![Consorcio](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/blob/main/imagensREADME/consorcio.png)
- **Figura 1:** *Exemplo de arquivo Consorcio.txt. [Autor]*

Para executar copie e cole o comando abaixo substituindo {porta} pelo número da porta onde o servidor fará sua comunicação e {nome} pelo nome do Banco que será executado neste contêiner, certifique-se de que ele seja o mesmo que está presente no arquivo Consorcio.txt e que nenhum outro já esteja rodando com esse nome. Repita o processo para a quantidade de bancos que você deseja iniciar, sempre substituindo {porta} e {nome}.

```
docker run -it -v "$(pwd)/Consorcio.txt:/Consorcio.txt" -p {porta}:{porta} vanderleicio/banco python app.py "{nome}"
```
Pronto, a solução já está executando e funcionando.

## Introdução

O pix tem se mostrado uma tecnologia cada vez mais integrada ao cotidiano da sociedade brasileira, facilitando a execução de transações bancárias costumeiras e permitindo que elas sejam feitas de maneira rápida e fácil, através de celulares, aplicações web e etc. Diante desse contexto, foi proposto o desenvolvimento de uma solução capaz de integrar um consórcio de bancos de um país imaginário que não possui banco central. Esse sistema deve permitir que usuários de qualquer um dos bancos possam manipular suas contas de pessoa jurídica ou de pessoa física, conjunta ou individual, a partir de qualquer um dos terminais, sem que isso apresente qualquer risco a integridade dos seus saldos. Para tal, foi desenvolvido um sistema em Python na versão 3.12, com o uso do framework Flask para o desenvolvimento da API REST fornecida pelos bancos e que será acessada pelos outros bancos, e da bibliotecan"requests" para implementar as comunicações entre os componentes, a interface da comunicação foi desenvolvida com HTML, CSS e JavaScript.

A solução proposta pode ser dividida em três entidades: uma entidade conta, responsável por armazenar e realizar as operações mais básicas necessárias, ou seja, somar e subtrair do seu saldo, garantindo que não haja erro no momento da sua execução; uma entidade banco, que gerencia as contas que estão sob seu escopo, armazenando-as e realizando as transações de uma maneira geral e também garantindo que os saldos sejam restaurados caso haja algum problema nas transações; e uma entidade controller, responsável por estabelecer as comunicações entre os bancos.

Já este relatório é dividido em 3 partes além desta Introdução, sendo elas: a discussão detalhada acerca do desenvolvimento do produto, os resultados e a conclusão.

## Discussão sobre produto

A principal parte da solução, e justamente o foco do problema, é a comunicação entre os servidores dos bancos e os eventuais problemas de concorrência e conectividade que podem acontecer a partir das interações entre as mais diversas solicitações dos usuário. Para garantir a persistência dos dados e da conexão o protocolo de comunicação usado foi o HTTP, além de ter sido solicitado a necessidade de que todas os servidores fossem APIs REST. Atrelado a isso foram desenvolvidos protocolos próprios para garantir a correta comunicação e tratamento das mensagens entre os servidores, eles podem ser visto na Figura 2.

![Protocolos](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/blob/main/imagensREADME/Protocolos.png)
- **Figura 2:** *Protocolos usados na comunicação entre bancos. [Autor]*

Quase todas as ações listadas são executadas ao serem solicitadas pela interface a qual o usuário tem acesso, com exceção da ação de "participante" que é voltada pra a execução do processo de transferência. Dessa forma, ao precisar de qualquer uma das solicitação 

