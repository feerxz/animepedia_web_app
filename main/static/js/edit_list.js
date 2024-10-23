// Lista de animes que ya están en la lista del usuario
var animesEnLista = [];

// Selecciona todos los elementos que contienen los nombres de los animes en la lista del usuario
var animesSeleccionados = document.querySelectorAll('.car');

// Agrega los nombres de los animes al array
for (var i = 0; i < animesSeleccionados.length; i++) {
    animesEnLista.push(animesSeleccionados[i].textContent.trim());
}
// Crea un campo oculto para cada anime que ya está en la lista del usuario
for (let i = 0; i < animesEnLista.length; i++) {
    // Crea un nuevo campo oculto
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'selected-animes';
    hiddenInput.value = animesEnLista[i];

    // Añade el nuevo campo oculto al formulario
    document.querySelector('form').appendChild(hiddenInput);
}

document.getElementById('update-animes').addEventListener('click', function(event) {
    
    document.querySelector('.row.mt-4.d-none').classList.remove('d-none');
    
    document.getElementById('title').style.display = "block";

    // Obtén todos los animes
    var animes = document.querySelectorAll('.anime');
    // Itera sobre todos los animes
    for (var i = 0; i < animes.length; i++) {
        // Crea un nuevo botón
        var btn = document.createElement("button");
        btn.className = "btn ml-2"; // Agrega la clase "btn" de Bootstrap y "ml-2" para un margen a la izquierda
        
        // Si el anime está en la lista del usuario, el botón debe decir "Quitar de la lista"
        if (animesEnLista.includes(animes[i].textContent)) {
            btn.textContent = "Quitar de la lista";
            btn.className += " btn-danger"; // Agrega la clase "btn-danger" de Bootstrap
        } else {
            // Si el anime no está en la lista del usuario, el botón debe decir "Agregar a la lista"
            btn.textContent = "Agregar a la lista";
            btn.className += " btn-success"; // Agrega la clase "btn-success" de Bootstrap
        }

        // Agrega el botón al final del div con la clase 'card-body'
        animes[i].closest('.card-body').appendChild(btn);
        // Agrega un evento de clic al botón
        btn.addEventListener('click', (function(i) {
            return function() {
                // Si el botón dice "Agregar a la lista", agrega el anime a la lista y cambia el texto del botón
                if (this.textContent === "Agregar a la lista") {
                    this.textContent = "Quitar de la lista";
                    this.className = "btn ml-2 btn-danger";
                    animesEnLista.push(animes[i].textContent);
                    console.log(animesEnLista);
                    // Crea un nuevo div con la clase 'card'
                    const card = document.createElement('div');
                    card.className = 'card';

                    // Crea un nuevo div con la clase 'card-body car'
                    const cardBody = document.createElement('div');
                    cardBody.className = 'card-body car';
                    cardBody.textContent = animes[i].textContent;

                    // Añade el div 'card-body car' al div 'card'
                    card.appendChild(cardBody);

                    // Crea un nuevo div con la clase 'col-2'
                    const col = document.createElement('div');
                    col.className = 'col-2';

                    // Añade el div 'card' al div 'col-2'
                    col.appendChild(card);

                    // Añade el nuevo div 'col-2' a la sección de animes seleccionados
                    document.querySelector('.row').appendChild(col);

                    // Crea un nuevo campo oculto
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'selected-animes';
                    hiddenInput.value = animes[i].textContent;

                    // Añade el nuevo campo oculto al formulario
                    document.querySelector('form').appendChild(hiddenInput);

                } else {
                    // Si el botón dice "Quitar de la lista", quita el anime de la lista y cambia el texto del botón
                    this.textContent = "Agregar a la lista";
                    this.className = "btn ml-2 btn-success";
                    var index = animesEnLista.indexOf(animes[i].textContent);
                    if (index > -1) {
                        animesEnLista.splice(index, 1);
                    }

                    // Encuentra el div correspondiente y lo elimina
                    const divs = document.querySelectorAll('.row .col-2');
                    divs.forEach(div => {
                        if (div.textContent.trim() === animes[i].textContent) {
                            div.remove();
                        }
                    });

                    // Encuentra el campo oculto correspondiente y lo elimina
                    const hiddenInput = document.querySelector(`input[name="selected-animes"][value="${animes[i].textContent}"]`);
                    if (hiddenInput) {
                        hiddenInput.remove();
                    }
                }
                
                // Actualiza la cantidad de animes seleccionados
                document.getElementById('cantidad_animes').value = animesEnLista.length;
            };
        })(i));
    }
    document.getElementById('saveButton').addEventListener('click', function(event) {
        if (animesEnLista.length === 0) {
            alert('Debe seleccionar al menos un anime');
            event.preventDefault();
        } else if (animesEnLista.length > 50) {
            alert('No puedes seleccionar más de 50 animes');
            event.preventDefault();
        }
    });  
});
document.getElementById('cancelButton').addEventListener('click', function(event) {
    event.preventDefault();
    location.reload();
});