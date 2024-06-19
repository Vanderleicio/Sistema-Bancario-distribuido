class Transacao:

    def __init__(self, id, contas_envolvidas):
        self.id = id
        self.contas_envolvidas = contas_envolvidas # Contas envolvidas nessa transacao: [{id, operacao, valor}, ...]
        self.saldos_reservados = [] # Saldos reservados de cada uma das contas
        self.preparada = False
        self.concluida = False
        self.sucesso = False
    
    def preparar(self, saldos_reservados):
        self.saldos_reservados = saldos_reservados
        self.preparada = True