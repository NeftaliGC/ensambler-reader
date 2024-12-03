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

function showSegments(idSegment) {
	const segmentos = RESPONSE.segmentos;
	// Referencia a la tabla donde se agregarán las filas

	populateTableSegment(segmentos);
	populateTableSimbols(segmentos);
}

// Función para agregar datos a la tabla
function populateTableSegment(data) {
	// Referencia a la tabla donde se agregarán las filas
	const tableBody = document.querySelector('#IdElementos tbody');
	// Iteramos sobre cada segmento
	data.forEach((segment) => {
		// Iteramos sobre cada línea dentro del segmento
		segment.forEach((line) => {
			// Creamos una nueva fila
			const row = document.createElement('tr');

			// Extraemos los datos necesarios
			const cp = line.cp || '';
			const complete = line.complete || '';
			const lineContent = Array.isArray(line.line)
				? line.line
				: [line.line]; // Aseguramos que sea un array
			const classification = Array.isArray(line.classification)
				? line.classification
				: [line.classification]; // Aseguramos que sea un array
			const codificacion = line.codificacion || '';
			const errores = line.errores || '';

			// Creamos las celdas de la fila
			const cpCell = `<td>${cp}</td>`;
			const completeCell = `<td>${complete}</td>`;
			const codificacionCell = `<td>${codificacion}</td>`;
			const erroresCell = `<td>${errores}</td>`;

			// Creamos la celda para Separación de Elementos con <br>
			const lineCell = document.createElement('td');
			lineContent.forEach((element) => {
				const span = document.createElement('span');
				span.textContent = element;
				lineCell.appendChild(span);
				lineCell.appendChild(document.createElement('br')); // Agregamos el <br>
			});

			// Creamos la celda para Identificación con <br>
			const classificationCell = document.createElement('td');
			classification.forEach((element) => {
				const span = document.createElement('span');
				span.textContent = element;
				classificationCell.appendChild(span);
				classificationCell.appendChild(document.createElement('br')); // Agregamos el <br>
			});

			// Construimos la fila completa
			row.innerHTML = `
                ${cpCell}
                ${completeCell}
            `;
			row.appendChild(lineCell); // Agregamos la celda con separación de elementos
			row.appendChild(classificationCell); // Agregamos la celda con identificación
			row.innerHTML += `
                ${codificacionCell}
                ${erroresCell}
            `;

			// Agregamos la fila al cuerpo de la tabla
			tableBody.appendChild(row);
		});
	});
}

function populateTableSimbols(data) {
	// Referencia a la tabla donde se agregarán las filas
	const tableBody = document.querySelector('#Simbolos tbody');
	// Iteramos sobre los segmentos
	data.forEach((segment) => {
		// Iteramos sobre cada línea dentro del segmento
		segment.forEach((line) => {
			// Verificar si no hay errores en la línea, es decir, si el error es "correcto"
			const errores = line.errores || '';
			if (errores !== 'Correcto') return; // Si hay un error, no agregar la línea a la tabla

			// Crear una nueva fila para la tabla de símbolos
			const row = document.createElement('tr');

			// Extraemos los datos necesarios
			const simbolo = line.line[0] || ''; // Se toma el valor de la línea como símbolo
			const tipo = Array.isArray(line.classification)
				? line.classification.join(', ')
				: line.line[1] || ''; // El tipo puede ser un arreglo de clasificaciones o el segundo valor de la línea
			const valor = line.complete || ''; // El valor es el contenido completo de la línea
			const tamano = line.codificacion || ''; // El tamaño (codificación) de la línea

			// Creamos las celdas de la fila
			const simboloCell = `<td>${simbolo}</td>`;
			const tipoCell = `<td>${tipo}</td>`;
			const valorCell = `<td>${valor}</td>`;
			const tamanoCell = `<td>${tamano}</td>`;

			// Añadimos las celdas a la fila
			row.innerHTML = `
                ${simboloCell}
                ${tipoCell}
                ${valorCell}
                ${tamanoCell}
            `;

			// Agregamos la fila al cuerpo de la tabla
			tableBody.appendChild(row);
		});
	});
}
