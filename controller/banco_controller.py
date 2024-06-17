from flask import Blueprint, jsonify, request, render_template
from banco.servicos_banco import Banco
import requests

banco_blueprint = Blueprint('banco', __name__, template_folder= '../interfaces')
banco = Banco("Banco do LARSID")
#consorcio = [{'nome': 'LARSIDesco', 'rota': 'http://127.0.0.1:5002'}] # Digitar aqui os outros bancos: {'nome': nome_do_banco, 'rota': rota_do_banco} Ex: {'nome': 'LARSIDesco', 'rota': 'http://127.0.0.2:5025'}
consorcio = []
conta_atual = None

@banco_blueprint.route('/')
def home():
    return render_template('index.html')

@banco_blueprint.route('/cadastrar')
def login():
    return render_template('cadastro.html')

@banco_blueprint.route('/selContas')
def contas():
    return render_template('interLogin.html', usercpf=conta_atual)

@banco_blueprint.route('/inicio')
def inicio():
    global conta_atual
    if conta_atual:
        usuario = banco.get_conta_id(conta_atual["id"]).to_dict()
        return render_template('logado.html', user=usuario)

@banco_blueprint.route('/checarcpf', methods=['POST'])
def cpf_cadastrado():
    global conta_atual
    cpf = request.get_json()['cpf']
    contas = banco.get_contas_do_cpf(cpf)
    if (len(contas)):
        conta_atual = cpf
        return jsonify({'success': True})

    return jsonify({'success': False})

@banco_blueprint.route('/api/registrar', methods=['POST'])
def registrar():
    dados = request.get_json()
    nome = dados['nome']
    cpf = dados['cpfs']
    tipo = dados['tipo']
    senha = dados['senha']
    banco.add_conta(nome, cpf, tipo, senha)
    return jsonify({'message': f'Conta registrada com sucesso!', 'success': True})

@banco_blueprint.route('/api/login', methods=['POST'])
def auth_login():
    dados = request.get_json()
    cpf = dados['cpf']
    senha = dados['senha']
    print(cpf)
    if banco.login(cpf, senha):
        global conta_atual # Pode ser os dados da conta ou o cpf que está tentando logar.
        id_conta = banco.get_conta_cpf(cpf).id
        print(id_conta)
        conta_atual = {"id": id_conta, "cpf": cpf, "cpf_logado": conta_atual}
        return jsonify({'success': True})
    
    return jsonify({'success': False})

@banco_blueprint.route('/api/contas/cpf', methods=['GET'])
def get_contas_do_cpf():
    cpfs = request.args.getlist('CPFs')
    contas = banco.get_contas_do_cpf(cpfs[0])
    return jsonify([conta.to_dict() for conta in contas]), "200"

@banco_blueprint.route('/api/contas/cpfetipo', methods=['GET'])
def get_conta():
    cpfs = request.args.getlist('CPFs')
    tipo = request.args.getlist('tipo')
    conta = banco.get_conta_cpf_tipo(cpfs[0], tipo[0])
    return jsonify(conta.to_dict()), "200"

@banco_blueprint.route('/api/contas/todas', methods=['GET'])
def get_tdas_contas():
    cpf = conta_atual["cpf_logado"]

    # Garantir que a primeira conta da lista é a conta que está logada no momento
    tdas_contas = [{'banco': banco.nome, 'contas': [banco.get_conta_id(conta_atual['id']).to_dict()]}]

    for conta in banco.get_contas_do_cpf(cpf):
        if conta.cpf != tdas_contas[0]['contas'][0]['cpf']:
            # Conta a ser adicionada não é a que já está
            tdas_contas[0]['contas'].append(conta.to_dict())
    
    #print("CPF DA CONTA " + cpf[0])
    parametros = {'CPFs': cpf[0]}
    for bancos in consorcio:
        contas = requests.get(bancos['rota'] + '/api/contas/cpf', params=parametros).json()
        if len(contas) > 0:
            banco_conta = {'banco': bancos['nome'], 'contas': contas}
            tdas_contas.append(banco_conta)
    print(tdas_contas)
    return jsonify(tdas_contas)

@banco_blueprint.route('/api/contas/geral', methods=['GET'])
def get_tdas_contas_geral():
    cpf = request.args.getlist('cpf')

    # Garantir que a primeira conta da lista é a conta que está logada no momento
    tdas_contas = [{'banco': banco.nome, 'contas': [conta.to_dict() for conta in banco.get_contas_do_cpf(cpf[0])]}]

    #print("CPF DA CONTA " + cpf[0])
    parametros = {'CPFs': cpf[0]}
    for bancos in consorcio:
        contas = requests.get(bancos['rota'] + '/api/contas/cpf', params=parametros).json()
        if len(contas) > 0:
            banco_conta = {'banco': bancos['nome'], 'contas': contas}
            tdas_contas.append(banco_conta)
    print(tdas_contas)
    return jsonify(tdas_contas)

@banco_blueprint.route('/api/depositar', methods=['POST'])
def deposito():
    dados = request.get_json()
    cpf = eval(dados['cpf'])
    valor = float(dados['valor'])
    conta = banco.get_conta_cpf(cpf)
    funcionou = banco.entrada(conta.id, valor)
    if (funcionou):
        print("Operação foi um sucesso!")
    else:
        print("Operação falhou")
    
    return jsonify({'success': True})
    

@banco_blueprint.route('/api/sacar', methods=['POST'])
def saque():
    dados = request.get_json()
    cpf = eval(dados['cpf'])
    valor = float(dados['valor'])
    conta = banco.get_conta_cpf(cpf)
    if (banco.saida(conta.id, valor)):
        print("Operação foi um sucesso!")
        return jsonify({'success': True})
    else:
        print("Operação falhou")
        return jsonify({'success': False})
        

@banco_blueprint.route('/api/transferencia', methods=['POST'])
def transferencia():
    contas_origem = request.args.getlist('origens')  # [{'banco': string, 'id': int, 'valor': float}]
    contas_destino = request.args.getlist('destino') # {'banco': string, 'id': int} 
    # IMPLEMENTAR A LÓGICA DE COORDENADOR



@banco_blueprint.route()
def participante():
    # IMPLEMENTAR A LÓGICA DE PARTICIPANTE
    pass

'''
[
    {'banco': nome_do_banco, 'contas': [{"nome": self.nome, "tipo": self.tipo, "cpf": self.cpf, "saldo": self.saldo}]},

]
'''