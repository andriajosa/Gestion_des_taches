DB_CONFIG = {
    "host" : "localhost",
    "user" : "root",
    "password" : "",
    "database" : "todolist" 
}

JWT_SECRET_KEY = "cle_secrete_to_do_list"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 1

# Cle Fernet utilisee pour chiffrer les descriptions des taches.
# Generee une seule fois avec :
#   from cryptography.fernet import Fernet
#   print(Fernet.generate_key())
FERNET_KEY = b"KfN2z1sB8h8T2f0uQeYV3rW1lM9pXeD6cGZbA0oV8qE="

API_HOST = "127.0.0.1"
API_PORT = 5000