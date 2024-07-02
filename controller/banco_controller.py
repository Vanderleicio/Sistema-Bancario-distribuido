from flask import Blueprint, jsonify, request, render_template, current_app
from banco.servicos_banco import Banco
import requests
import sys

nomeBanco = str(sys.argv[1]) # Nome do Banco que será instanciado
banco_blueprint = Blueprint('banco', __name__, template_folder= '../interfaces')
banco = Banco(nomeBanco)
#consorcio = [{'nome': "Banco do LARSID", 'rota': 'http://127.0.0.1:5000'}, {'nome': 'LARSIDesco', 'rota': 'http://127.0.0.1:5001'}, {'nome': 'LARSIDBank', 'rota': 'http://127.0.0.1:5002'}] # Digitar aqui os outros bancos: {'nome': nome_do_banco, 'rota': rota_do_banco} Ex: {'nome': 'LARSIDesco', 'rota': 'http://127.0.0.2:5025'}
consorcio = {}
PORTA = 0
conta_atual = None
status_participantes = []

def inicializacao():
    global PORTA, consorcio
    bancos = {}
    with open('Consorcio.txt', 'r') as file:
        linhas = file.readlines()
        for linha in linhas:
            bank = linha.strip().split(":", 1)
            bancos[bank[0]] = bank[1]
    
    PORTA = (bancos[str(sys.argv[1])]).split(":")[2]
    consorcio = bancos


inicializacao()


@banco_blueprint.route('/')
def home():
    return render_template('index.html', nomeDoBanco=nomeBanco)

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
    if banco.login(cpf, senha):
        global conta_atual # Pode ser os dados da conta ou o cpf que está tentando logar.
        id_conta = banco.get_conta_cpf(cpf).id
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
    
    parametros = {'CPFs': cpf}
    for bancos in consorcio:
        if bancos != banco.nome:
            try:
                contas = requests.get(consorcio[bancos] + '/api/contas/cpf', params=parametros, timeout=3).json()
                if len(contas) > 0:
                    banco_conta = {'banco': bancos, 'contas': contas}
                    tdas_contas.append(banco_conta)
            except:
                continue
    return jsonify(tdas_contas)

@banco_blueprint.route('/api/contas/geral', methods=['GET'])
def get_tdas_contas_geral():
    cpf = request.args.getlist('cpf')
    # Garantir que a primeira conta da lista é a conta que está logada no momento
    tdas_contas = [{'banco': banco.nome, 'contas': [conta.to_dict() for conta in banco.get_contas_do_cpf(cpf[0])]}]

    #print("CPF DA CONTA " + cpf[0])
    parametros = {'CPFs': cpf[0]}
    for bancos in consorcio:
        if bancos != banco.nome:
            try:
                contas = requests.get(consorcio[bancos] + '/api/contas/cpf', params=parametros, timeout=3).json()
                if len(contas) > 0:
                    banco_conta = {'banco': bancos, 'contas': contas}
                    tdas_contas.append(banco_conta)
            except:
                continue
    return jsonify(tdas_contas)

@banco_blueprint.route('/api/depositar', methods=['POST'])
def deposito():
    dados = request.get_json()
    bancoNome = dados['banco']

    if bancoNome == nomeBanco:
        cpf = dados['cpf']
        valor = float(dados['valor'])
        conta = banco.get_conta_cpf(cpf)
        funcionou = banco.entrada(conta.id, valor)
        if (funcionou):
            print("Operação foi um sucesso!")
            return jsonify({'success': True})
        else:
            print("Operação falhou")
            return jsonify({'success': False})
    else:
        try:
            headers = {'Content-Type': 'application/json'}
            url = consorcio[bancoNome] + '/api/depositar'
            envio = {'banco': bancoNome, 'cpf': dados['cpf'], 'valor': dados['valor']}
            resposta = requests.post(url, json=envio, headers=headers, timeout=3).json()
            return resposta
        except:
            return jsonify({'success': False})
        
    

