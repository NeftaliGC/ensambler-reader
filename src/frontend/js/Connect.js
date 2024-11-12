const API = 'http://127.0.0.1:8000';
let RESPONSE = {};
let currentPage = 0; //páginación actual
const LINES_PER_PAGE = 10; // Cantidad de líneas por página

atras = document.getElementById('atras');
adelante = document.getElementById('adelante');

document.getElementById('file').addEventListener('change', async function () {
	const fileInput = this;
	const file = fileInput.files[0];
	const fileName = file ? file.name : '';

	// Verificar que el archivo tenga la extensión .asm
	if (!fileName.endsWith('.asm')) {
		alert('Por favor, selecciona un archivo con extensión .asm');
		return; // Detener el proceso si el archivo no es .asm
	}
	document.getElementById('file-name').textContent = fileName;

	// Desplazarse a la sección "main"
	document.querySelector('main').scrollIntoView({ behavior: 'smooth' });

	// Crear un FormData y agregar el archivo
	const formData = new FormData();
	formData.append('file', file);

	try {
		const response = await fetch(`${API}/uploadfile/`, {
			method: 'POST',
			body: formData,
		});

		if (response.ok) {
			const data = await response.json();
			RESPONSE = data;
			console.log('Archivo cargado con éxito:', RESPONSE);
			showSegments();
			// Puedes actualizar la UI con los datos de "segmentos" obtenidos de la respuesta
		} else {
			console.error(
				'Error en la carga del archivo:',
				response.statusText
			);
		}
	} catch (error) {
		console.error('Error de conexión con el servidor:', error);
	}
});


// Función para mostrar segmentos de código
function showSegments() {
    const segmentos = RESPONSE.segmentos; // Asegúrate de que RESPONSE.segmentos esté correctamente asignado al archivo JSON cargado
    const codigoFuente = document.getElementById('codigoFuente');
    const sepxelementos = document.getElementById('sepXElementos');
    const identificacion = document.getElementById('identificacion');

    // Limpiar el contenido actual
    codigoFuente.innerHTML = '';
    sepxelementos.innerHTML = '';
    identificacion.innerHTML = '';

    // Calcular el rango de líneas a mostrar
    const start = currentPage * LINES_PER_PAGE;
    const end = start + LINES_PER_PAGE;

    // Verificar si estamos dentro del rango del total de líneas
    if (start >= segmentos.length) {
        currentPage = Math.max(0, Math.floor(segmentos.length / LINES_PER_PAGE) - 1);
        return;
    }

    // Mostrar las líneas de código y sus identificaciones en el rango especificado
    segmentos.slice(start, end).forEach((segment) => {
        segment.forEach((lineInfo) => {
            codigoFuente.innerHTML += `${lineInfo.line}<br>`;
            sepxelementos.innerHTML += `${lineInfo.line}<br>`;
            identificacion.innerHTML += `${lineInfo.classification}<br>`;
        });
    });

    // Desactivar botones si estamos en la primera o última página
    document.getElementById('atras').disabled = currentPage === 0;
    document.getElementById('adelante').disabled = end >= segmentos.length;
}

// Función para cambiar de página
function changePage(offset) {
    currentPage += offset;
    showSegments();
}

// Eventos para los botones "adelante" y "atrás"
document.getElementById('adelante').addEventListener('click', () => changePage(1));
document.getElementById('atras').addEventListener('click', () => changePage(-1));

// Inicializar la primera visualización de segmentos
showSegments();
