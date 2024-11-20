# Tiko Task

Tiko Test is a Django-based project designed to manage events and user profiles.

## Key Technologies Used
- **Python3.10**: python version.
- **Django-Restframework**: For writing APIs.
- **Django-Pytest**: For writing tests.
- **JWT**: For authentication.
- **Swagger**: For documenting API endpoints.

## Getting Started

### Prerequisites

Make sure you have Python 3.10 installed on your system.

### Installation and details 

1. **Clone the repository**:
   ```sh
   git clone <url>
   cd tiko-test

2. **Install the required packages**:
    ```sh
   pip install -r requirements.txt

3. **Run migrations to set up the database**:
    ```sh
   python manage.py makemigrations events user_profile
   python manage.py migrate
   
4. **Running the Server**:
    ```sh
   python manage.py runserver

5. **API Endpoints**:

    **Events**
- <server_ip>/event/create/
- <server_ip>/event/all/
- <server_ip>/event/user/
- <server_ip>/event/update/<event_id>/
- <server_ip>/event/register/<event_id>/
- <server_ip>/event/unregister/<event_id>/

    **User**
- <server_ip>/user/register/


6. **API Documentation Endpoints**:

- <server_ip>/swagger/
- <server_ip>/redoc/

7. **Run all tests**:

Few test been introduced, to give idea about writing tests 
   ```sh
   pytest 
   ```
8. **Docker**:

Docker file is available you can build and run the docker from following commands. And access the server directly
   ```sh
   docker build -t tiko_test .
   docker run -p 8000:8000 tiko_test
   ```
To access docker by command line
   ```sh
   docker exec -it <container_id_or_name> /bin/bash
   ```
9. **Postman collection**:

Postman collection has been added into the project, you can use it by importing it in the postman. 
Before using make sure you adjust the **environment variables**.
