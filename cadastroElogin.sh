#!/bin/bash

# URL da API para cadastro e login
SIGNUP_URL="http://127.0.0.1:5000/api/registrar"
LOGIN_URL="http://127.0.0.1:5000/api/login"

# Dados para o cadastro
SIGNUP_DATA='{"nome":"usuario_teste", "cpfs":"12345678901", "tipo": 1, "senha": "123" }'

# Dados para o login
LOGIN_DATA='{"cpf":"12345678901","tipo": 1, "senha": "123"}'

# Função para testar o cadastro
test_signup() {
  RESPONSE=$(curl -s -o signup_response.txt -w "%{http_code}" -X POST $SIGNUP_URL -H "Content-Type: application/json" -d "$SIGNUP_DATA")

  # Imprimir o código de resposta HTTP
  echo "Código de resposta HTTP do Cadastro: $RESPONSE"

  # Imprimir a resposta da API
  #echo "Resposta da API de Cadastro:"
  #cat signup_response.txt
}

# Função para testar o login
test_login() {
  RESPONSE=$(curl -s -o login_response.txt -w "%{http_code}" -X POST $LOGIN_URL -H "Content-Type: application/json" -d "$LOGIN_DATA")

  # Imprimir o código de resposta HTTP
  echo "Código de resposta HTTP do Login: $RESPONSE"

  # Imprimir a resposta da API
 # echo "Resposta da API de Login:"
  #cat login_response.txt
}

# Executar as funções
test_signup
test_login
