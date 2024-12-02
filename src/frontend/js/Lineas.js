function adjustHorizontalDivider() {
    // Calcula la altura máxima entre las columnas
    const codigoFuente = document.getElementById("codigoFuente");
    const sepXElementos = document.getElementById("sepXElementos");
    const identificacion = document.getElementById("identificacion");
    
    const maxHeight = Math.max(
        codigoFuente.offsetHeight,
        sepXElementos.offsetHeight,
        identificacion.offsetHeight
    );

    // Establece la posición de la línea horizontal justo al final de la columna más alta
    document.getElementById("horizontalDivider").style.top = maxHeight + "px";
}

// Llama a la función cuando cargue la página y cada vez que se redimensione la ventana
window.addEventListener("load", () => {
    adjustHorizontalDivider();
});
window.addEventListener("resize", () => {
    adjustHorizontalDivider();
});