@banco_blueprint.route('/api/sacar', methods=['POST'])
def saque():
    dados = request.get_json()
    bancoNome = dados['banco']

    if bancoNome == nomeBanco:
        cpf = dados['cpf']
        valor = float(dados['valor'])
        conta = banco.get_conta_cpf(cpf)
        conta_envolvida = [{'id': conta.id, 'valor': valor}]
        sucesso_preparacao, id_transacao = banco.preparar_saida(conta_envolvida)
        if (sucesso_preparacao):
            banco.saida(id_transacao)
            print("Operação foi um sucesso!")
            return jsonify({'success': True})
        else:
            print("Operação falhou")
            return jsonify({'success': False})
    else:
        try:
            headers = {'Content-Type': 'application/json'}
            url = consorcio[bancoNome] + '/api/sacar'
            envio = {'banco': bancoNome, 'cpf': dados['cpf'], 'valor': dados['valor']}
            resposta = requests.post(url, json=envio, headers=headers, timeout=3).json()
            return resposta
        except:
            return jsonify({'success': False})
        

@banco_blueprint.route('/api/transferencia', methods=['POST'])
def transferencia():
    dados = request.get_json()
    contas_origem = dados['contas_origem']  # [{'banco': string, 'id': int, 'valor': float}]
    conta_destino = eval(dados['conta_destino']) # {'banco': string, 'id': int}
    bancosAlvos = {}
    total = 0
    for conta in contas_origem:
        if not bancosAlvos.get(conta['banco']):
            bancosAlvos[conta['banco']] = []
        total += float(conta['valor'])
        bancosAlvos[conta['banco']].append({'id': conta['id'], 'retirar': True, 'valor': float(conta['valor'])})
    
    if not bancosAlvos.get(conta_destino['banco']):
        bancosAlvos[conta_destino['banco']] = []

    bancosAlvos[conta_destino['banco']].append({'id': conta_destino['id'], 'retirar': False, 'valor': total})

    bancosComunicados = {} #{'nomeDoBanco':['idTran', contasAlvo]}
    for bancoAlvo, contasAlvo in bancosAlvos.items():
        # FAZER A LÓGICA PARA ADICIONAR OS OUTROS BANCOS
        try:
            headers = {'Content-Type': 'application/json'}
            envio = {'mensagem': 'preparar', 'contas': contasAlvo, 'id_tran': None}
            url = consorcio[bancoAlvo] + '/api/participante'
            resp = requests.post(url, json=envio, headers=headers, timeout=3)
            resp.raise_for_status()
            resposta = resp.json()
        except:
            resposta['sucesso'] = False

        if (resposta['sucesso']):
            bancosComunicados[bancoAlvo] = [resposta['transacao'], contasAlvo]

        else:
            for bancos in bancosComunicados:
                url = consorcio[bancos] + '/api/participante'
                envio = {'mensagem': 'cancelar', 'contas': bancosComunicados[bancos][1], 'id_tran': bancosComunicados[bancos][0]}
                requests.post(url, json=envio, headers=headers).raise_for_status()
            return jsonify({'sucesso': False})
    else:
        for bancos in bancosComunicados:
            url = consorcio[bancos] + '/api/participante'
            envio = {'mensagem': 'comitar', 'contas': bancosComunicados[bancos][1], 'id_tran': bancosComunicados[bancos][0]}
            resp = requests.post(url, json=envio, headers=headers)
            resp.raise_for_status()

    return jsonify({'sucesso': True})



@banco_blueprint.route('/api/participante', methods=['POST'])
def participante():
    dados = request.get_json()
    ordem = dados['mensagem'] # 'preparar', 'comitar' ou 'cancelar'
    contas_alvo = dados['contas'] # [{'id': int, 'retirar': bool, 'valor': float}]
    
    contas_p_retirar = []
    contas_p_depositar = []

    for conta in contas_alvo:
        if conta['retirar']:
            contas_p_retirar.append(conta)
        else:
            contas_p_depositar.append(conta)

    if ordem == 'preparar':
        sucesso, id_transacao = banco.preparar_saida(contas_p_retirar)
        print("Preparando")
        return jsonify({'sucesso': sucesso, 'transacao': id_transacao})
    
    elif ordem == 'comitar':
        print("Comitando")
        id_tran = dados['id_tran']
        sucesso = banco.saida(id_tran)
        for conta in contas_p_depositar:
            print(conta)
            banco.entrada(conta['id'], conta['valor'])

        return jsonify({'sucesso': sucesso})

    
    elif ordem == "cancelar":
        print("Cancelando")
        id_tran = dados['id_tran']
        sucesso = banco.cancelar(id_tran)
        return jsonify({'sucesso': sucesso})
    else:
        print("Nenhuma das opções possíveis foi selecionada.")

'''
[
    {'banco': nome_do_banco, 'contas': [{"nome": self.nome, "tipo": self.tipo, "cpf": self.cpf, "saldo": self.saldo}]},

]
'''