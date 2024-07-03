# Sistema-Bancario-distribuido
Projeto para desenvolver um sistema de comunicação entre bancos de maneira distribuída, solução do problema 2 da TEC502 MI - Concorrência e Conectividade.

### Sumário 
------------
+ [Como Executar](#como-executar-a-solução)
+ [Introdução](#introdução)
+ [Discussão sobre produto](#Discussão-sobre-produto)
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

O pix tem se mostrado uma tecnologia cada vez mais integrada ao cotidiano da sociedade brasileira, facilitando a execução de transações bancárias costumeiras e permitindo que elas sejam feitas de maneira rápida e fácil, através de celulares, aplicações web e etc. Diante desse contexto, foi proposto o desenvolvimento de uma solução capaz de integrar um consórcio de bancos de um país imaginário que não possui banco central. Esse sistema deve permitir que usuários de qualquer um dos bancos possam manipular suas contas de pessoa jurídica ou de pessoa física, conjunta ou individual, a partir de qualquer um dos terminais, sem que isso apresente qualquer risco à integridade dos seus saldos. Para tal, foi desenvolvido um sistema em Python na versão 3.12, com o uso do framework Flask para o desenvolvimento da API REST fornecida pelos bancos e que será acessada pelos outros bancos, e da biblioteca "requests" para implementar as comunicações entre os componentes, a interface da comunicação foi desenvolvida com HTML, CSS e JavaScript.

A solução proposta pode ser dividida em três entidades: uma entidade conta, responsável por armazenar e realizar as operações mais básicas necessárias, ou seja, somar e subtrair do seu saldo, garantindo que não haja erro no momento da sua execução; uma entidade banco, que gerencia as contas que estão sob seu escopo, armazenando-as e realizando as transações de uma maneira geral e também garantindo que os saldos sejam restaurados caso haja algum problema nas transações; e uma entidade controller, responsável por estabelecer as comunicações entre os bancos.

Já este relatório é dividido em 3 partes além desta introdução, sendo elas: a discussão detalhada acerca do desenvolvimento do produto, os resultados e a conclusão.

## Discussão sobre produto

A principal parte da solução, é justamente o foco do problema, é a comunicação entre os servidores dos bancos e os eventuais problemas de concorrência e conectividade que podem acontecer a partir das interações entre as mais diversas solicitações dos usuários. Para garantir a persistência dos dados e da conexão, o protocolo de comunicação usado foi o HTTP, além de ter sido solicitado a necessidade de que todos os servidores fossem APIs REST. Atrelado a isso foram desenvolvidos protocolos próprios para garantir a correta comunicação e tratamento das mensagens entre os servidores, eles podem ser vistos na Figura 2.

![Protocolos](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/blob/main/imagensREADME/Protocolos.png)
- **Figura 2:** *Protocolos usados na comunicação entre bancos. [Autor]*

Quase todas as ações listadas são executadas ao serem solicitadas pela interface a qual o usuário tem acesso, com exceção da ação de "participante" que é voltada pra a execução do processo de transferência. Dessa forma, ao precisar de qualquer uma das solicitações ela é feita ao servidor, que processa seu resultado e envia para interface, seja confirmando a execução, seja avisando que algo deu errado, ou passando o dado solicitado.

As três principais operações envolvidas no problema e que são as responsáveis por solucioná-lo são a de saque, a de depósito e a de transferência. As operações de depósito e saque normalmente envolvem apenas um banco e por isso não têm um algoritmo voltado a lidar com concorrência, nessas operações uma única ação é feita (somar ou subtrair do saldo da conta correspondente) e para garantir a preservação dos dados, é usado um mutex nos saldos das contas, garantindo que mais de uma operação não possa acessá-lo ao mesmo tempo, garantindo que ele sempre tenha o valor correto. Ao juntar esse aspecto do sistema, com o fato de que o servidor Flask trata suas solicitações de forma independente (inclusive com contextos diferentes), é possível garantir a sincronização e persistência do servidor e dos dados das suas contas, quando mais de uma solicitação é enviada.

Já a operação de transferência pode ser realizada de diversas contas e em tempos diversos, o que pode fazer com que problemas de concorrência ocorram, para gerenciar essa questão foi utilizado o protocolo 2 Phase Commit (2PC), indicado para lidar com consistência e atomicidades das transações. Assim, as transações envolvendo transferências seguem o seguinte modelo:

1 - Uma requisição POST é feita à api do banco em que se está logado, contendo uma lista das contas de origem e os valores que serão retirados delas e a conta de destino;

2 - O servidor que recebe essa solicitação fica responsável por ser o gerente de todo o processo e solicita a cada um dos bancos participantes o voto deles em relação à transação;

3 - Cada um dos bancos participantes recebe a lista das suas contas que estão envolvidas na transação, então eles criam um armazenamento dessa transação gerando um id para ela e guardando os valores que serão colocados ou retirados de cada conta;

4 - Os bancos participantes verificam se todas as contas envolvidas podem enviar o saldo solicitado, se todas poderem ele vota pelo commit, se ao menos uma não puder ele vota pelo cancel;

5 - O banco gerente recebe os votos de cada um dos bancos participantes, e se ao menos um deles tiver votado pelo cancelamento, ele solicita que todos os outros bancos também cancelem (o banco que votou pelo cancelamento, cancela automaticamente sua operação).

6- Se todos os bancos participantes votaram pelo commit, o banco gerente solicita que todos comitem, e eles confirmam suas operações.

Com isso, é possível garantir que o algoritmo de concorrência distribuída seja bem empregado e resolva os possíveis problemas de solicitações concorrentes na prática. Através desse processo também é possível garantir a confiabilidade dos dados quando transações concorrentes são feitas no mesmo banco, garantindo que o saldo fique correto e que os clientes possam fazer suas transações, já que ao fazer a solicitação o banco gerencia e garante que os saldos não sejam alterados por mais de um processo ao mesmo tempo, e o 2PC garante que se em algum momento durante a transação houve um erro que não permitisse sua conclusão, ela seja cancelada e seus dados restaurados.

Já no ponto de vista de confiabilidade, para garantir que não ocorram erros com as transações ou solicitações dos usuários, um algoritmo de timeout é usado toda vez que há alguma comunicação entre os servidores, e um erro é levantado caso algum dos bancos não responda no tempo hábil ou ocorra qualquer outro erro durante a transferência, o que garante que a resposta daquele banco desconectado seja sempre de cancelar e não commitar, e assim anulando a solicitação feita  e informando ao usuário que o banco não pode ser acessado no momento. Quando o banco pode novamente ser acessado, o cliente poderá ver seus saldos nas contas desse banco e fazer solicitações a ele, bem como ver quais são as contas de outros usuários naquele banco, o que volta a permitir que transferências sejam feitas para ele.

### Interface principal do usuário

Após fazer o cadastro da sua conta e o login, o usuário fará as principais operações do sistema no "Painel de Controle", nele será mostrado todas as contas associadas ao CPF dele, tanto no banco quanto em outros bancos do consórcio, a Figura 3 ilustra essa situação, na qual a pessoa tem uma conta conjunta num banco e outra individual em outro, além da conta em que ele já está logado:

![Contas](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/blob/main/imagensREADME/contasLogadas.png)
- **Figura 3:** *Conta logada e as outras contas do usuário. [Autor]*

Além disso, o usuário também pode realizar operações de depósito, saque e transferência, no caso das duas primeiras ele deve selecionar a conta dele que receberá o depósito/saque (Figura 4), já as transferências é preciso selecionar as contas de onde sairá o dinheiro e a conta de destino, selecionando dentre as contas do cpf pesquisado (Figura 5).

![Deposito](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/blob/main/imagensREADME/Depositos.png)
- **Figura 4:** *Interface de depósito/saque. [Autor]*

![Contas](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/blob/main/imagensREADME/transferencia.png)
- **Figura 5:** *Interface de transferência. [Autor]*

## Conclusão

A solução desenvolvida atende aos critérios solicitados no problema, e realiza satisfatoriamente as atividades para as quais ela foi desenvolvida. Ela atende as necessidades de comunicação entre os servidores dos bancos, e a mantém de forma distribuída. Além disso, o sistema mostra-se consistente com relação aos problemas advindos da concorrência entre as solicitações e os dados que elas acessam, como mostram os [testes](https://github.com/Vanderleicio/Sistema-Bancario-distribuido/tree/main/testes) feitos em Shell Script, além de se manter consistente quando há problemas de desconexões.
