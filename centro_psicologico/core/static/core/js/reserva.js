let reservasFinal = [];

const CLAVE_RESERVAFINAL = "datos_reserva_final";

async function verificar() {
    const url = 'https://api.boostr.cl/holidays.json';
    const datePicker = document.getElementById('fecha');

    if (datePicker.reportValidity() && datePicker.value) {
        try {
            const solicitud = await fetch(url);
            const datosFeriados = await solicitud.json();
            const feriados = datosFeriados.data;

            const horaSeleccionada = document.querySelector('.hora-btn.selected');
            let esFeriado = undefined;
            const fechaSeleccionada = datePicker.value;
            const fechaSeleccionadaDate = new Date(fechaSeleccionada);

            const esDomingo = fechaSeleccionadaDate.getUTCDay() === 0;

            for (const fecha of feriados) {
                if (fecha.date === fechaSeleccionada) {
                    esFeriado = fecha;
                    break;
                }
            }

            if (!horaSeleccionada) {
                mostrarMensaje('Por favor, seleccione una hora para agendar la cita.');
            } else if (esDomingo) {
                mostrarMensaje('No puede elegir esta fecha ya que es domingo.');
            } else if (esFeriado) {
                mostrarMensaje('No puede elegir esta fecha ya que es feriado: ' + esFeriado.title);
            } else {
                let nombre = document.getElementById('nombreReserva').value.trim();
                let apellido = document.getElementById('apellidoReserva').value.trim();
                let telefono = parseInt(document.getElementById('telefono2').value.trim());
                let tipo = document.getElementById('tipo').value.trim();
                let tipo2 = document.getElementById('tipo2').value.trim();

                let reservaFinal = {
                    nombre: nombre,
                    apellido: apellido,
                    telefono: telefono,
                    tipo: tipo,
                    tipo2: tipo2,
                    fecha: fechaSeleccionada,
                    hora: horaSeleccionada.innerText
                };

                const reservasGuardadas = JSON.parse(localStorage.getItem(CLAVE_RESERVAFINAL)) || [];
                const horaTomada = reservasGuardadas.some(reserva =>
                    reserva.fecha === reservaFinal.fecha && reserva.hora === reservaFinal.hora
                );

                if (horaTomada) {
                    mostrarMensaje('No puede reservar esta fecha y hora porque ya está ocupada.');
                } else {
                    reservasGuardadas.push(reservaFinal);
                    localStorage.setItem(CLAVE_RESERVAFINAL, JSON.stringify(reservasGuardadas));
                    $('#modal-reserva-exitosa').modal('show'); 
                    actualizarContadorCarrito();  
                }
            }
        } catch (error) {
            console.error('Ocurrió un error al recoger los datos.');
        }
    }
}

document.querySelectorAll('.hora-btn').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.hora-btn').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    });
});


function guardarReserva() {
    const guardado = JSON.parse(localStorage.getItem(CLAVE_RESERVAFINAL)) || [];
    // Asegúrate de que reservasFinal tenga las reservas más recientes
    guardado.push(...reservasFinal);
    // Guardar el array completo en localStorage
    localStorage.setItem(CLAVE_RESERVAFINAL, JSON.stringify(guardado));
}
console.log(localStorage.getItem(CLAVE_RESERVAFINAL));

function mostrarReservas() {
    const carritoItemsContainer = document.getElementById("carrito-items");
    const reservas = JSON.parse(localStorage.getItem(CLAVE_RESERVAFINAL)) || [];
    carritoItemsContainer.innerHTML = '';

    reservas.forEach(reserva => {
        const reservaElement = document.createElement("div");
        reservaElement.classList.add("carrito-item");
        const contenidoReserva = `
            <h2>Reserva: ${reserva.tipo === '1' ? 'Terapia Individual' : 'Terapia de Parejas'}</h2>
            <p>Nombre de quien reserva: ${reserva.nombre} ${reserva.apellido}</p>
            <p>Télefono: ${reserva.telefono}</p>
            <p>Modalidad: ${reserva.tipo2 === '1' ? 'Presencial' : 'Online'}</p>
            <p>Hora: ${reserva.hora}</p>
            <p>Fecha: ${reserva.fecha}</p>
            <p>Precio: ${reserva.tipo === '1' ? '$24.500' : '$48.000'}</p>
        `;
        reservaElement.innerHTML = contenidoReserva;
        carritoItemsContainer.appendChild(reservaElement);
    });
}

