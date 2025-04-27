-- Create database
CREATE DATABASE IF NOT EXISTS epic_x_horoscope;
USE epic_x_horoscope;

-- Users table (optional, for future authentication)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Places table (for dropdown data)
CREATE TABLE IF NOT EXISTS places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Horoscope calculations table
CREATE TABLE IF NOT EXISTS horoscope_calculations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_birth DATE NOT NULL,
    time_of_birth TIME NOT NULL,
    place_id INT NOT NULL,
    rashi VARCHAR(20) NOT NULL,
    nakshatra VARCHAR(20) NOT NULL,
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(id)
);

-- Match making results table
CREATE TABLE IF NOT EXISTS matchmaking_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    boy_name VARCHAR(100) NOT NULL,
    girl_name VARCHAR(100) NOT NULL,
    boy_horoscope_id INT NOT NULL,
    girl_horoscope_id INT NOT NULL,
    compatibility_score DECIMAL(5,2) NOT NULL,
    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (boy_horoscope_id) REFERENCES horoscope_calculations(id),
    FOREIGN KEY (girl_horoscope_id) REFERENCES horoscope_calculations(id)
);

-- Translations table
CREATE TABLE IF NOT EXISTS translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(100) NOT NULL,
    language VARCHAR(10) NOT NULL,
    value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_translation (`key`, language)
);

-- Create indexes
CREATE INDEX idx_places_name ON places(name);
CREATE INDEX idx_horoscope_dob ON horoscope_calculations(date_of_birth);
CREATE INDEX idx_matchmaking_names ON matchmaking_results(boy_name, girl_name);
CREATE INDEX idx_translations_key ON translations(`key`);
