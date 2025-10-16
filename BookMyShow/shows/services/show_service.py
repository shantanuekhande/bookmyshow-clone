# apps/show/services/show_service.py

from django.db import transaction
from django.utils import timezone
from ..factories.show_factory import ShowFactory
from ..models import Show, Screen ,Movie
from datetime import timedelta

class ShowService:
    """
    Service class to handle show-related operations.
    """

    @staticmethod
    @transaction.atomic
    def create_show(movie_id, screen_id, start_time, base_price, offer=None):
        """
        Creates a new show after performing validation.
        """

        # 1. Validate existence of movie and screen
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValueError("Invalid movie_id")

        try:
            screen = Screen.objects.get(id=screen_id)
        except Screen.DoesNotExist:
            raise ValueError("Invalid screen_id")

        # 2. Validate start_time
        if start_time < timezone.now():
            raise ValueError("Start time cannot be in the past")

        # 3. Check for overlapping shows on the same screen
        overlapping = Show.objects.filter(
            screen=screen,
            start_time__lt=start_time + timedelta(minutes=movie.duration_minutes),
            end_time__gt=start_time
        ).exists()
        if overlapping:
            raise ValueError("Screen already has a show during this time")

        # 4. Delegate creation to factory
        show = ShowFactory.create_show(
            movie=movie,
            screen=screen,
            start_time=start_time,
            base_price=base_price,
            offer=offer
        )

        return show
