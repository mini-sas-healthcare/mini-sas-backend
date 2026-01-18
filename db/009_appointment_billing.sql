CREATE TABLE appointment_billing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    appointment_id VARCHAR(100) NOT NULL UNIQUE,
    patient_id VARCHAR(100) NOT NULL,
    provider_id VARCHAR(100) NOT NULL,

    cpt_code VARCHAR(20) NOT NULL,
    payer_code VARCHAR(50) NOT NULL,

    amount NUMERIC(10,2) NOT NULL,

    status VARCHAR(50) NOT NULL CHECK (
        status IN ('PENDING', 'COMPLETED')
    ),

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_appointment_billing_appointment
        FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),

    CONSTRAINT fk_appointment_billing_patient
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id),

    CONSTRAINT fk_appointment_billing_provider
        FOREIGN KEY (provider_id) REFERENCES providers(provider_id),

    CONSTRAINT fk_appointment_billing_cpt
        FOREIGN KEY (cpt_code) REFERENCES cpt_codes(cpt_code),

    CONSTRAINT fk_appointment_billing_payer
        FOREIGN KEY (payer_code) REFERENCES payers(payer_code)
);
