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
    `NumeroIdentificacion` varchar(20) DEFAULT NULL,
    `CorreoUsuario` varchar(255) DEFAULT NULL,
    `CelularUsuario` varchar(20) DEFAULT NULL,
    `ContrasenaUsuario` varchar(50),
    PRIMARY KEY (`IdUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla prestamos
CREATE TABLE `prestamos` (
    `IdPrestamo` int NOT NULL AUTO_INCREMENT,
    `NombrePrestatario` varchar(255) NOT NULL,
    `IdentificacionPrestatario` varchar(50) NOT NULL,
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

-- 10 inserciones para usuarios
INSERT INTO usuarios (NombreUsuario, ApellidoUsuario, TipoIdentificacion, NumeroIdentificacion, CorreoUsuario, CelularUsuario, ContrasenaUsuario) VALUES
('juan david ', 'Cardenas perez', 'CC', 1131104356, 'Juanchotv123@gmail.com', 3053577992, '123');

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

COMMIT;

create user 'juanchotv123@gmail.com'@'localhost' identified by '123';
create user 'admin'@'localhost' identified by '123';

-- CREATE ROLE 'ADMIN';
--     grant select,insert,update,delete ON fabrica.* TO admin;

-- CREATE ROLE 'juanchotv123';
--     GRANT ALL PRIVILEGES ON *.* TO 'juanchotv123'@'localhost' WITH GRANT OPTION;
--     FLUSH PRIVILEGES;

        
