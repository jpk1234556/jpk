-- Database Schema for Property Management System

-- Users table (for admins and property owners)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'property_owner')),
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Properties table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('hostel', 'apartment', 'hotel', 'rental')),
    address TEXT,
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rooms/Units table
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id),
    unit_number VARCHAR(50),
    type VARCHAR(50),
    capacity INTEGER,
    price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available', 'occupied', 'maintenance')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tenants table
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    unit_id INTEGER REFERENCES units(id),
    lease_start DATE,
    lease_end DATE,
    rent_amount DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Maintenance requests table
CREATE TABLE maintenance_requests (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER REFERENCES units(id),
    submitted_by INTEGER REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);