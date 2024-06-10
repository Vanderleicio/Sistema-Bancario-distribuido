from flask import Blueprint, jsonify, request, render_template
from banco.servicos_banco import Banco
import requests

banco_blueprint = Blueprint('banco', __name__, template_folder= '../interface')
banco = Banco("Banco do LARSID")
consorcio = [{'nome': 'LARSIDesco', 'rota': 'http://127.0.0.1:5002'}] # Digitar aqui os outros bancos: {'nome': nome_do_banco, 'rota': rota_do_banco} Ex: {'nome': 'LARSIDesco', 'rota': 'http://127.0.0.2:5025'}
conta_atual = None

@banco_blueprint.route('/')
def home():
    return render_template('index.html')

@banco_blueprint.route('/cadastrar')
def login():
    return render_template('cadastro.html')

@banco_blueprint.route('/inicio')
def inicio():
    print(conta_atual)
    if conta_atual:
        print("Teste")
        usuario = banco.get_conta_cpf_tipo(conta_atual['cpf'], conta_atual['tipo']).to_dict()
        return render_template('logado.html', user=usuario)

@banco_blueprint.route('/api/registrar', methods=['POST'])
def registrar():
    dados = request.get_json()
    nome = dados['nome']
    cpf = dados['cpfs']
    tipo = dados['tipo']
    senha = dados['senha']
    banco.add_conta(nome, cpf, tipo, senha)
    return jsonify({'message': f'Conta registrada com sucesso para {nome}!', 'success': True})

@banco_blueprint.route('/api/login', methods=['POST'])
def auth_login():
    dados = request.get_json()
    cpf = dados['cpf']
    tipo = dados['tipo']
    senha = dados['senha']
    print("Teste")
    if banco.login(cpf, tipo, senha):
        global conta_atual
        conta_atual = {'cpf': cpf, 'tipo': tipo}
        return jsonify({'success': True})
    
    return jsonify({'success': False})

@banco_blueprint.route('/api/contas/cpf', methods=['GET'])
def get_contas_do_cpf():
    cpfs = request.args.getlist('CPFs')
    contas = banco.get_contas_cpf(cpfs[0])
    return jsonify([conta.to_dict() for conta in contas]), "200"

@banco_blueprint.route('/api/contas/cpfetipo', methods=['GET'])
def get_conta():
    cpfs = request.args.getlist('CPFs')
    tipo = request.args.getlist('tipo')
    conta = banco.get_conta_cpf_tipo(cpfs[0], tipo[0])
    return jsonify(conta.to_dict()), "200"

@banco_blueprint.route('/api/contas/todas', methods=['GET'])
def get_tdas_contas():
    cpf = conta_atual['cpf']
    tdas_contas = [{'banco': banco.nome, 'contas': [conta.to_dict() for conta in banco.get_contas_cpf(cpf)]}]
    parametros = {'CPFs': cpf}
    for bancos in consorcio:
        contas = requests.get(bancos['rota'] + '/api/contas/cpf', params=parametros).json()
        if len(contas) > 0:
            banco_conta = {'banco': bancos['nome'], 'contas': contas}
            tdas_contas.append(banco_conta)
        
    return jsonify(tdas_contas)

'''
[
    {'banco': nome_do_banco, 'contas': [{"nome": self.nome, "tipo": self.tipo, "cpf": self.cpf, "saldo": self.saldo}]},

]
'''