// Espera 5 segundos (5000 milisegundos), para luego ocultar el mensaje
setTimeout(function() {
    const message = document.getElementById('message');
    if (message) {
        message.style.display = 'none';
    }
}, 5000);