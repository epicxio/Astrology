-- First, disable foreign key checks
SET FOREIGN_KEY_CHECKS = 0;

-- Drop the existing places table
DROP TABLE IF EXISTS places;

-- Create the new places table with updated structure
CREATE TABLE places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1; 