mostrarReservas();


function pasoDePago(event) {
    if (!localStorage.getItem(CLAVE_RESERVAFINAL)) {
        alert("Usted no tiene ninguna reserva, por favor seleccione alguna para continuar su reserva");
        event.preventDefault(); 
    }
}

function limpiarLocalStorage() {
    if (localStorage.getItem(CLAVE_RESERVAFINAL)) {
        localStorage.removeItem(CLAVE_RESERVAFINAL);
        alert("El carrito ha sido vaciado.");
        window.location.reload();
    } else {
        alert("¡UPS! Al parecer, usted no tiene reserva agregada.");
    }
}
function mostrarMensajeEnModal(mensaje) {
    document.getElementById('alertMessage').innerText = mensaje;

    $('#alertModal').modal('show');
}

function limpiarLocalStorageFIN() {
    if (localStorage.getItem(CLAVE_RESERVAFINAL)) {
        localStorage.removeItem(CLAVE_RESERVAFINAL);
        window.location.reload();
    } else {
        mostrarMensajeEnModal("Compra realizada correctamente.");
    }
}


console.log(reservasFinal); // Verifica el contenido de reservasFinal antes de guardarlo

function actualizarContadorCarrito() {
    const reservas = JSON.parse(localStorage.getItem(CLAVE_RESERVAFINAL)) || [];
    const cantidadProductos = reservas.length;
    const contadorElemento = document.getElementById('cantidad-productos');
    if (contadorElemento) {
        contadorElemento.textContent = cantidadProductos;
    }
}

actualizarContadorCarrito();

// Función para calcular el precio total de las reservas
function calcularPrecioTotal() {
    let precioTotal = 0;

    // Obtener las reservas guardadas en localStorage
    const reservas = JSON.parse(localStorage.getItem(CLAVE_RESERVAFINAL)) || [];

    // Calcular el precio total sumando los precios de las reservas
    reservas.forEach(reserva => {
        // Asignar precios según el tipo de terapia
        if (reserva.tipo === '1') {
            precioTotal += 24500; 
        } else {
            precioTotal += 48000; 
        }
    });

    // Actualizar el contenido de la etiqueta <span class="carrito-precio-total">
    const carritoPrecioTotalElement = document.querySelector(".carrito-precio-total");
    carritoPrecioTotalElement.textContent = `$${precioTotal}`;
}

// Llamar a la función para calcular el precio total al cargar la página
calcularPrecioTotal();

function pasoDePago(event) {
    // Verificar si el carrito tiene datos o no en el localStorage
    if (!localStorage.getItem(CLAVE_RESERVAFINAL)) {
        alert("Usted no tiene ninguna reserva, por favor seleccione alguna para continuar su reserva");
        event.preventDefault(); 
    } 
}

document.querySelector('.btn-pagar').addEventListener('click', enviarReservasAJAX);

function enviarReservasAJAX() {
    const reservas = JSON.parse(localStorage.getItem('datos_reserva_final')) || [];

    if (reservas.length === 0) {
        alert("No tienes ninguna reserva seleccionada. Por favor, selecciona una reserva para continuar.");
        return;
    }

    // Eliminar duplicados basados en fecha y hora
    const reservasUnicas = reservas.filter((reserva, index, self) =>
        index === self.findIndex((t) => (
            t.fecha === reserva.fecha && t.hora === reserva.hora
        ))
    );

    fetch('/guardar-reservas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(reservasUnicas),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log('Reservas enviadas correctamente al backend.');
            localStorage.removeItem('datos_reserva_final');
            window.location.href = "{% url 'wait_and_redirect' %}";
        } else {
            console.error('Error en la respuesta del backend:', data.error);
        }
    })
    .catch(error => {
        console.error('Ocurrió un error al enviar reservas:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}