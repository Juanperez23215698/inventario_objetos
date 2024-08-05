CREATE DATABASE fabrica;
USE fabrica;

-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-05-2024 a las 05:55:16
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `fabrica`



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones`
--

CREATE TABLE `devoluciones` (
    `IdDevoluciones` int(11) NOT NULL,
    `IdInstructor` int(11) DEFAULT NULL,
    `IdPrestamo` int(11) DEFAULT NULL,
    `IdProducto` int(11) DEFAULT NULL,
    `FechaHoraDevolucion` datetime DEFAULT NULL,
    `EstadoDevolucion` enum('Bueno', 'Mal Estado') DEFAULT NULL,
    `Observaciones` varchar(225) DEFAULT NULL,
    `EstadoPrestamo` enum('Culminados') DEFAULT NULL,
    `CantidadDevolutiva` int(11) DEFAULT NULL,
    `ModoTiempoLugar` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT * FROM devoluciones;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
    `IdPrestamo` int(11) NOT NULL,
    `IdInstructor` int(11) DEFAULT NULL,
    `IdProducto` int(11) DEFAULT NULL,
    `FechaHoraPrestamo` datetime DEFAULT NULL,
    `CantidadPrestamo` int(11) DEFAULT NULL,
    `EstadoPrestamo` enum('En curso', 'Culminados') DEFAULT NULL,
    `ObservacionesPrestamo` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT * FROM prestamos;


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productosgenerales`
--

