var isEditing = false;
var cancelButton = document.getElementById('cancelButton');
cancelButton.addEventListener('click', function(event) {
    event.preventDefault();
    location.reload();
});

document.getElementById('editButton').addEventListener('click', function(event) {
    var editButton = this; // Guardamos una referencia a 'this'
    cancelButton.style.display = 'inline-block';
    
    if (isEditing) {
        var username = document.getElementById('username');
        var email = document.getElementById('email');
        var first_name = document.getElementById('first_name');
        var last_name = document.getElementById('last_name');
        
        if (username.value && email.value && first_name.value && last_name.value) {
            Swal.fire({
                title: '¿Estás seguro?',
                text: "¿Quieres guardar los cambios?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, guardar!',
                cancelButtonText: 'No, cancelar!'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Si el usuario hace clic en "OK", cambiamos el tipo de botón a 'submit' para enviar el formulario
                    editButton.type = 'submit';
                    editButton.click(); // Hacemos clic en el botón para enviar el formulario
                } else {
                    // Si el usuario hace clic en "Cancelar", evitamos que se envíe el formulario
                    event.preventDefault();
                }
            });

        } else {
            // Si alguno de los campos está vacío, mostramos un mensaje de error
            Swal.fire({
                icon: 'warning',
                title: 'Por favor, llena todos los campos requeridos',
                confirmButtonText: 'OK'
            });
        }
    } else {
        // Si no estamos en modo de edición, habilitamos los campos y cambiamos el texto del botón
        document.getElementById('username').readOnly = false;
        document.getElementById('username').required = true;
        document.getElementById('email').readOnly = false;
        document.getElementById('email').required = true;
        document.getElementById('first_name').readOnly = false;
        document.getElementById('first_name').required = true;
        document.getElementById('last_name').readOnly = false;
        document.getElementById('last_name').required = true;
        
        this.textContent = 'Guardar';
        // Evitamos que se envíe el formulario
        event.preventDefault();
        // Cambiamos a modo de edición
        isEditing = true;
    }
});