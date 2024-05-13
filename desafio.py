from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf=cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo =0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = self.valor > saldo
        
        if excedeu_saldo:
            print("Saldo insuficiente!")
            return False
        elif valor> 0:
            self._saldo -=valor
            print("Saque realizado com sucesso")
            return True
        else:
            print("Operacao inválida")
            
        return False
            
    def depositar(self, valor):
        if valor > 0:
            saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite= 500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"]== Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques
        
        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
        
        
class Historico:
    def __init__(self):
        self._transacoes =[]
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
        })

class Transacao(ABC):
    
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    
    def __init__(self, valor) -> None:
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    return """

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo usuario
        [nc] Nova conta
        [lc] Listar contas
        [q] Sair

        Escolha uma Opcao: """

def recupera_conta_cliente(clientes):
    cpf = input("Informe o cpf do cliente")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente nao encontrado")
        return 
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    return conta, cliente

def depositar(clientes):
    
    conta, cliente = recuperar_conta_cliente(clientes)
    if not conta or not cliente:
        return
    
    valor = float(input("Informe o valor a depositar: "))
    transacao = Deposito(valor)
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    conta, cliente = recuperar_conta_cliente(clientes)
    if not conta or not cliente:
        return
    
    valor = float(input("Informe o valor para saque: "))
    transacao = Saque(valor)
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    conta, cliente = recuperar_conta_cliente(clientes)
    if not conta or not cliente:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    
    extrato = ""

    if not transacoes:
        extrato = "Nao foram realizadas movimentacoes"
    else:
        for transacao in transacoes:
            extrato +=f"\n{transacao['tipo']}: \n\t R$ {transacao['valor']:.2f}"

    
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")
    
def criar_cliente(clientes):
    cpf = input("Informe o CPF")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("Ja existe um cliente com este CPF")
        return
    
    nome = input("Informe o nome:")
    data_nascimento = input("Informe a data de nascimento")
    endereco = input("Informe o endereco")
    cliente = PessoaFisica(nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    cliente.append(cliente)
    print("Cliente criado com sucesso!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados= [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o cpf do cliente")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        conta = ContaCorrente.nova_conta(cliente= cliente, numero= numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
        print("Conta criada com sucesso")
        return 
    print("Usuario nao encontrado")
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(linha)
 
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente nao possui conta")
        return
    
    return cliente.contas[0]
        
def main():
    
    clientes = []
    contas = []
    
    while True:

        opcao = input(menu())

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)
            
        elif opcao == "nu":
            criar_cliente(clientes)
            
        elif opcao == "nc":
            numero_conta = len(contas) +1
            criar_conta(numero_conta, clientes, contas)
                
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            
main()