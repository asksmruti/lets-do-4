# Survey Database Sample SQL Queries

This document provides a set of SQL queries for managing a survey database based on the previously defined data model. It serves as a reference to create tables, insert data, retrieve information, update records, and delete entries in the survey system database.

## Table of Contents

- [Creating Tables](#creating-tables)
- [Inserting Data](#inserting-data)
- [Retrieving Data](#retrieving-data)
- [Updating Data](#updating-data)
- [Deleting Data](#deleting-data)


## Creating Tables

The following SQL statements are used to create tables that constitute the survey data model.

### SurveySections Table

Stores information on different sections of the survey.

```sql
CREATE TABLE SurveySections (
  SectionID INT AUTO_INCREMENT PRIMARY KEY,
  SectionName VARCHAR(255) NOT NULL
);
```

### QuestionTypes Table

Defines the types of questions used in the survey. 

```sql
CREATE TABLE QuestionTypes (
  QuestionTypeID INT AUTO_INCREMENT PRIMARY KEY,
  TypeName VARCHAR(255) NOT NULL
);
```
### Questions Table

Contains questions that are part of the survey, each related to a section and question type.

```sql
CREATE TABLE Questions (
  QuestionID INT AUTO_INCREMENT PRIMARY KEY,
  SectionID INT,
  QuestionTypeID INT,
  QuestionText VARCHAR(255) NOT NULL,
  FOREIGN KEY (SectionID) REFERENCES SurveySections(SectionID),
  FOREIGN KEY (QuestionTypeID) REFERENCES QuestionTypes(QuestionTypeID)
);
```
### QuestionOptions Table
Stores possible answer options for the questions in the survey.

```sql
CREATE TABLE QuestionOptions (
  OptionID INT AUTO_INCREMENT PRIMARY KEY,
  QuestionID INT,
  OptionValue VARCHAR(255) NOT NULL,
  FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID)
);
```

## Inserting Data

Populate the tables with initial data necessary for the survey application.

```sql
-- Insert SurveySections data
INSERT INTO SurveySections (SectionName) VALUES ('Needs');
INSERT INTO SurveySections (SectionName) VALUES ('Product Clusters');
INSERT INTO SurveySections (SectionName) VALUES ('Triggers');
-- Add more sections as needed
-- Insert QuestionTypes data
INSERT INTO QuestionTypes (TypeName) VALUES ('multi-choice');
INSERT INTO QuestionTypes (TypeName) VALUES ('multiple-choice');
INSERT INTO QuestionTypes (TypeName) VALUES ('single-choice');
-- Add more question types as needed
-- Insert Questions data
INSERT INTO Questions (SectionID, QuestionTypeID, QuestionText) VALUES (1, 1, 'What is the primary reason for your purchase?');
-- Add more questions linking to SectionID and QuestionTypeID as needed
-- Insert QuestionOptions data
INSERT INTO QuestionOptions (QuestionID, OptionValue) VALUES (1, 'Replacement');
INSERT INTO QuestionOptions (QuestionID, OptionValue) VALUES (1, 'Upgrade');
INSERT INTO QuestionOptions (QuestionID, OptionValue) VALUES (1, 'Remodel');
-- Add more options as needed
```

## Retrieving Data

Use the following queries to read data from the survey database.


```sql
-- Get all questions from a specific section
SELECT q.QuestionText
FROM Questions q
JOIN SurveySections s ON q.SectionID = s.SectionID
WHERE s.SectionName = 'Needs';
-- Get all question types
SELECT TypeName
FROM QuestionTypes;
-- Get all options for a specific question
SELECT o.OptionValue
FROM QuestionOptions o
JOIN Questions q ON o.QuestionID = q.QuestionID
WHERE q.QuestionText = 'What is the primary reason for your purchase?';
```

## Updating Data

```sql
-- Update a question text
UPDATE Questions
SET QuestionText = 'What is the main reason for your purchase?'
WHERE QuestionID = 1;
-- Update an option value
UPDATE QuestionOptions
SET OptionValue = 'Home Remodeling'
WHERE OptionID = 3 AND QuestionID = 1;
Deleting Data
-- Delete a question option
DELETE FROM QuestionOptions
WHERE OptionID = 3;
-- Delete a question
DELETE FROM Questions
WHERE QuestionID = 1;
```
