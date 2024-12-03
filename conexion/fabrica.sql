<<<<<<< HEAD
DROP DATABASE IF EXISTS fabrica;
CREATE DATABASE fabrica;
USE fabrica;

=======
-- Drop database fabrica; 
CREATE DATABASE fabrica;
USE fabrica;



>>>>>>> 3cf74083f5ef97659d41e28158e18897e627ada6
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

<<<<<<< HEAD
-- Tabla productosgenerales
=======



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




>>>>>>> 3cf74083f5ef97659d41e28158e18897e627ada6
CREATE TABLE `productosgenerales` (
    `IdProducto` int NOT NULL AUTO_INCREMENT,
    `NombreProducto` varchar(225) DEFAULT NULL,
    `DescripcionProducto` varchar(225) DEFAULT NULL,
    `TipoProducto` varchar(20) DEFAULT NULL,
    `CantidadProducto` int DEFAULT NULL,
    `ObservacionesProducto` varchar(225) DEFAULT NULL,
    PRIMARY KEY (`IdProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

<<<<<<< HEAD
-- Tabla usuarios
=======
INSERT INTO productosgenerales (NombreProducto, DescripcionProducto, TipoProducto, CantidadProducto, ObservacionesProducto)
VALUES
    ('Marcador', 'Marcador Sharpee Negro', 'Consumibles', 10, 'NO BORRABLE'),
    ('Computador', 'PORTATIL APPLE', 'Devolutivos', 2, 'NO FUNCIONA LA LETRA S'),
    ('Cable LAN', '2 METROSxCaja', 'Consumibles', 15, 'N/A'),
    ('Mouse Logitech', 'Mouse referencia: 81927', 'Devolutivos', 4, 'BUEN ESTADO'),
    ('Borrador', 'Borrador tablero nuevo', 'Consumibles', 22, 'NUEVOS');

SELECT * FROM productosgenerales;


>>>>>>> 3cf74083f5ef97659d41e28158e18897e627ada6
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

<<<<<<< HEAD
-- Tabla prestamos
CREATE TABLE `prestamos` (
    `IdPrestamo` int NOT NULL AUTO_INCREMENT,
    `NombrePrestatario` varchar(255) NOT NULL,
    `IdentificacionPrestatario` varchar(50) NOT NULL,
    `FichaPrestatario` varchar(50) NOT NULL,
    `TelefonoPrestatario` varchar(50) NOT NULL,
    `FechaPrestamo` datetime NOT NULL,
    `ObservacionesPrestamo` text,
    `ObjetosPrestados` json NOT NULL,
    `TipoProducto` enum('Devolutivo(s)', 'No Devolutivo(s)') NOT NULL,
    `EstadoPrestamo` enum('Activo', 'Culminado') NOT NULL,
    PRIMARY KEY (`IdPrestamo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla devoluciones (actualizada con la relación a prestamos)
CREATE TABLE `devoluciones` (
    `IdDevoluciones` int(11) NOT NULL AUTO_INCREMENT,
    `IdPrestamo` int NOT NULL,
    `FechaHoraDevolucion` datetime DEFAULT NULL,
    `EstadoDevolucion` enum('Bueno', 'Mal Estado') DEFAULT NULL,
    `Observaciones` varchar(225) DEFAULT NULL,
    `EstadoPrestamo` enum('Devuelto') DEFAULT NULL,
    `CantidadDevolutiva` int(11) DEFAULT NULL,
    PRIMARY KEY (`IdDevoluciones`),
    CONSTRAINT `fk_devoluciones_prestamos` FOREIGN KEY (`IdPrestamo`) 
    REFERENCES `prestamos` (`IdPrestamo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10 inserciones para productosgenerales
INSERT INTO productosgenerales (NombreProducto, DescripcionProducto, TipoProducto, CantidadProducto, ObservacionesProducto) VALUES
('Laptop Dell', 'Laptop Dell Inspiron 15', 'Devolutivos', 5, 'Buen estado'),
('Proyector Epson', 'Proyector Epson PowerLite 118', 'Devolutivos', 3, 'Nuevo'),
('Tableta Gráfica', 'Tableta Wacom Intuos', 'Devolutivos', 2, 'Usado'),
('Cámara DSLR', 'Cámara Canon EOS Rebel T7', 'Devolutivos', 1, 'Excelente estado'),
('Micrófono', 'Micrófono Blue Yeti USB', 'Devolutivos', 4, 'Como nuevo'),
('Papel A4', 'Resma de papel A4', 'Consumibles', 50, 'Nuevo'),
('Bolígrafos', 'Caja de bolígrafos azules', 'Consumibles', 100, 'Nuevos'),
('Cuadernos', 'Cuadernos espirales tamaño carta', 'Consumibles', 30, 'Nuevos'),
('Tinta de Impresora', 'Cartucho de tinta negra HP', 'Consumibles', 10, 'Original'),
('Cable HDMI', 'Cable HDMI 2m', 'Consumibles', 15, 'Nuevo');
=======
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
    `CelularInstructor` int(11) DEFAULT NULL,
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
>>>>>>> 3cf74083f5ef97659d41e28158e18897e627ada6

-- 10 inserciones para usuarios
INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario) VALUES
('juan david ', 'Cardenas perez', 'CC', 1131104356, 'Juanchotv123@gmail.com', 3053577992, '123');

-- 10 inserciones para prestamos
INSERT INTO prestamos (NombrePrestatario, IdentificacionPrestatario, FichaPrestatario, TelefonoPrestatario, FechaPrestamo, ObservacionesPrestamo, ObjetosPrestados, TipoProducto) VALUES
('Laura Gómez', '1098765432', 'Ficha7', '3101234567', '2024-04-07 09:00:00', 'Préstamo de laptop', '[{"idProducto":6,"nombre":"Laptop Dell","descripcion":"Laptop Dell Inspiron 15","stock":1}]', 'Devolutivo(s)'),
('Carlos Rodríguez', '1087654321', 'Ficha8', '3202345678', '2024-04-08 10:30:00', 'Préstamo de proyector', '[{"idProducto":7,"nombre":"Proyector Epson","descripcion":"Proyector Epson PowerLite 118","stock":1}]', 'Devolutivo(s)'),
('Ana Martínez', '1076543210', 'Ficha9', '3303456789', '2024-04-09 11:45:00', 'Préstamo de tableta gráfica', '[{"idProducto":8,"nombre":"Tableta Gráfica","descripcion":"Tableta Wacom Intuos","stock":1}]', 'Devolutivo(s)'),
('Diego López', '1065432109', 'Ficha10', '3404567890', '2024-04-10 13:15:00', 'Préstamo de cámara', '[{"idProducto":9,"nombre":"Cámara DSLR","descripcion":"Cámara Canon EOS Rebel T7","stock":1}]', 'Devolutivo(s)'),
('María Sánchez', '1054321098', 'Ficha11', '3505678901', '2024-04-11 14:30:00', 'Préstamo de micrófono', '[{"idProducto":10,"nombre":"Micrófono","descripcion":"Micrófono Blue Yeti USB","stock":1}]', 'Devolutivo(s)'),
('Andrés Pérez', '1043210987', 'Ficha12', '3606789012', '2024-04-12 15:45:00', 'Préstamo de papel', '[{"idProducto":11,"nombre":"Papel A4","descripcion":"Resma de papel A4","stock":5}]', 'No Devolutivo(s)'),
('Sofía Díaz', '1032109876', 'Ficha13', '3707890123', '2024-04-13 16:00:00', 'Préstamo de bolígrafos', '[{"idProducto":12,"nombre":"Bolígrafos","descripcion":"Caja de bolígrafos azules","stock":10}]', 'No Devolutivo(s)'),
('Javier Torres', '1021098765', 'Ficha14', '3808901234', '2024-04-14 17:30:00', 'Préstamo de cuadernos', '[{"idProducto":13,"nombre":"Cuadernos","descripcion":"Cuadernos espirales tamaño carta","stock":3}]', 'No Devolutivo(s)'),
('Valentina Rojas', '1010987654', 'Ficha15', '3909012345', '2024-04-15 18:45:00', 'Préstamo de tinta', '[{"idProducto":14,"nombre":"Tinta de Impresora","descripcion":"Cartucho de tinta negra HP","stock":1}]', 'No Devolutivo(s)'),
('Gabriel Castro', '1009876543', 'Ficha16', '3001123456', '2024-04-16 09:15:00', 'Préstamo de cable HDMI', '[{"idProducto":15,"nombre":"Cable HDMI","descripcion":"Cable HDMI 2m","stock":1}]', 'No Devolutivo(s)');

-- 10 inserciones para devoluciones
INSERT INTO devoluciones (IdPrestamo, FechaHoraDevolucion, EstadoDevolucion, Observaciones, EstadoPrestamo, CantidadDevolutiva) VALUES
(1, '2024-04-10 14:00:00', 'Bueno', 'Devuelto en perfectas condiciones', 'Devuelto', 1),
(2, '2024-04-11 16:30:00', 'Bueno', 'Proyector funciona correctamente', 'Devuelto', 1),
(3, '2024-04-12 10:45:00', 'Bueno', 'Tableta en buen estado', 'Devuelto', 1),
(4, '2024-04-13 11:15:00', 'Mal Estado', 'Cámara con rasguños leves', 'Devuelto', 1),
(5, '2024-04-14 13:30:00', 'Bueno', 'Micrófono funciona perfectamente', 'Devuelto', 1),
(6, '2024-04-15 15:00:00', 'Bueno', 'Papel no devolutivo, se registra por control', 'Devuelto', 5),
(7, '2024-04-16 16:15:00', 'Bueno', 'Bolígrafos no devolutivos, se registra por control', 'Devuelto', 10),
(8, '2024-04-17 17:45:00', 'Bueno', 'Cuadernos no devolutivos, se registra por control', 'Devuelto', 3),
(9, '2024-04-18 09:30:00', 'Bueno', 'Tinta no devolutiva, se registra por control', 'Devuelto', 1),
(10, '2024-04-19 10:45:00', 'Bueno', 'Cable HDMI no devolutivo, se registra por control', 'Devuelto', 1);

-- Trigger para establecer el EstadoPrestamo basado en TipoProducto
DELIMITER //

CREATE TRIGGER set_estado_prestamo
BEFORE INSERT ON prestamos
FOR EACH ROW
BEGIN
    IF NEW.TipoProducto = 'Devolutivo(s)' THEN
        SET NEW.EstadoPrestamo = 'Activo';
    ELSEIF NEW.TipoProducto = 'No Devolutivo(s)' THEN
        SET NEW.EstadoPrestamo = 'Culminado';
    END IF;
END;//

DELIMITER ;

<<<<<<< HEAD
COMMIT;
=======

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



>>>>>>> 3cf74083f5ef97659d41e28158e18897e627ada6
