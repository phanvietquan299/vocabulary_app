CREATE DATABASE IF NOT EXISTS vocab_app
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE vocab_app;

ALTER DATABASE vocab_app
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS vocabularies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(100) NOT NULL,
    meaning VARCHAR(255) NOT NULL,
    pronunciation VARCHAR(100),
    example VARCHAR(255),
    image_url VARCHAR(255),
    topic VARCHAR(50)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
