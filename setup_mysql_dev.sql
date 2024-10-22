-- prepares MySQL server
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED by 'hbnb_dev_pwd';
CREATE TABLE IF NOT EXISTS hbnb_dev_db.states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS hbnb_dev_db.cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    name VARCHAR(128) NOT NULL
    CONSTRAINT fk_state_id FOREIGN KEY (state_id) REFERENCES states(id)
    on DELETE CASCADE
);
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
