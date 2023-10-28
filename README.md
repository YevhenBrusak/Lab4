# Lab 4

It is a secure password management system that enforces password policies, implements user registration and login functionality, and offers additional security features.

## Features
* User registration and login
* Password policy enforcement:
* Minimum length of 8 characters
* At least one uppercase letter
* At least one lowercase letter
* At least one digit
* At least one special character (non-letter and non-digit)
* Passwords are securely hashed for storage
* User authentication based on hash equality
* Limit on consecutive failed login attempts
* CAPTCHA mechanism to protect against bots during registration
* Optional two-factor authentication (2FA) implementation

##  Notes
The requirements.txt file should list all Python libraries that your notebooks depend on, and they will be installed using:
```
pip install -r requirements.txt

```
