CREATE TABLE payers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payer_code VARCHAR(50) NOT NULL UNIQUE,
    payer_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);