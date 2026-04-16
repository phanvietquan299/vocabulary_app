CREATE TABLE IF NOT EXISTS vocabularies (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL,
    meaning VARCHAR(255) NOT NULL,
    pronunciation VARCHAR(100),
    example VARCHAR(255),
    local_url VARCHAR(255),
    remote_url VARCHAR(255),
    image_url VARCHAR(255),
    audio_url VARCHAR(255),
    topic VARCHAR(50)
);
