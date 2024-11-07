const API = 'http://127.0.0.1:8000';
let RESPONSE = {};

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

function showSegments(idSegment) {
	const segmentos = RESPONSE.segmentos;
	const codigoFuente = document.getElementById('codigoFuente');
	const sepxelementos = document.getElementById('sepXElementos');
	const identificacion = document.getElementById('identificacion');

	// Limpiar el contenido actual
	codigoFuente.innerHTML = '';
	sepxelementos.innerHTML = '';
	identificacion.innerHTML = '';

	// mostrar en codigo fuente el quinto segmento
	const code = segmentos[4];
	code[0].forEach((element) => {
		codigoFuente.innerHTML += elem + '</br>';
		element.forEach((elem) => {});
	});

	const sepelem = segmentos.slice(0, 4);
	console.log(sepelem);
	sepelem.forEach((element) => {
		element.forEach((elem) => {
			sepxelementos.innerHTML += elem.line + '</br>';
		});
		/* sepxelementos.innerHTML += element.line + '</br>'; */
	});

	const identifier = segmentos.slice(0, 4);
	sepelem.forEach((element) => {
		element.forEach((elem) => {
			identificacion.innerHTML += elem.classification + '</br>';
		});
	});
}
