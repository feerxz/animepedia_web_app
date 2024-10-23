
document.addEventListener('DOMContentLoaded', (event) => {
    let buttons = document.querySelectorAll('.read-more');

    // Itera sobre cada botón
    buttons.forEach((button) => {
        // Agrega un controlador de eventos 'click' a cada botón
        button.addEventListener('click', function() {
            // Encuentra el elemento de descripción corta y larga relacionado con este botón
            let shortDescription = this.parentNode.querySelector('.short-description');
            let fullDescription = this.parentNode.querySelector('.full-description');

            // Comprueba si la descripción completa está oculta
            if (fullDescription.classList.contains('hidden')) {
                // Si está oculta, muéstrala y oculta la descripción corta
                fullDescription.classList.remove('hidden');
                shortDescription.classList.add('hidden');
                this.textContent = 'Leer menos';
            } else {
                // Si no está oculta, ocúltala y muestra la descripción corta
                fullDescription.classList.add('hidden');
                shortDescription.classList.remove('hidden');
                this.textContent = 'Leer más';
            }
        });
    });
});
