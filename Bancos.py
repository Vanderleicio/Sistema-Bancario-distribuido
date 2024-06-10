'''

conta = {'tipo': int [1 (PF-P),2 (PF-C),3 (PJ)], 'nome': string, 'cpf': [string, string], 'saldo': float, 'lock': bool}

formto de envio = {'cpf'= string, 'contas' = [dict, dict, ...]}
'''

class Banco:
    # Através do IP do banco é que ele receberá e enviará transações
    def __init__(self, nome, ip):
        self.nome = nome
        self.ip = ip
        self.contas = []
    
    def criar_conta(self, cpf, tipo, ):
        pass

    def get_saldo(self, cpf, ip_origem):
        # Enviar para o ip_origem o saldo do cliente cpf
        envio = {'cpf': cpf, 'contas': []}
        for conta in self.contas:
            if cpf in conta['cpf']:
                infos = {'tipo': conta['tipo'], 'saldo': conta['saldo']}
                envio['contas'].append(infos)
                print("Achei sua conta")

    def listar_saldos(self, cpf):
        # Enviar para todos os bancos uma solicitacao get_saldo()
        pass

    def enviar_transferência(self, valor, cpf, ip_destino):
        # Realizar o protocolo de emissão de uma transferência
        pass

    def receber_transferência(self, valor, cpf, ip_origem):
        # Realizar o protocolo de emissão de uma transferência
        pass

    def fazer_pagamento(self, valor, cpf):
        # Debitar valor na codigo_conta do cliente cpf
        pass
    
    def fazer_depositivo(self, valor, cpf, codigo_conta):
        # Depositar valor na codigo_conta do cliente cpf
        pass