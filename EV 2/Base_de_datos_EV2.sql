
CREATE DATABASE IF NOT EXISTS iot_systemsensor;
USE iot_systemsensor;

-- Tabla de sensores
CREATE TABLE sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,      
    ubicacion VARCHAR(150),            
    descripcion TEXT,                  
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de mediciones
CREATE TABLE measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,            
    nivel FLOAT NOT NULL,              
    alerta VARCHAR(50),
    estado VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

