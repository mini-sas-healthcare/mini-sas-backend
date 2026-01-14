CREATE TABLE cpt_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cpt_code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    global_period_days INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);