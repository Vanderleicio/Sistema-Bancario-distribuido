from models.conta import Conta

# Nome: String, Cpf: String, Tipo: int
# Tipos: PF - P (1), PF - C (2), PJ (3)

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = []
    
    def add_conta(self, nome, cpf, tipo, senha):
        for conta in self.contas:
            print(cpf)
            print(conta.cpf)
            if cpf == conta.cpf:
                print("VOCÊ JÁ TEM UMA CONTA DESSE TIPO")
                raise RuntimeError("Conta já existente")

        nova_conta = Conta(nome, cpf, tipo, senha)
        self.contas.append(nova_conta)
    
    def get_contas_cpf(self, n_cpf):
        contas = []
        for conta in self.contas:
            print(n_cpf)
            print(conta.cpf)
            if n_cpf in conta.cpf:
                contas.append(conta)
        
        return contas
    
    def get_conta_cpf_tipo(self, n_cpf, tipo):
        for conta in self.contas:
            if n_cpf in conta.cpf and tipo == conta.tipo:
                return conta
    
    def login(self, cpf, tipo, senha):
        return self.get_conta_cpf_tipo(cpf, tipo).senha == senha
