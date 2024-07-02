import threading

# Tipos: PF - P (1), PF - C (2), PJ (3)

class Conta:
    def __init__(self, id, nome, cpf, tipo, senha):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.senha = senha
        self.saldos = []
        self.cpf = cpf
        self.saldo = 0
        self.lock = threading.Lock()
    
    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "tipo": self.tipo, "cpf": self.cpf, "saldo": self.saldo}
    
    def add_saldo(self, valor):
        try:
            # Seção crítica
            self.travar_saldo()
            self.saldo += valor
            self.liberar_saldo()
            print(f"Somando {valor} no saldo")
        except Exception as e:
            print(str(e))

    def sub_saldo(self, valor):
        try:
            self.travar_saldo()
            # Seção crítica
            if self.saldo < valor:
                self.liberar_saldo()
                raise RuntimeError("Saldo insuficiente ")
            else:
                self.saldo -= valor
            self.liberar_saldo()
            print(f"Subtraindo {valor} no saldo")
        except RuntimeError:
            raise RuntimeError("Saldo insuficiente ")
        except Exception as e:
            print(str(e))
    
    def desfazer_add(self, valor):
        # RECONSIDERAR !!!
        self.lock.acquire()
        
        try:
            self.saldo -= valor
            print(f"Desfazendo o acréscimo de {valor}")
        finally:
            self.lock.release()
    
    def desfazer_sub(self, valor):
        # RECONSIDERAR !!!
        self.lock.acquire()
        
        try:
            self.saldo += valor
            print(f"Desfazendo a subtração de {valor}")
        finally:
            self.lock.release()

    def travar_saldo(self):
        adquirido = self.lock.acquire(blocking=False)
        if not adquirido:
            raise RuntimeError("Movimentação sendo feita. Aguarde...")
    
    def liberar_saldo(self):
        self.lock.release()