Feature: book an appointment
  check different scenarios for booking an appointment

  Scenario: successfully book an appointment for tomorrow 9am
        Given the practitioner schedule is empty for tomorrow 9am standard appointment
        When the patient books a standard appointment for a tomorrow 9am
        Then the practitioner can see the new standard appointment on their schedule for tomorrow 9am

  Scenario: failure on booking an appointment for tomorrow 9am
        Given the practitioner has an initial appointment for tomorrow 9am
        When the patient tries booking a standard appointment for a tomorrow 9am
        Then the practitioner see the old initial appointment on their schedule for tomorrow 9am


