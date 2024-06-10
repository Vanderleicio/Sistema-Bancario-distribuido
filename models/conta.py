import threading

# Tipos: PF - P (1), PF - C (2), PJ (3)

class Conta:
    def __init__(self, nome, cpf, tipo, senha):
        self.nome = nome
        self.tipo = tipo
        self.senha = senha
        self.saldos = []

        if (self.tipo == 2):
            # Contas conjuntas têm 2 cpfs associados
            self.cpf = cpf
        else:
            self.cpf = cpf
        
        self.saldo = 0
        self.lock = threading.Lock()
    
    def to_dict(self):
        return {"nome": self.nome, "tipo": self.tipo, "cpf": self.cpf, "saldo": self.saldo}
    
    def add_saldo(self, valor):
        adquirido = self.lock.acquire(blocking=False)
        if not adquirido:
            raise RuntimeError("Movimentação sendo feita. Aguarde...")

        try:
            # Seção crítica
            self.saldo += valor
            print(f"Somando {valor} no saldo")
        finally:
            self.lock.release()
    
    def sub_saldo(self, valor):
        adquirido = self.lock.acquire(blocking=False)
        if not adquirido:
            raise RuntimeError("Movimentação sendo feita. Aguarde...")

        try:
            # Seção crítica
            if self.saldo < valor:
                raise RuntimeError("Saldo insuficiente ")
            else:
                self.saldo -= valor
            print(f"Subtraindo {valor} no saldo")
        finally:
            self.lock.release()
    
    def desfazer_add(self, valor):
        self.lock.acquire()
        
        try:
            self.saldo -= valor
            print(f"Desfazendo o acréscimo de {valor}")
        finally:
            self.lock.release()
    
    def desfazer_sub(self, valor):
        self.lock.acquire()
        
        try:
            self.saldo += valor
            print(f"Desfazendo a subtração de {valor}")
        finally:
            self.lock.release()