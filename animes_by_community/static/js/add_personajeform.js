
document.querySelector('form').addEventListener('click', function(e) {
    if (e.target.matches('.add-personaje')) {
        e.preventDefault();

        var fieldset = e.target.closest('fieldset');
        var newFieldset = fieldset.cloneNode(true);

        var personajeCount = document.querySelector('input[name="personaje_count"]');
        if (!personajeCount) {
            personajeCount = document.createElement('input');
            personajeCount.type = 'hidden';
            personajeCount.name = 'personaje_count';
            personajeCount.value = 0;
            document.querySelector('form').appendChild(personajeCount);
        }
        personajeCount.value = parseInt(personajeCount.value) + 1;

        // Limpia los campos del formulario en el nuevo fieldset y genera nuevos id
        var inputs = newFieldset.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].value = '';
            var newId = inputs[i].id + '_' + Date.now();
            inputs[i].id = newId;

            // Actualiza el atributo for de la etiqueta label correspondiente
            var label = newFieldset.querySelector('label[for="' + inputs[i].id + '"]');
            if (label) {
                label.setAttribute('for', newId);
            }
        }
        // Elimina el botón "Descartar" del fieldset clonado
        var oldDeleteButton = newFieldset.querySelector('.delete-personaje');
        if (oldDeleteButton) oldDeleteButton.parentNode.removeChild(oldDeleteButton);

        // Oculta el botón "Añadir Personaje" y "Eliminar" en el fieldset anterior
        var addButton = fieldset.querySelector('.add-personaje');
        var deleteButton = fieldset.querySelector('.delete-personaje');
        if (addButton) addButton.style.display = 'none';
        if (deleteButton) deleteButton.style.display = 'none';

        
        // Añade el nuevo fieldset al formulario
        fieldset.parentNode.insertBefore(newFieldset, fieldset.nextSibling);

        var formElements = fieldset.querySelectorAll('input, select, textarea, label');
        for (var i = 0; i < formElements.length; i++) {
            formElements[i].style.display = 'none';
        }

        var expandArrow = document.createElement('span');
        expandArrow.textContent = '▼';
        expandArrow.style.cursor = 'pointer';
        expandArrow.addEventListener('click', function() {
            for (var i = 0; i < formElements.length; i++) {
                formElements[i].style.display = formElements[i].style.display === 'none' ? '' : 'none';
            }
        });
        fieldset.insertBefore(expandArrow, fieldset.firstChild);
        
        

        // Agrega el botón "Eliminar" al nuevo fieldset
        var newDeleteButton = document.createElement('button');
        newDeleteButton.textContent = 'Descartar';
        newDeleteButton.className = 'btn btn-danger delete-personaje';
        newDeleteButton.addEventListener('click', function(e) {
            e.preventDefault();
            newFieldset.parentNode.removeChild(newFieldset);
            // Muestra el botón "Añadir Personaje" en el fieldset anterior cuando se elimina el nuevo fieldset
            if (addButton) addButton.style.display = '';
            if (deleteButton) deleteButton.style.display = '';

            // Decrementa el conteo de personajes
            var personajeCount = document.querySelector('input[name="personaje_count"]');
            if (personajeCount) {
                personajeCount.value = parseInt(personajeCount.value) - 1;
            }
        });
        newFieldset.querySelector('.add-personaje').after(newDeleteButton);
    }
});