CREATE TABLE `productosgenerales` (
    `IdProducto` int NOT NULL AUTO_INCREMENT,
    `NombreProducto` varchar(225) DEFAULT NULL,
    `DescripcionProducto` varchar(225) DEFAULT NULL,
    `TipoProducto` varchar(20) DEFAULT NULL,
    `CantidadProducto` int DEFAULT NULL,
    `ObservacionesProducto` varchar(225) DEFAULT NULL,
    PRIMARY KEY (`IdProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO productosgenerales (NombreProducto, DescripcionProducto, TipoProducto, CantidadProducto, ObservacionesProducto)
VALUES
    ('Marcador', 'Marcador Sharpee Negro', 'Consumibles', 10, 'NO BORRABLE'),
    ('Computador', 'PORTATIL APPLE', 'Devolutivos', 2, 'NO FUNCIONA LA LETRA S'),
    ('Cable LAN', '2 METROSxCaja', 'Consumibles', 15, 'N/A'),
    ('Mouse Logitech', 'Mouse referencia: 81927', 'Devolutivos', 4, 'BUEN ESTADO'),
    ('Borrador', 'Borrador tablero nuevo', 'Consumibles', 22, 'NUEVOS');

SELECT * FROM productosgenerales;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--
CREATE TABLE `usuarios` (
    `IdUsuario` int NOT NULL AUTO_INCREMENT,
    `NombreUsuario` varchar(255) DEFAULT NULL,
    `ApellidoUsuario` varchar(255) DEFAULT NULL,
    `TipoIdentificacion` enum('CC','TI') DEFAULT NULL,
    `NumeroIdentificacion` int(15) DEFAULT NULL,
    `CorreoUsuario` varchar(255) DEFAULT NULL,
    `CelularUsuario` int(11) DEFAULT NULL,
    `ContrasenaUsuario` varchar(50),
    PRIMARY KEY (`IdUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario)
VALUES
    ('Santiago', 'Urrea', 'CC', 1031648741, 'santi@gmail.com',  3246016033, 'santi777'),
    ('Juan', 'Guzman', 'CC', 101781711, 'jp@gmail.com',  3105527890, 'jp777');
SELECT * FROM usuarios;

--
-- Estructura de tabla para la tabla `instructores`
--
CREATE TABLE `instructores` (
    `IdInstructor` int NOT NULL AUTO_INCREMENT,
    `NombreInstructor` varchar(255) DEFAULT NULL,
    `ApellidoInstructor` varchar(255) DEFAULT NULL,
    `TipoIdentificacion` enum('CC','TI') DEFAULT NULL,
    `NumeroIdentificacion` int(15) DEFAULT NULL,
    `CorreoInstructor` varchar(255) DEFAULT NULL,
    `CelularInstructor` int(11) DEFAULT NULL,
    PRIMARY KEY (`IdInstructor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO instructores (NombreInstructor, ApellidoInstructor, TipoIdentificacion, NumeroIdentificacion, CorreoInstructor, CelularInstructor)
VALUES
    ('Uldarico', 'Andrade', 'CC', 30567429, 'uandrade@soy.sena.edu.co',  3246016033),
    ('Fernando', 'Galindo', 'CC', 72648591, 'fegasu@gmail.com',  3105527890);
SELECT * FROM instructores;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
    ADD PRIMARY KEY (`IdDevoluciones`),
    ADD KEY `IdInstructor` (`IdInstructor`),
    ADD KEY `IdPrestamo` (`IdPrestamo`),
    ADD KEY `IdProducto` (`IdProducto`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
    ADD PRIMARY KEY (`IdPrestamo`),
    ADD KEY `IdInstructor` (`IdInstructor`),
    ADD KEY `IdProducto` (`IdProducto`);

select * from prestamos;

--
-- AUTO_INCREMENT de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
    MODIFY `IdDevoluciones` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
    MODIFY `IdPrestamo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productosgenerales`
--
ALTER TABLE `productosgenerales`
    MODIFY `IdProducto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
    MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `instructores`
--
ALTER TABLE `instructores`
    MODIFY `IdInstructor` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
    ADD CONSTRAINT `devoluciones_ibfk_1` FOREIGN KEY (`IdInstructor`) REFERENCES `instructores` (`IdInstructor`),
    ADD CONSTRAINT `devoluciones_ibfk_2` FOREIGN KEY (`IdPrestamo`) REFERENCES `prestamos` (`IdPrestamo`),
    ADD CONSTRAINT `devoluciones_ibfk_3` FOREIGN KEY (`IdProducto`) REFERENCES `productosgenerales` (`IdProducto`);

--
-- Filtros para la tabla `prestamos`
--
ALTER TABLE `prestamos`
    ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`IdInstructor`) REFERENCES `instructores` (`IdInstructor`),
    ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`IdProducto`) REFERENCES `productosgenerales` (`IdProducto`);




--
-- Inserts para la tabla `prestamos`
--
INSERT INTO prestamos (IdInstructor, IdProducto, FechaHoraPrestamo, CantidadPrestamo, EstadoPrestamo, ObservacionesPrestamo)
VALUES
    (1, 4, '2024-06-12 10:30:00', 1, 'En curso', 'N/A'),
    (2, 1, '2024-06-12 10:30:00', 1, 'En curso', 'N/A');
SELECT * FROM prestamos;

--
-- Vista para la tabla `prestamos`
--
CREATE VIEW vista_prestamos AS
SELECT p.IdPrestamo, p.IdInstructor, i.NombreInstructor, i.ApellidoInstructor, p.IdProducto, pg.NombreProducto, p.FechaHoraPrestamo, p.CantidadPrestamo, p.EstadoPrestamo, p.ObservacionesPrestamo
FROM prestamos p
JOIN productosgenerales pg ON p.IdProducto = pg.IdProducto
JOIN instructores i ON p.IdInstructor = i.IdInstructor;

SELECT * FROM vista_prestamos;

--
-- Vista para la tabla `devoluciones`
--
CREATE VIEW vista_devoluciones AS
SELECT 
    d.IdDevoluciones,
    d.IdInstructor,
    i.NombreInstructor,
    d.IdPrestamo,
    d.IdProducto,
    pg.NombreProducto,
    d.FechaHoraDevolucion,
    d.EstadoDevolucion,
    d.Observaciones,
    d.EstadoPrestamo,
    d.CantidadDevolutiva,
    d.ModoTiempoLugar
FROM 
    devoluciones d
JOIN 
    instructores i ON d.IdInstructor = i.IdInstructor
JOIN 
    productosgenerales pg ON d.IdProducto = pg.IdProducto;

SELECT * FROM vista_devoluciones;



CREATE VIEW prestamos_en_curso AS
SELECT p.IdPrestamo, p.IdInstructor, i.NombreInstructor, i.ApellidoInstructor, p.IdProducto, pg.NombreProducto, 
    p.FechaHoraPrestamo, p.CantidadPrestamo, p.EstadoPrestamo, p.ObservacionesPrestamo
FROM prestamos p
JOIN productosgenerales pg ON p.IdProducto = pg.IdProducto
JOIN instructores i ON p.IdInstructor = i.IdInstructor
WHERE p.EstadoPrestamo = 'En curso';

SELECT * FROM prestamos_en_curso;




DELIMITER //

CREATE TRIGGER actualizar_estado_prestamo
AFTER INSERT ON devoluciones
FOR EACH ROW
BEGIN
    IF NEW.EstadoPrestamo = 'Culminados' THEN
        UPDATE prestamos
        SET EstadoPrestamo = 'Culminados'
        WHERE IdProducto = NEW.IdProducto;
    END IF;
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER actualizar_cantidad_producto
AFTER INSERT ON devoluciones
FOR EACH ROW
BEGIN
    UPDATE productosgenerales
    SET CantidadProducto = CantidadProducto + NEW.CantidadDevolutiva
    WHERE IdProducto = NEW.IdProducto;
END;
//

DELIMITER ;






DELIMITER //

CREATE TRIGGER restar_cantidad_producto
AFTER INSERT ON prestamos
FOR EACH ROW
BEGIN
    UPDATE productosgenerales
    SET CantidadProducto = CantidadProducto - NEW.CantidadPrestamo
    WHERE IdProducto = NEW.IdProducto;
END;

//

DELIMITER ;

COMMIT;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
