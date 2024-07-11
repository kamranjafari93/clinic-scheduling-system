# Clinic Scheduling System

This application implements the core components of an on-line scheduling system for a physiotherapy clinic. 
The application includes a set of unit tests. It does not include any database, console application or GUI.
The clinic has the following business rules:

- The clinic is open from 9am until 5pm.
- The clinic offers three types of appointments, a 90 minutes initial consultation, standard 60 minute appointments and 30 minute check-ins.
- Appointments do not overlap. There can only be one booked appointment at any time.
- Appointments start on the hour or half-hour.
- Bookings can only be made for appointments that start and end within the clinic hours.
- Bookings cannot be made within 2 hours of the appointment start time.

## The application MVP will:

Provide the patient with a list of available appointment times. Inputs are the appointment type and a date, either today or in the future. The 2 hour booking deadline applies for today’s appointments.
Allow the patient to book an appointment.
Provide the practitioner with a list of scheduled appointments for the current day.

## Prerequisites
- Docker installed on your system
- Python 3 installed on your system
- pip installed on your system

## Setup Instructions
1. **Configure Environment Variables**:
   - Copy the `.env.example` file and rename it to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your configuration settings.
2. **Configure Virtual Environment**
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```
   - Install Dependencies:
     ```bash
     pip install -r requirements-venv.txt
     ```
   - Install pre-commit:
     ```bash
     pre-commit install
     ```
   
## Running the Project
- To build and start the Docker container, run the following command:
  ```bash
  docker-compose up -d --build
  ```
- Access the shell of the Docker container by:
  ```bash
  docker exec -it app-kamranjafari sh
  ```
## Test Cases ##

This project utilizes 4 different types of testing:

- **Static Testing**: By using <u>mypy</u> and <u>pylint</u> as pre-commit hooks, static type checking and adherence to PEP8 rules are enforced. 
- **Unit Testing**: By Implementing test cases for each individual function and method using <u>pytest</u>.
- **Integration Testing**: By implementing test cases that require interaction between several functions and classes  using <u>pytest</u>.
- **Behavior (Feature) Testing**: By implementing scenario-based test cases using <u>pytest-bdd</u>.

To run the test cases, enter the following command inside the Docker container shell and in the root of the project:
  ```bash
  python3 -m pytest -v -s --cov=src --cov-report=html 
  ```
This command executes all the test cases and also displays the code test coverage.

## Assumptions ##

Here are the assumptions for implementing this project:
- In this scheduling system, time zones play a pivotal role. It is assumed that all dates and times are based on the **America/Vancouver** time zone.
- The Clinic model is not extensively involved, as the MVP goals do not directly pertain to it. However, the relationship between the Clinic and Practitioner models is implemented.
- More **Behavior Tests** could be added to achieve better coverage; however, this project currently includes only the essential ones.


