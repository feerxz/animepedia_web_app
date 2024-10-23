// Selecciona el campo de entrada y el contenedor principal de animes
const searchInput = document.querySelector('#search');
const animeContainer = document.querySelector('#animes-container');

// Añade un evento de input al campo de entrada
searchInput.addEventListener('input', function() {
    // Obtiene el texto de búsqueda del campo de entrada
    const searchText = this.value.toLowerCase();

    // Obtiene todos los artículos de animes del contenedor
    const animes = animeContainer.querySelectorAll('article');

    // Para cada anime en el contenedor...
    animes.forEach(anime => {
        // Obtiene el título del anime y lo convierte a minúsculas
        const animeTitle = anime.querySelector('h3').textContent.toLowerCase();

        // Si el título del anime incluye el texto de búsqueda...
        if (animeTitle.includes(searchText)) {
            // Muestra el anime
            anime.style.display = '';
        } else {
            // Oculta el anime
            anime.style.display = 'none';
        }
    });
});