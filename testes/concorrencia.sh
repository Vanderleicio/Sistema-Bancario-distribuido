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
deposito "Banco do LARSID" "[\"12345678901\"]" "3" $BANCO_DO_LARSID &
#deposito "Banco do LARSID" "[\"12345678901\"]" "5" $BANCO_DO_LARSID &
deposito "LARSIDesco" "[\"12345678901\"]" "5" $LARSIDESCO &

#echo "Fazendo retiradas simultâneas:"
#saque "Banco do LARSID" "[\"12345678901\"]" "7" $BANCO_DO_LARSID &
#saque "Banco do LARSID" "[\"12345678901\"]" "16" $BANCO_DO_LARSID &
#saque "LARSIDesco" "[\"12345678901\"]" "10" $LARSIDESCO &
saque "LARSIDBank" "[\"23456789012\"]" "8" $LARSIDBANK &

wait

echo "SALDOS PÓS DEPÓSITOS: "
saldos $BANCO_DO_LARSID "12345678901"

origem1='[{"id": 1, "banco": "Banco do LARSID", "valor": "3"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]'
origem2='[{"id": 1, "banco": "Banco do LARSID", "valor": "2"}]'
origem3='[{"id": 1, "banco": "Banco do LARSID", "valor": "10"}, {"id": 1, "banco": "LARSIDesco", "valor": "3"}]'
origem4='[{"id": 1, "banco": "Banco do LARSID", "valor": "100"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]'
origem5='[{"id": 1, "banco": "Banco do LARSID", "valor": "5"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]'
origem6='[{"id": 1, "banco": "Banco do LARSID", "valor": "10"}, {"id": 1, "banco": "LARSIDesco", "valor": "5"}]'
destino1='{\"id\": 1, \"banco\": \"LARSIDBank\", \"cpf\": [\"23456789012\"]}'
destino2='{\"id\": 2, \"banco\": \"Banco do LARSID\", \"cpf\": [\"12345678901\", \"23456789012\"]}'

echo "Fazendo transferências simultâneas:"
transferencia $BANCO_DO_LARSID "$origem1" "$destino1" & #Sai: U1B1: 3, U1B2: 5/ Entra: U2B3: 8
transferencia $BANCO_DO_LARSID "$origem1" "$destino1" & #Sai: U1B1: 3, U1B2: 5/ Entra: U2B3: 8
transferencia $BANCO_DO_LARSID "$origem2" "$destino2" & #Sai: U1B1: 2/ Entra: U3B1: 2
transferencia $BANCO_DO_LARSID "$origem3" "$destino2" & #Sai: U1B1: 10, U1B2: 3/ Entra: U3B1: 13
transferencia $BANCO_DO_LARSID "$origem4" "$destino1" & #Sai: U1B1: 100, U1B2: 5/ Entra: U2B3: 105 ERRO
transferencia $BANCO_DO_LARSID "$origem5" "$destino1" & #Sai: U1B1: 5, U1B2: 5/ Entra: U2B3: 10
transferencia $BANCO_DO_LARSID "$origem6" "$destino1" & #Sai: U1B1: 10, U1B2: 5/ Entra: U2B3: 15
transferencia $BANCO_DO_LARSID "$origem5" "$destino1" & #Sai: U1B1: 5, U1B2: 5/ Entra: U2B3: 10
transferencia $BANCO_DO_LARSID "$origem6" "$destino1" & #Sai: U1B1: 10, U1B2: 5/ Entra: U2B3: 15
transferencia $BANCO_DO_LARSID "$origem5" "$destino1" & #Sai: U1B1: 5, U1B2: 5/ Entra: U2B3: 10

wait

echo "SALDOS PÓS TRANFERÊNCIAS: "
saldos $BANCO_DO_LARSID "12345678901"
saldos $BANCO_DO_LARSID "23456789012"
