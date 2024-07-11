Feature: patient book an appointment
  patient receives a list of available appointment times and books one

  Scenario: successfully book an appointment for today
        Given the practitioner schedule is filled with some appointments
        When the patient books a standard appointment for an available time slot
        Then the practitioner can see the new standard appointment on their schedule for that patient

  Scenario: failure on booking an appointment for today
        Given the practitioner schedule is filled with some appointments in the morning
        When the patient books a initial appointment for an unavailable time slot
        Then the appointment is not added to the schedule of the practitioner


