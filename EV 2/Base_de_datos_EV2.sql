
CREATE DATABASE IF NOT EXISTS iot_systemsensor;
USE iot_systemsensor;


CREATE TABLE IF NOT EXISTS water_level (
    id INT AUTO_INCREMENT PRIMARY KEY,   
    nivel FLOAT NOT NULL,                
    alerta VARCHAR(50),                  
    estado VARCHAR(50),                  
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);
