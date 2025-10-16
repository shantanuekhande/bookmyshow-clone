# # apps/show/controllers/show_controller.py
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from ..serializers.show_serializer import ShowCreateSerializer
# from ..services.show_service import ShowService
#
# class ShowCreateView(APIView):
#     """
#     API endpoint to create a new Show.
#     """
#
#     @swagger_auto_schema(
#         operation_summary="Create a new show",
#         operation_description="Admin can create a show by providing movie_id, screen_id, start_time, and base_price.",
#         request_body=ShowCreateSerializer,
#         responses={
#             201: openapi.Response('Show created successfully'),
#             400: openapi.Response('Invalid input data')
#         }
#     )
#     def post(self, request):
#         serializer = ShowCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             try:
#                 show = ShowService.create_show(**data)
#                 return Response({"message": "Show created successfully", "show_id": show.id}, status=status.HTTP_201_CREATED)
#             except ValueError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# apps/show/controllers/show_controller.py
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.show_serializer import ShowCreateSerializer
from ..services.show_service import ShowService

class ShowController(ViewSet):
    service = ShowService()

    @swagger_auto_schema(
        operation_summary="Create a new show",
        operation_description="Admin can create a show by providing movie, screen, start_time, base_price, and optional offer.",
        request_body=ShowCreateSerializer,
        responses={
            201: openapi.Response('Show created successfully', ShowCreateSerializer),
            400: 'Invalid input data'
        }
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_show(self, request):
        serializer = ShowCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            show = self.service.create_show(
                movie_id=data['movie'].id,
                screen_id=data['screen'].id,
                start_time=data['start_time'],
                base_price=data['base_price'],
                offer=data.get('offer')
            )

            return Response(
                {
                    "id": show.id,
                    "movie": show.movie.title,
                    "screen": show.screen.name,
                    "start_time": show.start_time,
                    "end_time": show.end_time,
                    "base_price": str(show.base_price)
                },
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
