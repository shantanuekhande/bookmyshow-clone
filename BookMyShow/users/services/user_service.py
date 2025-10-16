from django.contrib.auth import authenticate
from ..models import Role, User
from ..user_repository import UserRepository


class UserService:
    def register_user(self, email, password, role = Role.CUSTOMER):
        """
        Creates a new user using email as username.
        """
        # Step 1: check if user exists
        if UserRepository.get_by_email(email):
            raise ValueError("User with this email already exists")

        # create role object
        role  = role.lower()
        # Step 2: validate role
        if role == 'admin':
            role = Role.ADMIN
        elif role == 'customer':
            role = Role.CUSTOMER
        else:
            raise ValueError("Invalid role")

        # Step 3: create user
        user  = UserRepository.create_user(email, password, role)
        return user


    def authenticate_user(self, email, password):
        """
        Authenticate using email + password
        """
        user = authenticate(username=email, password=password)
        if not user:
            raise ValueError("Invalid credentials")
        return user
