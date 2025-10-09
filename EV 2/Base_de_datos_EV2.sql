CREATE DATABASE IF NOT EXISTS iot_systemsensor;
USE iot_systemsensor;

CREATE TABLE IF NOT EXISTS sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(150),
    descripcion TEXT,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    nivel FLOAT,
    alerta TINYINT,
    estado VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

INSERT INTO sensors (nombre, ubicacion, descripcion)
VALUES ('Tanque principal', 'Planta alta', 'HC-SR04 en tanque A');


select * FROM sensors;

select * FROM measurements;

USE iot_systemsensor;

SHOW TABLES;
