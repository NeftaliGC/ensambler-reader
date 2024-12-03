const API = 'http://127.0.0.1:8000';
let RESPONSE = {};
let currentPage = 0; // Página actual
const LINES_PER_PAGE = 5; // Líneas por página

const atras = document.getElementById('atras');
const adelante = document.getElementById('adelante');

// Cargar el archivo .asm
document.getElementById('file').addEventListener('change', async function () {
	const fileInput = this;
	const file = fileInput.files[0];
	const fileName = file ? file.name : '';

	// Verificar que el archivo tenga la extensión .ens
	if (!fileName.endsWith('.ens')) {
		alert('Por favor, selecciona un archivo con extensión .ens');
		return; // Detener el proceso si el archivo no es .ens
	}
	document.getElementById('file-name').textContent = fileName;

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
			showSegments(); // Mostrar los segmentos en la tabla
			showSymbols(); // Mostrar los símbolos en la tabla de símbolos
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

// Mostrar segmentos en la tabla
function showSegments() {
	const segmentos = RESPONSE.segmentos;

	// Llenar la tabla de inmediato
	populateTableSegment(segmentos); // Llenar la tabla con todos los datos

	// Actualizar la visibilidad de las filas según la página actual
	updateTableVisibility();

	// Función para llenar la tabla de segmentos
	function populateTableSegment(data) {
		const tableBody = document.querySelector('#IdElementos tbody');
		tableBody.innerHTML = ''; // Limpiar la tabla antes de actualizar

		// Iteramos sobre todos los segmentos de los datos
		data.forEach((segment) => {
			segment.forEach((line) => {
				const row = document.createElement('tr');

				const cp = line.cp || '';
				const complete = line.complete || '';
				const lineContent = Array.isArray(line.line)
					? line.line
					: [line.line];
				const classification = Array.isArray(line.classification)
					? line.classification
					: [line.classification];
				const codificacion = line.codificacion || '';
				const errores = line.errores || '';

				const cpCell = `<td>${cp}</td>`;
				const completeCell = `<td>${complete}</td>`;
				const codificacionCell = `<td>${codificacion}</td>`;
				const erroresCell = `<td>${errores}</td>`;

				const lineCell = document.createElement('td');
				lineContent.forEach((element) => {
					const span = document.createElement('span');
					span.textContent = element;
					lineCell.appendChild(span);
					lineCell.appendChild(document.createElement('br'));
				});

				const classificationCell = document.createElement('td');
				classification.forEach((element) => {
					const span = document.createElement('span');
					span.textContent = element;
					classificationCell.appendChild(span);
					classificationCell.appendChild(
						document.createElement('br')
					);
				});

				row.innerHTML = `${cpCell}${completeCell}`;
				row.appendChild(lineCell);
				row.appendChild(classificationCell);
				row.innerHTML += `${codificacionCell}${erroresCell}`;

				tableBody.appendChild(row);
			});
		});
	}

	// Función para actualizar la visibilidad de las filas en la tabla
	function updateTableVisibility() {
		const tableRows = document.querySelectorAll('#IdElementos tbody tr');
		const totalRows = tableRows.length;
		const start = currentPage * LINES_PER_PAGE;
		const end = start + LINES_PER_PAGE;

		tableRows.forEach((row, index) => {
			if (index >= start && index < end) {
				row.style.display = 'table-row'; // Mostrar la fila
			} else {
				row.style.display = 'none'; // Ocultar la fila
			}
		});
	}

	// Navegación entre páginas
	atras.addEventListener('click', () => {
		if (currentPage > 0) {
			currentPage--;
			updateTableVisibility();
		}
	});

	adelante.addEventListener('click', () => {
		const totalRows = document.querySelectorAll(
			'#IdElementos tbody tr'
		).length;
		const totalPages = Math.ceil(totalRows / LINES_PER_PAGE);
		if (currentPage < totalPages - 1) {
			currentPage++;
			updateTableVisibility();
		}
	});
}

// Mostrar símbolos en la tabla de símbolos
function showSymbols() {
	const simbolos = RESPONSE.simbols;

	// Llenar la tabla de símbolos
	populateSymbolTable(simbolos);

	// Función para llenar la tabla de símbolos
	function populateSymbolTable(data) {
		const tableBody = document.querySelector('#Simbolos tbody');
		tableBody.innerHTML = ''; // Limpiar la tabla antes de actualizar

		// Iteramos sobre los datos de los símbolos
		data.forEach((symbol) => {
			const row = document.createElement('tr');

			const nombre = symbol.simbolo || '';
			const tipo = symbol.tipo || '';
			const direccion = symbol.valor || '';
			const valor = symbol.tamano || '';

			row.innerHTML = `<td>${nombre}</td><td>${tipo}</td><td>${direccion}</td><td>${valor}</td>`;

			tableBody.appendChild(row);
		});
	}
}
