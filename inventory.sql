CREATE DATABASE inventory_system;
USE inventory_system;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    price FLOAT,
    expiry_date DATE
);
