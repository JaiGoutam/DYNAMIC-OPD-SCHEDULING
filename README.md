# DYNAMIC-OPD-SCHEDULING
This GitHub repository hosts a robust and user-friendly appointment booking system developed using Django, HTML, CSS, and JavaScript. The system is designed to streamline the process of scheduling appointments for healthcare services, ensuring a dynamic and efficient experience for both patients and healthcare providers.
Dynamic and Time-Saving Appointment Booking System
This project implements a dynamic and time-saving appointment booking system using Django, HTML, CSS, and JavaScript. The system is designed to streamline the process of scheduling appointments for healthcare services, making it easier for both patients and healthcare providers.

Key Features
User-Friendly Interface: An intuitive and responsive interface allows patients to easily schedule appointments by selecting the desired date, location, and entering their health information.

Location Selection: Patients can choose from multiple locations, providing flexibility and convenience for selecting the nearest healthcare facility.

Health Information Entry: Fields for temperature, heart rate, symptoms, and primary complaints ensure healthcare providers are prepared for the appointment and can provide timely care.

Symptom Checkbox: Checkbox options for common symptoms like cough, body pain, and headache allow patients to quickly communicate additional health concerns, saving time during the appointment.

Special Considerations: Additional checkbox for female patients to indicate pregnancy status ensures healthcare providers are fully informed for tailored care.

Follow-up Appointments: Patients can indicate if the appointment is a follow-up, aiding in planning future care and scheduling subsequent visits.

Consent Checkbox: A mandatory consent checkbox ensures patients acknowledge and agree to the terms and conditions of the appointment booking.

Validation and Error Handling: Client-side validation ensures all required fields are filled before submission, preventing errors and ensuring smooth data submission.

Technologies Used
Django: Backend framework for handling requests, processing data, and interacting with the database.

HTML/CSS: Frontend structure and styling for a clean and modern interface.

JavaScript: Enhances user interactivity, performs client-side validation, and integrates with Chart.js for dynamic charts.

Chart.js: Displays visual data representations of appointment statistics, offering insights into doctor performance metrics.

Installation


Clone the repository:
git clone <repository_url>
cd appointment-booking-system


Install dependencies:
pip install -r requirements.txt


Apply database migrations:
python manage.py migrate


Start the development server:
python manage.py runserver


Access the application at http://localhost:8000/.

Acknowledgments
Thanks to the Django community for providing robust tools and resources.
Chart.js for providing a simple yet flexible JavaScript charting library.
HTML5 Boilerplate and Bootstrap for the frontend templates and styles.
