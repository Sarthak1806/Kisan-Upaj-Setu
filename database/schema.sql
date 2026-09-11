CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'farmer'
);

CREATE TABLE procurement_centers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    address VARCHAR(255)
);

CREATE TABLE procurement_slots (
    id SERIAL PRIMARY KEY,
    center_id INTEGER REFERENCES procurement_centers(id),
    crop_name VARCHAR(100) NOT NULL,
    procurement_date VARCHAR(50) NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20) NOT NULL,
    capacity INTEGER DEFAULT 20,
    booked_count INTEGER DEFAULT 0
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    booking_code VARCHAR(50) UNIQUE,
    farmer_id INTEGER REFERENCES users(id),
    slot_id INTEGER REFERENCES procurement_slots(id),
    quantity_quintal FLOAT,
    status VARCHAR(50) DEFAULT 'Confirmed',
    payment_status VARCHAR(50) DEFAULT 'Pending',
    payment_amount FLOAT DEFAULT 0
);

INSERT INTO procurement_centers
(name, district, state, address)
VALUES
('Model Town Center', 'New Delhi', 'Delhi', NULL),
('Najafgarh Center', 'South West Delhi', 'Delhi', NULL),
('Mundka Center', 'West Delhi', 'Delhi', NULL);

INSERT INTO procurement_slots
(center_id, crop_name, procurement_date, start_time, end_time, capacity)
VALUES

-- MODEL TOWN CENTER

(1, 'Wheat',   '2026-09-06', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-06', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-06', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-06', '02:00 PM', '03:00 PM', 20),

(1, 'Wheat',   '2026-09-07', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-07', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-07', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-07', '02:00 PM', '03:00 PM', 20),

(1, 'Wheat',   '2026-09-08', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-08', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-08', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-08', '02:00 PM', '03:00 PM', 20),

(1, 'Wheat',   '2026-09-09', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-09', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-09', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-09', '02:00 PM', '03:00 PM', 20),

(1, 'Wheat',   '2026-09-10', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-10', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-10', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-10', '02:00 PM', '03:00 PM', 20),

(1, 'Wheat',   '2026-09-11', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-11', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-11', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-11', '02:00 PM', '03:00 PM', 20),

(1, 'Wheat',   '2026-09-12', '09:00 AM', '10:00 AM', 20),
(1, 'Rice',    '2026-09-12', '10:00 AM', '11:00 AM', 20),
(1, 'Maize',   '2026-09-12', '11:00 AM', '12:00 PM', 20),
(1, 'Mustard', '2026-09-12', '02:00 PM', '03:00 PM', 20),


-- NAJAFGARH CENTER

(2, 'Wheat',   '2026-09-06', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-06', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-06', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-06', '02:00 PM', '03:00 PM', 20),

(2, 'Wheat',   '2026-09-07', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-07', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-07', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-07', '02:00 PM', '03:00 PM', 20),

(2, 'Wheat',   '2026-09-08', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-08', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-08', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-08', '02:00 PM', '03:00 PM', 20),

(2, 'Wheat',   '2026-09-09', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-09', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-09', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-09', '02:00 PM', '03:00 PM', 20),

(2, 'Wheat',   '2026-09-10', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-10', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-10', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-10', '02:00 PM', '03:00 PM', 20),

(2, 'Wheat',   '2026-09-11', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-11', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-11', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-11', '02:00 PM', '03:00 PM', 20),

(2, 'Wheat',   '2026-09-12', '09:00 AM', '10:00 AM', 20),
(2, 'Rice',    '2026-09-12', '10:00 AM', '11:00 AM', 20),
(2, 'Maize',   '2026-09-12', '11:00 AM', '12:00 PM', 20),
(2, 'Mustard', '2026-09-12', '02:00 PM', '03:00 PM', 20),


-- MUNDKA CENTER

(3, 'Wheat',   '2026-09-06', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-06', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-06', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-06', '02:00 PM', '03:00 PM', 20),

(3, 'Wheat',   '2026-09-07', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-07', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-07', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-07', '02:00 PM', '03:00 PM', 20),

(3, 'Wheat',   '2026-09-08', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-08', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-08', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-08', '02:00 PM', '03:00 PM', 20),

(3, 'Wheat',   '2026-09-09', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-09', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-09', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-09', '02:00 PM', '03:00 PM', 20),

(3, 'Wheat',   '2026-09-10', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-10', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-10', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-10', '02:00 PM', '03:00 PM', 20),

(3, 'Wheat',   '2026-09-11', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-11', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-11', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-11', '02:00 PM', '03:00 PM', 20),

(3, 'Wheat',   '2026-09-12', '09:00 AM', '10:00 AM', 20),
(3, 'Rice',    '2026-09-12', '10:00 AM', '11:00 AM', 20),
(3, 'Maize',   '2026-09-12', '11:00 AM', '12:00 PM', 20),
(3, 'Mustard', '2026-09-12', '02:00 PM', '03:00 PM', 20);
