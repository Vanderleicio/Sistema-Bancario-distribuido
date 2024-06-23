from models.conta import Conta
from models.transacao import Transacao

# Nome: String, Cpf: String, Tipo: int
# Tipos: PF - P (1), PF - C (2), PJ (3)

class Banco:

    def __init__(self, nome):
        self.ULTIMO_ID = 1
        self.ULTIMA_TRANSACAO = 1
        self.nome = nome
        self.contas = []
        self.transacoes = []
    
    def add_conta(self, nome, cpf, tipo, senha):
        for conta in self.contas:
            if cpf == conta.cpf:
                print("VOCÊ JÁ TEM UMA CONTA DESSE TIPO")
                raise RuntimeError("Conta já existente")

        nova_conta = Conta(self.ULTIMO_ID, nome, cpf, tipo, senha)
        self.ULTIMO_ID += 1
        self.contas.append(nova_conta)
    
    def get_contas_do_cpf(self, n_cpf):
        # Retorna todas as contas associadas ao CPF/CNPJ passado.
        contas = []
        for conta in self.contas:
            #print(n_cpf)
            #print(conta.cpf)
            if n_cpf in conta.cpf:
                contas.append(conta)
        
        return contas
    
    def get_conta_cpf(self, cpfs):
        # Retorna a conta associada ao(s) CPF(s)/CNPJ especificado(s).
        for conta in self.contas:
            if cpfs == conta.cpf:
                print(conta)
                return conta
    
    def get_conta_id(self, id_conta):
        # Retorna a conta associada ao ID.
        for conta in self.contas:
            if id_conta == conta.id:
                return conta
    
    def login(self, cpf, senha):
        return self.get_conta_cpf(cpf).senha == senha
    
    def preparar_saida(self, contas_valor):
        # Protocolo para fazer a retirada de dinheiro de contas
        contas_envolvidas = []
        reservas = []

        for conta in contas_valor:
            conta_envolvida = {'id': conta['id'], 'operacao': 'saida', 'valor': conta['valor']}
            contas_envolvidas.append(conta_envolvida)

        transacao = Transacao(self.ULTIMA_TRANSACAO, contas_envolvidas)
        self.ULTIMA_TRANSACAO += 1
        self.transacoes.append(transacao)

        # Preparacao para transferencia:
        try:
            for conta in contas_valor:
                conta_envolvida = self.get_conta_id(conta['id'])
                conta_envolvida.sub_saldo(conta['valor'])
                reserva = {'id': conta['id'], 'valor': conta['valor']}
                reservas.append(reserva)
            
            transacao.preparar(reservas)
            return [True, self.ULTIMA_TRANSACAO - 1]
        except RuntimeError:
            print("TESTANDOOO")
            for conta in contas_valor:
                conta_envolvida = self.get_conta_id(conta['id'])
                conta_envolvida.add_saldo(conta['valor'])
            return [False, self.ULTIMA_TRANSACAO - 1]
    
    def saida(self, id_transacao):
        try:
            for transacao in self.transacoes:
                if transacao.id == id_transacao:
                    transacao.concluida = True
                    transacao.sucesso = True
                    return True
            return False
        except:
            return False

    def entrada(self, id_conta, valor):
        # Protocolo para fazer a entrada de dinheiro em contas
        try:
            contaAlvo = self.get_conta_id(id_conta)
            contaAlvo.add_saldo(valor)
            print(f"conta: {contaAlvo.nome}  Saldo: {contaAlvo.saldo}")
            print("SOMOOOU")
            return True
        except:
            return False
    
    def cancelar(self, id_transacao):
        # Cancelar uma transação que não deu certo
        for transacao in self.transacoes:
            if transacao.id == id_transacao:
                for conta in transacao.contas_envolvidas:
                    conta_envolvida = self.get_conta_id(conta['id'])
                    if conta.operacao == "saida":
                        conta_envolvida.desfazer_sub(conta['valor'])
                    else:
                        conta_envolvida.desfazer_add(conta['valor'])