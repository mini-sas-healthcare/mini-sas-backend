CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_id VARCHAR(100) NOT NULL UNIQUE,
    provider_id VARCHAR(100) NOT NULL,
    patient_id VARCHAR(100) NOT NULL,
    slot_time TIMESTAMP WITH TIME ZONE NOT NULL,

    status VARCHAR(50) NOT NULL CHECK (
        status IN ('PENDING', 'CONFIRMED', 'CANCELLED')
    ),

    cancelled_by VARCHAR(50),
    retry_count INTEGER DEFAULT 0,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);