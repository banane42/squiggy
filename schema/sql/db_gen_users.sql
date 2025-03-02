USE `squiggy`;

CREATE USER 'data_scribe'@'localhost' IDENTIFIED BY 'noosphere';
GRANT ALL PRIVILEGES ON `squiggy`.* TO 'data_scribe'@'localhost';