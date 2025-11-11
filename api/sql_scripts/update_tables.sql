ALTER TABLE patients
ADD COLUMN password_hash VARCHAR(500);

-- 1. Add hospital_id column to each table
ALTER TABLE medical_records
ADD COLUMN hospital_id INT;

ALTER TABLE prescriptions
ADD COLUMN hospital_id INT;

ALTER TABLE lab_test_results
ADD COLUMN hospital_id INT;

-- 2. Add foreign key constraints
ALTER TABLE medical_records
ADD CONSTRAINT fk_medical_record_hospital
FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id);

ALTER TABLE prescriptions
ADD CONSTRAINT fk_prescription_hospital
FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id);

ALTER TABLE lab_test_results
ADD CONSTRAINT fk_lab_test_result_hospital
FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id);
