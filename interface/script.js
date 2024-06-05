document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var cpf = document.getElementById('cpf').value;
    var senha = document.getElementById('senha').value;
    var tipoConta = document.getElementById('tipoConta').value;

    // Adicione aqui a lógica para verificar os dados de login
    alert(`CPF: ${cpf}\nSenha: ${senha}\nTipo de Conta: ${tipoConta}`);
});
