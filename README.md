To Run: 
Create an account for geoapify:https://myprojects.geoapify.com/register
and tollguru:https://platforms.mapup.ai/login?flow=signup&appState=eyJmbG93Ijoic3NvIiwicmVkaXJlY3RfdXJpIjoiaHR0cHM6Ly90b2xsZ3VydS5jb20vYXV0aGVudGljYXRlIiwiYXBwbGljYXRpb24iOiJ0b2xsZ3VydV93ZWIiLCAibmV4dCI6ICIvZGFzaGJvYXJkP3Byb2R1Y3Q9MSJ9

Get API Keys and create a .env file in root directory with the following three variables defined:
SECRET_KEY=  
GEOAPIFY_API_KEY=  
TOLLGURU_API_KEY=  

To get secret key open up a Python shell and run the following commands: 
```
import secrets
secret_key = secrets.token_hex(32)
```

Paste API keys and secret key into .env.

Install requirements using `pip install -r requirements.txt`.

Run app.py using `python app.py`.


