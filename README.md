# Women-s-Safety-

## Overview

The Women Safety System is a Django-based web application designed to enhance the safety of women in various scenarios.

## Features

- **Emergency Alerts**: Quickly send alerts to registered contacts.
- **Emergency Button**: Initiates calls to saved contacts when clicked, providing a quick response mechanism in emergencies.
- **Location Sharing**: Share your real-time location with trusted contacts.
- **Safety Resources**: Access a variety of safety tips and resources.
- **User Authentication**: Secure login and registration for users.

## Requirements For Run The Project

Before running the project, ensure you have the following installed:

- Python 3.x
- Django 4.x or higher
- Django REST framework 
- A database (SQLite, PostgreSQL, etc.)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Abhaysinh031/Women-Safety-System.git
   cd Women-Safety-System

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```
   
4. **Set up the database**:
    - For SQLite, no additional setup is required.
    - For PostgreSQL or other databases, ensure you have the database created and configure the DATABASES setting in settings.py.
  
5. **Run migrations**:
   ```bash
   python manage.py migrate
  

## Running The Project :
1. **Start the development server**:
  ```bash
  python manage.py runserver
```

2. **Access the application:**
   Open your web browser and go to http://127.0.0.1:8000/.


## Usage

- User Registration: Sign up to create an account.
- Emergency Alerts: Use the designated feature to send alerts.
- Access Resources: Navigate to the resources section for safety tips.


 ## Contact
For any inquiries, please reach out to abhysihdes031@gmail.com.



