# apps/users/controllers/user_controller.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from ..services.user_service import UserService
from ..serializers import UserSerializer, UserLoginSerializer


class UserController(ViewSet):
    user_service = UserService()

    # ========================= REGISTER =========================
    @swagger_auto_schema(
        method='post',
        request_body=UserSerializer,
        responses={
            201: "User created successfully",
            400: "Invalid data"
        }
    )
    @action(detail=False, methods=["post"])
    def register(self, request):
        """
        POST /api/users/register/
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data.get("email")
        password = data.get("password")
        role_name = data.get("role", "CUSTOMER")

        try:
            user = self.user_service.register_user(email=email, password=password, role=role_name)
            return Response(
                {"user_id": user.id, "email": user.email},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    # ========================= LOGIN =========================
    @swagger_auto_schema(
        method='post',
        request_body=UserLoginSerializer,
        responses={
            200: "Login successful",
            400: "Invalid credentials"
        }
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        POST /api/users/login/
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data.get("email")
        password = data.get("password")

        try:
            user = self.user_service.authenticate_user(email=email, password=password)
            return Response(
                {"user_id": user.id, "email": user.email},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
