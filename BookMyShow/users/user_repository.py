from .models import User

class UserRepository:
    @staticmethod
    def get_by_email(email):
        return User.objects.filter(email=email).first()

    @staticmethod
    def create_user(email, password, role):
        user = User(email=email, username=email, role=role)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_all_users():
        return User.objects.all()

class UserRepository:
    @staticmethod
    def get_by_email(email):
        """
        Returns User object if email exists, else None
        """
        return User.objects.filter(email=email).first()



    @staticmethod
    def create_user(email, password, role):
        """
        Creates and saves a new user
        """
        user = User(email=email, username=email, role=role)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_by_id(user_id):
        """
        Returns User object if id exists, else None
        """
        return User.objects.filter(id=user_id).first()

    @ staticmethod
    def get_all_users():
        """
        Returns all users
        """
        return User.objects.all()

