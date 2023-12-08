CREATE DATABASE proyecto;

SELECT proyecto

CREATE TABLE tienda (
    id_tienda INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tienda VARCHAR(30),
    ubicacion VARCHAR(30)
);
INSERT INTO tienda (id_tienda, nombre_tienda, ubicacion) VALUES
(1, 'Amazon', 'Mexico'),
(2, 'MercadoLibre', 'Mexico'),
(3, 'Amazon', 'USA'),
(4, 'BestBuy', 'USA');

CREATE TABLE samsung (
    id_sam INT AUTO_INCREMENT PRIMARY KEY,
    producto VARCHAR(50)
);

CREATE TABLE productos (
    id_productos INT AUTO_INCREMENT PRIMARY KEY,
    id_tienda INT,
    id_sam INT,
    producto VARCHAR(30),
    precio VARCHAR(30),
    calificacion VARCHAR(30),
    puntuaciones VARCHAR(30),
	FOREIGN KEY (id_tienda) REFERENCES productos(id_productos),
    FOREIGN KEY (id_sam) REFERENCES productos(id_productos)
);