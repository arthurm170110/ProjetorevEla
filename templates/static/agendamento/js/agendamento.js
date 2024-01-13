
var dataInput = document.getElementById('data');
var amanha = new Date();
amanha.setDate(amanha.getDate() + 1); // Adiciona um dia
var dataFormatada = amanha.toISOString().split('T')[0];
dataInput.setAttribute('min', dataFormatada);
dataInput.setAttribute('min', hoje);