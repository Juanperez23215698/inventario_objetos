
-- Crear usuarios con correos completos
create user 'prueba'@'localhost' identified by 'prueba';
create user 'juanchotv123'@'localhost' identified by '123';
create user 'admin@sistema.com'@'localhost' identified by '123';

-- Crear y asignar roles
CREATE ROLE 'ADMIN';
grant select,insert,update,delete ON fabrica.* TO admin;

CREATE ROLE 'USUARIO';
GRANT ALL PRIVILEGES ON *.* TO 'juanchotv123'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
