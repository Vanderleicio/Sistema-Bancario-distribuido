#!/bin/bash

# URL dos bancos
BANCO_DO_LARSID="http://127.0.0.1:5000/"
LARSIDESCO="http://127.0.0.1:5001/"
LARSIDBANK="http://127.0.0.1:5002/"

# Função para realizar um deposito
deposito() {
    local nomeBanco=$1
    local cpfs=$2
    local valor=$3
    local banco_url=$4


    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"banco\": \"$nomeBanco\", \"cpf\":$cpfs, \"valor\": \"$valor\"}" \
    "$banco_url/api/depositar")
    echo "Resposta do deposito: $RESPONSE"
}

saque(){
    local nomeBanco=$1
    local cpfs=$2
    local valor=$3
    local banco_url=$4


    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"banco\": \"$nomeBanco\", \"cpf\":$cpfs, \"valor\": \"$valor\"}" \
    "$banco_url/api/sacar")
    echo "Resposta do saque: $RESPONSE"
}

transferencia(){
    local banco_url=$1
    local origens=$2
    local destino=$3

    local json_data="{\"contas_origem\": $origens, \"conta_destino\": \"$destino\"}"

    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$json_data" "$banco_url/api/transferencia")
    echo "Resposta da transferencia: $RESPONSE"
}

saldos() {
    local banco_url=$1
    local cpfs=$2
    
    RESPONSE=$(curl -s "$banco_url/api/contas/geral?cpf=$cpfs")
    echo "Resposta do saldo: $RESPONSE"
}

echo "Fazendo depósitos simultâneos:"
deposito "Banco do LARSID" "[\"12345678901\"]" "50" $BANCO_DO_LARSID &
deposito "Banco do LARSID" "[\"12345678901\"]" "25" $BANCO_DO_LARSID &
deposito "LARSIDesco" "[\"12345678901\"]" "39" $LARSIDESCO &

#echo "Fazendo retiradas simultâneas:"
#saque "Banco do LARSID" "[\"12345678901\"]" "7" $BANCO_DO_LARSID &
#saque "Banco do LARSID" "[\"12345678901\"]" "16" $BANCO_DO_LARSID &
#saque "LARSIDesco" "[\"12345678901\"]" "10" $LARSIDESCO &

wait

echo "SALDOS PÓS DEPÓSITOS: "
saldos $BANCO_DO_LARSID "12345678901"

origens_var='[{"id": 1, "banco": "Banco do LARSID", "valor": "3"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]'
destino_var='{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}'


echo "Fazendo transferências simultâneas:"
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "3"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "3"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "2"}]' '{\"id\": 2, \"banco\": \"Banco do LARSID\", \"cpf\": [\"12345678901\", \"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "10"}, {"id": 1, "banco": "LARSIDesco", "valor": "3"}]' '{\"id\": 2, \"banco\": \"Banco do LARSID\", \"cpf\": [\"12345678901\", \"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "100"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "5"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "10"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "5"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "10"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &
transferencia $BANCO_DO_LARSID '[{"id": 1, "banco": "Banco do LARSID", "valor": "5"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]' '{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}' &

wait

echo "SALDOS PÓS TRANFERÊNCIAS: "
saldos $BANCO_DO_LARSID "12345678901"
saldos $BANCO_DO_LARSID "23456789012"
