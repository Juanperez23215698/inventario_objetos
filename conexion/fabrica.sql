DROP DATABASE IF EXISTS fabrica;
CREATE DATABASE fabrica;
USE fabrica;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Tabla productosgenerales
CREATE TABLE `productosgenerales` (
    `IdProducto` int NOT NULL AUTO_INCREMENT,
    `NombreProducto` varchar(225) DEFAULT NULL,
    `DescripcionProducto` varchar(225) DEFAULT NULL,
    `TipoProducto` varchar(20) DEFAULT NULL,
    `CantidadProducto` int DEFAULT NULL,
    `ObservacionesProducto` varchar(225) DEFAULT NULL,
    PRIMARY KEY (`IdProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla usuarios
CREATE TABLE `usuarios` (
    `IdUsuario` int NOT NULL AUTO_INCREMENT,
    `NombreUsuario` varchar(255) DEFAULT NULL,
    `ApellidoUsuario` varchar(255) DEFAULT NULL,
    `TipoIdentificacion` enum('CC','TI') DEFAULT NULL,
    `NumeroIdentificacion` int(20) DEFAULT NULL,
    `CorreoUsuario` varchar(255) DEFAULT NULL,
    `CelularUsuario` int(20) DEFAULT NULL,
    `ContrasenaUsuario` varchar(50),
    PRIMARY KEY (`IdUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla prestatario
CREATE TABLE `prestatario` (
    `IdPrestatario` int NOT NULL AUTO_INCREMENT,
    `NombrePrestatario` varchar(255) DEFAULT NULL,
    `ApellidoPrestatario` varchar(255) DEFAULT NULL,
    `TipoIdentificacion` enum('CC','TI') DEFAULT NULL,
    `NumeroIdentificacion` int(20) DEFAULT NULL,
    `CorreoPrestatario` varchar(255) DEFAULT NULL,
    `CelularPrestatario` int(11) DEFAULT NULL,
    PRIMARY KEY (`IdPrestatario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla devoluciones
CREATE TABLE `devoluciones` (
    `IdDevoluciones` int(11) NOT NULL AUTO_INCREMENT,
    `IdPrestatario` int(11) DEFAULT NULL,
    `IdProducto` int(11) DEFAULT NULL,
    `FechaHoraDevolucion` datetime DEFAULT NULL,
    `EstadoDevolucion` enum('Bueno', 'Mal Estado') DEFAULT NULL,
    `Observaciones` varchar(225) DEFAULT NULL,
    `EstadoPrestamo` enum('Culminados') DEFAULT NULL,
    `CantidadDevolutiva` int(11) DEFAULT NULL,
    `ModoTiempoLugar` varchar(225) DEFAULT NULL,
    PRIMARY KEY (`IdDevoluciones`),
    FOREIGN KEY (`IdPrestatario`) REFERENCES `prestatario` (`IdPrestatario`),
    FOREIGN KEY (`IdProducto`) REFERENCES `productosgenerales` (`IdProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `prestamos` (
    `IdPrestamo` int NOT NULL AUTO_INCREMENT,
    `NombrePrestatario` varchar(255) NOT NULL,
    `IdentificacionPrestatario` varchar(50) NOT NULL,
    `FichaPrestatario` varchar(50) NOT NULL,
    `TelefonoPrestatario` varchar(15) NOT NULL,
    `FechaPrestamo` datetime NOT NULL,
    `ObservacionesPrestamo` text,
    `ObjetosPrestados` json NOT NULL,
    PRIMARY KEY (`IdPrestamo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertar datos de ejemplo en productosgenerales
INSERT INTO productosgenerales (NombreProducto, DescripcionProducto, TipoProducto, CantidadProducto, ObservacionesProducto)
VALUES
    ('Marcador', 'Marcador Sharpee Negro', 'Consumibles', 10, 'NO BORRABLE'),
    ('Computador', 'PORTATIL APPLE', 'Devolutivos', 2, 'NO FUNCIONA LA LETRA S'),
    ('Cable LAN', '2 METROSxCaja', 'Consumibles', 15, 'N/A'),
    ('Mouse Logitech', 'Mouse referencia: 81927', 'Devolutivos', 4, 'BUEN ESTADO'),
    ('Borrador', 'Borrador tablero nuevo', 'Consumibles', 22, 'NUEVOS');

-- Insertar datos de ejemplo en usuarios
INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario)
VALUES
    ('Santiago', 'Urrea', 'CC', 1031648741, 'santi@gmail.com', 3246016033, 'santi777'),
    ('Juan', 'Guzman', 'CC', 101781711, 'jp@gmail.com', 3105527890, 'jp777'),
    ('Juan', 'Cardenas', 'CC', 1131104356, 'juanchotv123@gmail.com', 3053577992, '123');

-- Insertar datos de ejemplo en prestatario
INSERT INTO prestatario (NombrePrestatario, ApellidoPrestatario, TipoIdentificacion, NumeroIdentificacion, CorreoPrestatario, CelularPrestatario)
VALUES
    ('Uldarico', 'Andrade', 'CC', 30567429, 'uandrade@soy.sena.edu.co', 3246016033),
    ('Fernando', 'Galindo', 'CC', 72648591, 'fegasu@gmail.com', 3105527890),
    ('María', 'López', 'CC', 12345678, 'mlopez@example.com', 3101234567),
    ('Juan', 'Pérez', 'CC', 87654321, 'jperez@example.com', 3201234567),
    ('Ana', 'Gómez', 'CC', 11223344, 'agomez@example.com', 3001234567);

-- Vista devoluciones
CREATE VIEW vista_devoluciones AS
SELECT 
    d.IdDevoluciones,
    d.IdPrestatario,
    pr.NombrePrestatario,
    d.IdProducto,
    pg.NombreProducto,
    d.FechaHoraDevolucion,
    d.EstadoDevolucion,
    d.Observaciones,
    d.CantidadDevolutiva,
    d.ModoTiempoLugar
FROM devoluciones d
JOIN prestatario pr ON d.IdPrestatario = pr.IdPrestatario
JOIN productosgenerales pg ON d.IdProducto = pg.IdProducto;

-- Triggers
DELIMITER //

CREATE TRIGGER actualizar_cantidad_producto
AFTER INSERT ON devoluciones
FOR EACH ROW
BEGIN
    UPDATE productosgenerales
    SET CantidadProducto = CantidadProducto + NEW.CantidadDevolutiva
    WHERE IdProducto = NEW.IdProducto;
END;//

DELIMITER ;


COMMIT;