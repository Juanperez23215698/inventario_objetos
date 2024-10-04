-- Drop database fabrica; 
CREATE DATABASE fabrica;
USE fabrica;



SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";




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


CREATE TABLE `usuarios` (
    `IdUsuario` int NOT NULL AUTO_INCREMENT,
    `NombreUsuario` varchar(255) DEFAULT NULL,
    `ApellidoUsuario` varchar(255) DEFAULT NULL,
    `TipoIdentificacion` enum('CC','TI') DEFAULT NULL,
    `NumeroIdentificacion` int(20) DEFAULT NULL,
    `CorreoUsuario` varchar(255) DEFAULT NULL,
    `CelularUsuario` varchar(20) DEFAULT NULL,
    `ContrasenaUsuario` varchar(50),
    PRIMARY KEY (`IdUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario)
VALUES
    ('Santiago', 'Urrea', 'CC', 1031648741, 'santi@gmail.com',  3246016033, 'santi777'),
    ('Juan', 'Guzman', 'CC', 101781711, 'jp@gmail.com',  3105527890, 'jp777'),
    -- Mas usuarios de prueba 
    ('Juan', 'Cardenas', 'CC', 1131104356, 'juanchotv123@gmail.com', 3053577992, '123');
SELECT * FROM usuarios;


CREATE TABLE `instructores` (
    `IdInstructor` int NOT NULL AUTO_INCREMENT,
    `NombreInstructor` varchar(255) DEFAULT NULL,
    `ApellidoInstructor` varchar(255) DEFAULT NULL,
    `TipoIdentificacion` enum('CC','TI') DEFAULT NULL,
    `NumeroIdentificacion` int(20) DEFAULT NULL,
    `CorreoInstructor` varchar(255) DEFAULT NULL,
    `CelularInstructor` varchar(11) DEFAULT NULL,
    PRIMARY KEY (`IdInstructor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO instructores (NombreInstructor, ApellidoInstructor, TipoIdentificacion, NumeroIdentificacion, CorreoInstructor, CelularInstructor)
VALUES
    ('Uldarico', 'Andrade', 'CC', 30567429, 'uandrade@soy.sena.edu.co',  3246016033),
    ('Fernando', 'Galindo', 'CC', 72648591, 'fegasu@gmail.com',  3105527890),
    -- Mas inserciones de prueba 
    ('María', 'López', 'CC', 12345678, 'mlopez@example.com', 3101234567),
    ('Juan', 'Pérez', 'CC', 87654321, 'jperez@example.com', 3201234567),
    ('Ana', 'Gómez', 'CC', 11223344, 'agomez@example.com', 3001234567),
    ('Luis', 'Rodríguez', 'CC', 55667788, 'lrodriguez@example.com', 3107654321),
    ('Carla', 'Fernández', 'CC', 99887766, 'cfernandez@example.com', 3151234567),
    ('Pedro', 'Martínez', 'CC', 44556677, 'pmartinez@example.com', 3111234567),
    ('Lucía', 'Sánchez', 'CC', 33445566, 'lsanchez@example.com', 3121234567),
    ('Miguel', 'Ramírez', 'CC', 22334455, 'mramirez@example.com', 3131234567),
    ('Elena', 'Torres', 'CC', 66778899, 'etorres@example.com', 3141234567),
    ('Carlos', 'Vargas', 'CC', 88990011, 'cvargas@example.com', 3157654321);
SELECT * FROM instructores;


ALTER TABLE `devoluciones`
    ADD PRIMARY KEY (`IdDevoluciones`),
    ADD KEY `IdInstructor` (`IdInstructor`),
    ADD KEY `IdPrestamo` (`IdPrestamo`),
    ADD KEY `IdProducto` (`IdProducto`);


ALTER TABLE `prestamos`
    ADD PRIMARY KEY (`IdPrestamo`),
    ADD KEY `IdInstructor` (`IdInstructor`),
    ADD KEY `IdProducto` (`IdProducto`);

select * from prestamos;


ALTER TABLE `devoluciones`
    MODIFY `IdDevoluciones` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `prestamos`
    MODIFY `IdPrestamo` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `productosgenerales`
    MODIFY `IdProducto` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `usuarios`
    MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `instructores`
    MODIFY `IdInstructor` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `devoluciones`
    ADD CONSTRAINT `devoluciones_ibfk_1` FOREIGN KEY (`IdInstructor`) REFERENCES `instructores` (`IdInstructor`),
    ADD CONSTRAINT `devoluciones_ibfk_2` FOREIGN KEY (`IdPrestamo`) REFERENCES `prestamos` (`IdPrestamo`),
    ADD CONSTRAINT `devoluciones_ibfk_3` FOREIGN KEY (`IdProducto`) REFERENCES `productosgenerales` (`IdProducto`);


ALTER TABLE `prestamos`
    ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`IdInstructor`) REFERENCES `instructores` (`IdInstructor`),
    ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`IdProducto`) REFERENCES `productosgenerales` (`IdProducto`);




INSERT INTO prestamos (IdInstructor, IdProducto, FechaHoraPrestamo, CantidadPrestamo, EstadoPrestamo, ObservacionesPrestamo)
VALUES
    (1, 4, '2024-06-12 10:30:00', 1, 'En curso', 'N/A'),
    (2, 1, '2024-06-12 10:30:00', 1, 'En curso', 'N/A');
SELECT * FROM prestamos;


CREATE VIEW vista_prestamos AS
SELECT p.IdPrestamo, p.IdInstructor, i.NombreInstructor, i.ApellidoInstructor, p.IdProducto, pg.NombreProducto, p.FechaHoraPrestamo, p.CantidadPrestamo, p.EstadoPrestamo, p.ObservacionesPrestamo
FROM prestamos p
JOIN productosgenerales pg ON p.IdProducto = pg.IdProducto
JOIN instructores i ON p.IdInstructor = i.IdInstructor;

SELECT * FROM vista_prestamos;


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



