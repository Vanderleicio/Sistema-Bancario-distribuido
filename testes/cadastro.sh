#!/bin/bash

# URL dos bancos
BANCO_DO_LARSID="http://127.0.0.1:5000/"
LARSIDESCO="http://127.0.0.1:5001/"
LARSIDBANK="http://127.0.0.1:5002/"

# Usuarios
USER1B1='{"nome":["usuario1"], "cpfs":["12345678901"], "tipo": 1, "senha": "123" }'
USER3B1='{"nome":["usuario1", "usuario2"], "cpfs":["12345678901", "23456789012"], "tipo": 2, "senha": "123" }'
USER1B2='{"nome":["usuario1"], "cpfs":["12345678901"], "tipo": 1, "senha": "123" }'
USER2B3='{"nome":["usuario2"], "cpfs":["23456789012"], "tipo": 1, "senha": "123" }'


# Função para testar o cadastro
cadastros() {
  ROTA_CADASTRO="api/registrar"
  URL_CADASTRO=$BANCO_DO_LARSID$ROTA_CADASTRO
  RESPONSE=$(curl -s -X POST $URL_CADASTRO -H "Content-Type: application/json" -d "$USER1B1")
  echo "Cadastro U1B1: $RESPONSE"
  RESPONSE=$(curl -s -X POST $URL_CADASTRO -H "Content-Type: application/json" -d "$USER3B1")
  echo "Cadastro U3B1: $RESPONSE"
  
  URL_CADASTRO=$LARSIDESCO$ROTA_CADASTRO
  RESPONSE=$(curl -s -X POST $URL_CADASTRO -H "Content-Type: application/json" -d "$USER1B2")
  echo "Cadastro U1B2: $RESPONSE"

  URL_CADASTRO=$LARSIDBANK$ROTA_CADASTRO
  RESPONSE=$(curl -s -X POST $URL_CADASTRO -H "Content-Type: application/json" -d "$USER2B3")
  echo "Cadastro U2B3: $RESPONSE"
}

echo "Testando"
cadastros
