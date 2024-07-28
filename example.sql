-- Assuming the following table structure:

-- Table: sections
CREATE TABLE sections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table: questions
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    section_id INTEGER REFERENCES sections(id),
    question_type VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL
);

-- SQL Queries:

-- Insert a new section
INSERT INTO sections (name) VALUES ('Needs');

-- Insert a new question linked to a section (assuming section with id=1 is "Needs")
INSERT INTO questions (section_id, question_type, question_text) VALUES (1, 'single-choice', 'What is the primary reason for your purchase?');

-- Retrieve all questions for a specific section
SELECT q.* FROM questions q
JOIN sections s ON q.section_id = s.id
WHERE s.name = 'Needs';

-- Update a question text based on question id
UPDATE questions SET question_text = 'What is your main goal with this purchase?' WHERE id = 1;

-- Delete a question
DELETE FROM questions WHERE id = 1;

-- Delete a section and its associated questions
DELETE FROM questions WHERE section_id = 1;
DELETE FROM sections WHERE id = 1;