
from src.database.db import get_connection
from src.utils.errors.CustomException import CustomException
from .models.User import User


class AuthService():

    @classmethod
    def login_user(cls, users):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_user, username, password, email FROM users WHERE username = %s', (users.username,))
                row = cursor.fetchone()
                if row is not None:
                    user_id, username, stored_password, email = row
                    # Compara la contraseña proporcionada con la almacenada (hashed)
                    if cls.verify_password(users.password, stored_password):
                        authenticated_user = User(int(user_id), username, None, email)
            connection.close()
            return authenticated_user
        except Exception as ex:
            raise CustomException(ex)

    @staticmethod
    def verify_password(provided_password, stored_password):
        # Aquí asumimos que stored_password es un hash
      
        return provided_password == stored_password
