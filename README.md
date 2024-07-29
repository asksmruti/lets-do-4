# HPS Platform

The objective of this repository is to fulfil the following requirement -

1. Sketch out an architecture diagram, showing the main components of the digital web-based HPS product. Indicate how the components
   communicate with each other and what architectural style are being used/followed. Create a basic RESTful API endpoint (including some unit tests)
   for at least one of the components.
2. Design and diagram an underlying unified data model / database(s) to be used to store, analyze and modify the primary data. Write sample SQL
   queries to retrieve specific data from this database.
3. Define the relevant technical specifications and set of technologies that would be used to address the following operational aspects:
   <br>
   ❑ Extract data from different data sources, Transform it to the underlying data model, then Load it to the desired storage location. <br>
   ❑ Dealing with structured and unstructured data sources.<br>
   ❑ Scalability in order to process & serve behavioral data of billions of customers worldwide.<br>
   ❑ Support of various trigger mechanisms that would invoke data extraction and ingestion.
   </br>
4. Define what kind of technologies/platforms/tools should be used with or integrated into the application. Consider here also peripheral aspects such
   as observability and data quality.
5. List challenges/concerns that you see and indicate how you think they should be approached and resolved.
6. Calculate the total number of cups of coffee that the HPS product team consumes each sprint. Explain how you arrived at your answer.

# Survey Template Application (Requirement #1)

I believe the HPS platform serves as a tool for collecting data on the consumer's shopping journey through surveys. Nevertheless, there are numerous methods for documenting different sentiments and actions of consumers when they shop online. Particularly on the shopping website, it's possible to collect information on user activity and transaction specifics.

## Getting Started
This repository contains the source code for a Proof of Concept (PoC) survey template application. It demonstrates how to set up, run, and interact with a simple survey application using Python and FastAPI along with the design diagram.

## Solution Design

The solution has two interfaces admin and non-admin. Following is the flow diagram for both type of users.

- Admin flow diagram

![](images/admin-flow-diagram.png?raw=true)

- Consumer flow diagram

![](images/consumer-survey-flow-diagram.png?raw=true)

- Solution Design

![](images/HPS-solution-design.png?raw=true)



Follow these instructions to get the application running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10.14

### Installation

1. **Set up Python environment**:

First, install Python 3.10.14 and set up a virtual environment:

```bash
pyenv install 3.10.14
pyenv virtualenv 3.10.14 dev
pyenv local dev
```

2. **Install dependencies**:

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

### Running the Application

To run the application, execute:

```bash
python run.py

INFO:     Uvicorn running on http://127.0.0.1:4000 (Press CTRL+C to quit)
INFO:     Started reloader process [59706] using WatchFiles
INFO:     Started server process [59758]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Interacting with the Application

- #### API Documentation:
  - Access the interactive API documentation by navigating to: http://127.0.0.1:4000/docs
  - For Swagger UI: http://127.0.0.1:4000/docs

You can update the survey template using the following `curl` command:

```bash
curl -X PUT http://127.0.0.1:4000/update-section/Needs \
-H "Content-Type: application/json" \
-d '{
  "section": "Needs",
  "questions": [
    {
      "type": "multi-choice",
      "question": "What is the primary reason for your purchase?",
      "options": ["Replacement", "Upgrade", "Remodel", "Gift"]
    }
  ]
}'
```

- #### Example Running Instance:

An example of the running instance can be found at:

https://overall-clownfish-asksmruti-88d0204a.koyeb.app/survey

https://overall-clownfish-asksmruti-88d0204a.koyeb.app/docs

![](images/SwaggerAPI.png?raw=true)

### Running Tests

Execute the unit tests (both positive and negative scenarios) using:

`pytest test_main.py`

```bash
======================================================================= short test summary info ========================================================================
FAILED test_main.py::test_update_section - assert 500 == 200
FAILED test_main.py::test_delete_question - assert 404 == 200
FAILED test_main.py::test_add_question - assert 422 == 201
FAILED test_main.py::test_update_question - assert 422 == 200
==================================================================== 4 failed, 6 passed in 0.93s ======================================================================
```

# Survey Table Data Model (Requirement #2)

![](images/ER-diagram.png?raw=true)

# Survey Database Sample SQL Queries (Requirement #3)

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

# Data pipeline technology landscape (Requirement #4)

![](images/data-pipeline-technology-landscape.png?raw=true)

### Elements of a Data Pipeline:

- Data Source: Determine the various data sources, which may include databases, APIs, logs, and external streams.

- Data Processing: This phase has multiple steps
  - Data Transformation: This phase focuses on cleaning, enhancing, and converting raw data into a structured format.
  - Data Movement: Efficiently transfer data between different storage options and services w
  - Data Loading: Load the transformed data into its final destination, which might be Azure SQL Data Warehouse, Azure Synapse Analytics, or other database systems.

- Orchestration: Use tools like Azure Logic Apps or Apache Airflow to orchestrate the entire pipeline, ensuring that all steps are carried out in the correct sequence.

- Data Security and Compliance: Safeguard sensitive data both at rest and in transit. Azure Key Vault for secure key and secret management.

- Data Quality Check: Great Expectation open source platform can be used to do quality check.

- Data Storage: Data can be stored in Azure Datalake storage

- Monitoring and Logging: Establish comprehensive monitoring and logging through Azure Monitor and Azure Log Analytics to oversee pipeline performance and identify potential issues.

- Data Partitioning: For large datasets, implement partitioning strategies to improve data storage and retrieval efficiency.

Preferred architecture - _Kappa Architecture_ as this  easy to maintain and implement, unified codebase, real-time processing capabilities, cost-effectiveness, scalability, and reduced redundancy, fast and efficient data processing and analysis.

# Challenges (Requirement #5)

- The requirement could be more elaborative and some examples could be given

- The data model would be more complex when we will learn the complexity of data

- Real time data or historical data? Realtime data would be costly depending how much data but I presume if we track the user data on real time then it would be expensive. Therefore we need to understand what value this will bring for the growth of organisation.

# Coffee cups (Requirement #6)

Coffee cups can be determined by doing a team survey however the below numbers are completely based on assumption.

Assuming everyone in the team consume coffee

Here is a rough estimation

```
2Cups / Person / Day
1 Sprint = 2 Weeks = 10 Working Days
2 Cups/ x 10 Days x (2 FE + 2 BE + 4 DE + 2 DevOps + 1 PO) = 220 Cups
```
