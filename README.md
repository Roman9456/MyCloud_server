# MyCloud Backend

## Overview

This project is the backend of [MyCloud](https://github.com/Roman9456/MyCloud), a cloud storage application built with Django and Django REST Framework. The backend handles user authentication, file management, and provides a REST API for interacting with the cloud storage. It supports PostgreSQL for data storage and includes built-in CORS support for cross-origin requests.

## Requirements

To get started, you need to have the following installed:

- Python 3.x
- PostgreSQL
- `pip` (Python package installer)
- `virtualenv` (recommended for creating isolated environments)

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/Roman9456/MyCloud_server.gitl>
cd MyCloud_server
```

### 2. Set up a virtual environment 
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate 
``` 
### 3. Install dependencies 
```bash
pip install -r requirements.txt
``` 
### 4. Set up environment variables  
 - Create a .env file at the root of the project and set the following variables: 
 ```makefile 
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_DB_NAME=mycloud_db
DJANGO_DB_USER=your_db_user
DJANGO_DB_PASSWORD=your_db_password
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:5173 
``` 
 - Note: Make sure to replace the placeholder values with your actual credentials and configuration.  

 ### 5. Run database migrations 
 After setting up the .env file, run the following command to apply database migrations: 
 ```bash
pip python manage.py migrate  
``` 
### 6. Create a superuser (optional) 
To access the Django admin panel, create a superuser: 
 ```bash
python manage.py createsuperuser  
```   

### 7. Run the development server 
Now you can run the development server:
 ```bash
python manage.py runserver 
```   
The application will be accessible at http://127.0.0.1:8000. 

## Configuration Details 
### Logging 
 - Logging is set up to provide console output with different log levels for various components of the project. The logs will be visible in the console when running the application. 
 ## CORS Configuration 
 - Cross-Origin Resource Sharing (CORS) is configured to allow requests from specified origins, such as http://localhost:5173 (for the frontend development environment). You can add more origins to the CORS_ALLOWED_ORIGINS environment variable.
 ## Database Configuration
 - The backend uses PostgreSQL for database storage. Configure the database connection in the .env file by providing the database name, user, password, host, and port. 
## REST API Configuration
The backend is built using Django REST Framework and provides the following features:

 - Authentication: Custom authentication class NoExpirationTokenAuthentication for API token authentication.
 - Permissions: The API is configured with the permission class AllowAny, but you can change it to IsAuthenticated to restrict access.
 - Search and Ordering: Built-in support for filtering, searching, and ordering API results.
 - Custom Error Handling: A custom exception handler is used for better error reporting. 
## Static and Media Files
 - Static files (CSS, JS, images) are served from the /static/ URL path and stored in the staticfiles directory.
Media files (uploaded files) are served from the /media/ URL path and stored in the media directory. 

## Admin Panel 
 - Once you have created a superuser, you can access the Django Admin panel at http://127.0.0.1:8000/admin/. 

## Custom User Model
 - This project uses a custom user model called UserProfile from the mycloud_api app for user authentication and management. 

 ## Production Deployment
 - For deploying the application in production, follow these additional steps:

1. Set DEBUG=False in the .env file.
2. Configure a production-ready PostgreSQL instance.
3. Use a web server like Gunicorn and a reverse proxy like Nginx for handling production traffic.
4. Set up SSL for secure communication.
5. Use a cloud service like AWS or DigitalOcean for hosting.

## License
This project is licensed under the MIT License - see the LICENSE file for details.







 

    



 


