from models.conta import Conta

# Nome: String, Cpf: String, Tipo: int
# Tipos: PF - P (1), PF - C (2), PJ (3)

class Banco:

    def __init__(self, nome):
        self.ULTIMO_ID = 1
        self.nome = nome
        self.contas = []
    
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
    
    def saida(self, id_conta, valor):
        # Protocolo para fazer a retirada de dinheiro de uma conta
        try:
            contaAlvo = self.get_conta_id(id_conta)
            contaAlvo.sub_saldo(valor)
            return True
        except:
            return False
    
    def entrada(self, id_conta, valor):
        # Protocolo para fazer a entrada de dinheiro em uma conta
        try:
            contaAlvo = self.get_conta_id(id_conta)
            contaAlvo.add_saldo(valor)
            return True
        except:
            return False
