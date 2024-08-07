CREATE TABLE accounts(
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'user',
    permission VARCHAR DEFAULT 'read-only'
);

CREATE TABLE companies(
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE positions(
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE individuals(
    id SERIAL PRIMARY KEY,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    position_id INTEGER REFERENCES positions(id) ON DELETE SET NULL,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    CONSTRAINT unique_individual UNIQUE (position_id, company_id, firstname, lastname)
);

CREATE TABLE parent_companies(
    relation VARCHAR NOT NULL,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    CONSTRAINT parent_company_pk PRIMARY KEY (company_id, parent_id)
);


INSERT INTO companies
    (name)
VALUES
('NovaTech Solutions'),
('BlueSky Innovations'),
('SummitStream Enterprises'),
('SwiftEdge Technologies'),
('SilverLine Dynamics'),
('BrightPath Ventures'),
('TerraNova Industries'),
('HorizonTech Group'),
('QuantumLeap Solutions'),
('InfiniteSphere Inc.'),
('StellarWave Enterprises'),
('NexusGen Corporation'),
('FusionAxis Technologies'),
('ApexPeak Ventures'),
('Sunburst Innovations'),
('EverGreen Solutions'),
('SparkLink Industries'),
('PrimePulse Enterprises'),
('ZenithTech Group'),
('AgileCore Solutions');


INSERT INTO parent_companies
    (company_id, parent_id, relation)
VALUES
    (1, 2, 'Immediate Parent'),
    (1, 3, 'Immediate Parent'),
    (1, 4, 'Immediate Parent'),
    (1, 5, 'Ultimate Parent'),
    (2, 6, 'Ultimate Parent'),
    (2, 7, 'Ultimate Parent'),
    (2, 8, 'Immediate Parent'),
    (2, 9, 'Immediate Parent'),
    (3, 10, 'Ultimate Parent'),
    (3, 11, 'Immediate Parent'),
    (3, 12, 'Immediate Parent'),
    (3, 13, 'Immediate Parent'),
    (4, 14, 'Ultimate Parent'),
    (4, 15, 'Immediate Parent'),
    (4, 16, 'Immediate Parent'),
    (4, 17, 'Immediate Parent'),
    (5, 18, 'Immediate Parent'),
    (5, 19, 'Immediate Parent'),
    (5, 20, 'Ultimate Parent');


INSERT INTO positions
    (name)
VALUES
    ('Commissioner'),
    ('Director'),
    ('General Manager'),
    ('President Commissioner'),
    ('President Director'),
    ('Shareholder'),
    ('Vice President');


-- companies = 20, positions = 7
INSERT INTO individuals
    (firstname, lastname, position_id, company_id)
VALUES
    ('Abigail', 'Roberts', 5, 5),
    ('Abigail', 'Roberts', 5, 18),
    ('Abigail', 'Roberts', 3, 12),
    ('Abigail', 'Roberts', 3, 1),
    ('Alexander', 'Johnson', 3, 17),
    ('Alexander', 'Johnson', 7, 7),
    ('Alexander', 'Johnson', 7, 11),
    ('Alexander', 'Johnson', 7, 8),
    ('Alexander', 'Johnson', 2, 9),
    ('Astuti', 'Widodo', 7, 12),
    ('Astuti', 'Widodo', 2, 9),
    ('Astuti', 'Widodo', 2, 6),
    ('Astuti', 'Widodo', 2, 13),
    ('Benjamin', 'Green', 1, 8),
    ('Benjamin', 'Green', 1, 6),
    ('Benjamin', 'Green', 1, 13),
    ('Benjamin', 'Green', 1, 18),
    ('Benjamin', 'Green', 1, 16),
    ('Benjamin', 'Green', 6, 3),
    ('Budi', 'Santoso', 4, 14),
    ('Budi', 'Santoso', 4, 8),
    ('Budi', 'Santoso', 4, 5),
    ('Budi', 'Santoso', 4, 3),
    ('Budi', 'Santoso', 4, 19),
    ('Charlotte', 'King', 3, 6),
    ('Charlotte', 'King', 5, 5),
    ('Charlotte', 'King', 5, 8),
    ('Charlotte', 'King', 5, 1),
    ('Charlotte', 'King', 3, 17),
    ('Charlotte', 'King', 3, 13),
    ('Charlotte', 'King', 3, 2),
    ('Christopher', 'Scott', 7, 9),
    ('Christopher', 'Scott', 2, 13),
    ('Christopher', 'Scott', 2, 12),
    ('Christopher', 'Scott', 7, 10),
    ('Daniel', 'Lewis', 2, 20),
    ('Daniel', 'Lewis', 2, 17),
    ('Daniel', 'Lewis', 2, 6),
    ('Daniel', 'Lewis', 2, 14),
    ('Daniel', 'Lewis', 2, 16),
    ('Daniel', 'Lewis', 5, 2),
    ('David', 'Quinn', 1, 15),
    ('David', 'Quinn', 6, 11),
    ('David', 'Quinn', 6, 12),
    ('David', 'Quinn', 6, 18),
    ('David', 'Quinn', 6, 14),
    ('Dewi', 'Sari', 4, 10),
    ('Dewi', 'Sari', 4, 3),
    ('Dewi', 'Sari', 4, 7),
    ('Dewi', 'Sari', 4, 4),
    ('Dewi', 'Sari', 4, 6),
    ('Dewi', 'Sari', 4, 12),
    ('Dewi', 'Sari', 6, 18),
    ('Dika', 'Wahyudi', 3, 11),
    ('Dika', 'Wahyudi', 2, 5),
    ('Dika', 'Wahyudi', 2, 9),
    ('Dika', 'Wahyudi', 3, 3),
    ('Dimas', 'Prasetyo', 4, 8),
    ('Dimas', 'Prasetyo', 4, 19),
    ('Dimas', 'Prasetyo', 5, 14),
    ('Dimas', 'Prasetyo', 5, 18),
    ('Dimas', 'Prasetyo', 3, 13),
    ('Dimas', 'Prasetyo', 3, 9),
    ('Dimas', 'Prasetyo', 7, 16),
    ('Dimas', 'Prasetyo', 7, 11),
    ('Elizabeth', 'Turner', 1, 2),
    ('Elizabeth', 'Turner', 1, 4),
    ('Elizabeth', 'Turner', 1, 3),
    ('Elizabeth', 'Turner', 1, 5),
    ('Elizabeth', 'Turner', 2, 6),
    ('Elizabeth', 'Turner', 2, 11),
    ('Elizabeth', 'Turner', 2, 14),
    ('Emily', 'Davis', 4, 19),
    ('Emily', 'Davis', 4, 17),
    ('Emily', 'Davis', 1, 14),
    ('Emily', 'Davis', 1, 3),
    ('Emily', 'Davis', 1, 13),
    ('Emily', 'Davis', 1, 11),
    ('Fajar', 'Wibowo', 6, 4),
    ('Fajar', 'Wibowo', 6, 2),
    ('Fajar', 'Wibowo', 6, 12),
    ('Fajar', 'Wibowo', 5, 10),
    ('Fajar', 'Wibowo', 5, 14),
    ('Fajar', 'Wibowo', 5, 6),
    ('Fajar', 'Wibowo', 5, 3),
    ('Isabella', 'Harris', 7, 17),
    ('Isabella', 'Harris', 7, 7),
    ('Isabella', 'Harris', 7, 19),
    ('Isabella', 'Harris', 7, 14),
    ('Isabella', 'Harris', 3, 11),
    ('Isabella', 'Harris', 3, 9),
    ('James', 'Anderson', 2, 12),
    ('Joshua', 'White', 4, 9),
    ('Joshua', 'White', 4, 3),
    ('Joshua', 'White', 4, 10),
    ('Joshua', 'White', 4, 7),
    ('Madison', 'Young', 6, 5),
    ('Madison', 'Young', 6, 2),
    ('Madison', 'Young', 5, 3),
    ('Madison', 'Young', 5, 1),
    ('Madison', 'Young', 1, 16),
    ('Madison', 'Young', 1, 14),
    ('Matthew', 'Nelson', 5, 3),
    ('Matthew', 'Nelson', 5, 8),
    ('Matthew', 'Nelson', 5, 4),
    ('Matthew', 'Nelson', 7, 13),
    ('Matthew', 'Nelson', 7, 7),
    ('Matthew', 'Nelson', 7, 11),
    ('Matthew', 'Nelson', 6, 10),
    ('Matthew', 'Nelson', 6, 12),
    ('Matthew', 'Nelson', 6, 19),
    ('Maya', 'Dewi', 3, 20),
    ('Maya', 'Dewi', 3, 18),
    ('Maya', 'Dewi', 3, 16),
    ('Maya', 'Dewi', 5, 10),
    ('Maya', 'Dewi', 5, 7),
    ('Maya', 'Dewi', 5, 9),
    ('Mia', 'Parker', 2, 8),
    ('Mia', 'Parker', 2, 11),
    ('Mia', 'Parker', 2, 14),
    ('Mia', 'Parker', 2, 10),
    ('Mia', 'Parker', 1, 13),
    ('Mia', 'Parker', 1, 12),
    ('Mia', 'Parker', 1, 2),
    ('Mia', 'Parker', 1, 4),
    ('Nisa', 'Fitriani', 4, 10),
    ('Nisa', 'Fitriani', 4, 11),
    ('Nisa', 'Fitriani', 4, 12),
    ('Nisa', 'Fitriani', 5, 2),
    ('Nisa', 'Fitriani', 5, 1),
    ('Nisa', 'Fitriani', 5, 4),
    ('Nisa', 'Fitriani', 6, 5),
    ('Nisa', 'Fitriani', 6, 7),
    ('Nisa', 'Fitriani', 6, 6),
    ('Olivia', 'Bennett', 4, 5),
    ('Olivia', 'Bennett', 4, 7),
    ('Olivia', 'Bennett', 4, 3),
    ('Olivia', 'Bennett', 5, 10),
    ('Olivia', 'Bennett', 5, 6),
    ('Putri', 'Indah', 7, 20),
    ('Putri', 'Indah', 7, 5),
    ('Putri', 'Indah', 7, 3),
    ('Putri', 'Indah', 2, 7),
    ('Putri', 'Indah', 2, 15),
    ('Putri', 'Indah', 2, 10),
    ('Reza', 'Maulana', 3, 5),
    ('Reza', 'Maulana', 3, 3),
    ('Reza', 'Maulana', 3, 4),
    ('Reza', 'Maulana', 3, 12),
    ('Reza', 'Maulana', 3, 20),
    ('Rizky', 'Pratama', 1, 8),
    ('Rizky', 'Pratama', 1, 10),
    ('Rizky', 'Pratama', 1, 11),
    ('Rizky', 'Pratama', 1, 12),
    ('Rizky', 'Pratama', 4, 13),
    ('Rizky', 'Pratama', 4, 14),
    ('Rizky', 'Pratama', 4, 15),
    ('Rizky', 'Pratama', 4, 17),
    ('Siti', 'Nurhayati', 6, 3),
    ('Siti', 'Nurhayati', 6, 5),
    ('Siti', 'Nurhayati', 6, 6),
    ('Siti', 'Nurhayati', 6, 2),
    ('Sophia', 'Foster', 7, 2),
    ('Sophia', 'Foster', 7, 3),
    ('Sophia', 'Foster', 7, 5),
    ('Sophia', 'Foster', 7, 7),
    ('Sophia', 'Foster', 5, 9),
    ('Sophia', 'Foster', 5, 11),
    ('Sophia', 'Foster', 5, 13),
    ('Tri', 'Wahyuni', 2, 1),
    ('Tri', 'Wahyuni', 2, 3),
    ('Tri', 'Wahyuni', 2, 5),
    ('Tri', 'Wahyuni', 2, 7),
    ('Tri', 'Wahyuni', 2, 9),
    ('Tri', 'Wahyuni', 2, 11),
    ('Yudi', 'Kurniawan', 3, 7),
    ('Yudi', 'Kurniawan', 3, 9),
    ('Yudi', 'Kurniawan', 3, 13),
    ('Yudi', 'Kurniawan', 3, 15),
    ('Yudi', 'Kurniawan', 1, 17),
    ('Yudi', 'Kurniawan', 1, 19),
    ('Yudi', 'Kurniawan', 1, 6),
    ('Yudi', 'Kurniawan', 1, 2);
