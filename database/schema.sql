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
