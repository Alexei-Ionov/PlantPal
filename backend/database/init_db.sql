-- Drop tables if they exist before creating them
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS plant_species CASCADE;
DROP TABLE IF EXISTS user_plants CASCADE;
DROP TABLE IF EXISTS sensor_readings CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE plant_species (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    genus VARCHAR(255),
    family VARCHAR(255),
    edible BOOLEAN,
    image_url VARCHAR(255),
    growth_rate VARCHAR(255),
    toxicity VARCHAR(255),
    average_height FLOAT, 
    light VARCHAR(255),
    soil_moisture FLOAT
);

CREATE TABLE user_plants (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255),
    current_moisture FLOAT NOT NULL,
    desired_soil_moisture FLOAT NOT NULL,
    last_update TIMESTAMP, 
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    -- species_id INTEGER REFERENCES plant_species(id) ON DELETE CASCADE
);

CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY, 
    moisture_level FLOAT NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    plant_id INTEGER REFERENCES user_plants(id) ON DELETE CASCADE

);