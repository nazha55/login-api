Project API Documentation
This project includes all the essential APIs related to user authentication. The APIs are implemented in the login.py file.

APIs
Signup API: Allows users to create a new account.
Signin API: Allows users to log in to their accounts.
Forget Password API: Allows users to reset their forgotten passwords.
Request OTP API: Allows users to request a one-time password for authentication.
All of these APIs are implemented within the login.py file.

requirements.py File
The requirements.py file contains the Python installations and dependencies required for this project. Make sure to install the necessary packages using the following command:

pip install -r requirements.txt

## How to Run the Application

Run the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload

Open your browser and navigate to the Swagger UI for API documentation:
http://127.0.0.1:8000/docs
