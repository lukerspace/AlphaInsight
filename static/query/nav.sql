CREATE DATABASE IF NOT EXISTS dashboard;

use dashboard;


CREATE TABLE IF NOT EXISTS nav (
    Date DATETIME,
    Nav FLOAT,
    Label VARCHAR(255),
    Graphname VARCHAR(255),
    CreatedDate DATETIME
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into users (name,email,password,created_at) VALUES ('root','root@admin','0000','2024-09-03');

