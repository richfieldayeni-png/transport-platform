-- Users Table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    company_name TEXT,
    date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Drivers Table
CREATE TABLE drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
-- Admin Table
CREATE TABLE admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'admin'
);

-- Routes Table
CREATE TABLE routes (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_name TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    estimated_duration INTEGER,
    is_route_available BOOLEAN DEFAULT TRUE,
    route_completion BOOLEAN DEFAULT FALSE
);

-- Buses Table
CREATE TABLE buses (
    bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_name TEXT NOT NULL,
    bus_type TEXT,
    total_seats INTEGER NOT NULL,
    plate_number TEXT UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Trips Table
CREATE TABLE trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER REFERENCES routes(route_id),
    bus_id INTEGER REFERENCES buses(bus_id),
    driver_id INTEGER REFERENCES drivers(driver_id),
    scheduled_departure_time TIMESTAMP,
    actual_departure_time TIMESTAMP,
    scheduled_arrival_time TIMESTAMP,
    actual_arrival_time TIMESTAMP,
    status TEXT DEFAULT 'scheduled',
    date DATE NOT NULL
);

-- Payments Table
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_type TEXT NOT NULL,
    payment_status TEXT DEFAULT 'pending',
    payment_confirmation TEXT,
    payment_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_completion BOOLEAN DEFAULT FALSE,
    amount DECIMAL(10,2) NOT NULL
);

-- Bookings Table
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    trip_id INTEGER REFERENCES trips(trip_id),
    payment_id INTEGER REFERENCES payments(payment_id),
    seat_number INTEGER NOT NULL,
    reservation_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    booking_confirmation TEXT,
    booking_status TEXT DEFAULT 'pending'
);

-- Notifications Table
CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    trip_id INTEGER REFERENCES trips(trip_id),
    notification_type TEXT NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GPS Tracking Table
CREATE TABLE gps_locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER REFERENCES trips(trip_id),
    bus_id INTEGER REFERENCES buses(bus_id),
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    distance_covered DECIMAL(10,2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);