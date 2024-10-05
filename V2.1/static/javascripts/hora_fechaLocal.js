function setCurrentDateTime() {
    const now = new Date();
    const offset = now.getTimezoneOffset();
    now.setMinutes(now.getMinutes() - offset);

    // Convertir la fecha a un formato adecuado para el input
    const formattedDateTime = now.toISOString().slice(0, 16);

    // Establecer el valor del input al valor actual
    document.getElementById('datetime').value = formattedDateTime;
}

// Llamar a la función para establecer la fecha y hora actuales
setCurrentDateTime();