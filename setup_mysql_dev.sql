CREATE DATABASE IF NOT EXISTS Ecommerce;
CREATE USER IF NOT EXISTS 'aichaazlf'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON Ecommerce .* TO 'aichaazlf'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'aichaazlf'@'localhost';
FLUSH PRIVILEGES;