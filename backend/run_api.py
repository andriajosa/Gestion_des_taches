from API.app import creer_application
from config.settings import API_HOST, API_PORT

if __name__ == "__main__":
    application = creer_application()
    application.run(host=API_HOST, port=API_PORT, debug=True)