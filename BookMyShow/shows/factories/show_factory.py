from datetime import timedelta
from ..models import Show, ShowSeat , Status

class ShowFactory:
    @staticmethod
    def create_show(movie, screen, start_time, base_price, offer=None):
        """
        Factory responsible for creating a Show and its associated ShowSeats.
        """

        # 1. Compute end time
        end_time = start_time + timedelta(minutes=movie.duration_minutes)

        # 2. Create show
        show = Show.objects.create(
            movie=movie,
            screen=screen,
            start_time=start_time,
            end_time=end_time,
            base_price=base_price,
            offer=offer
        )

        # 3. Generate seats
        show_seats = []
        for screen_seat in screen.seats.all():
            price_multiplier = ShowFactory._get_multiplier(screen_seat.seat_type)

            show_seats.append(
                ShowSeat(
                    show=show,
                    seat=screen_seat,
                    price=base_price * price_multiplier,
                    status=Status.AVAILABLE
                )
            )

        ShowSeat.objects.bulk_create(show_seats)
        return show

    @staticmethod
    def _get_multiplier(seat_type):
        """
        Define seat type multipliers.
        """
        multipliers = {
            'REGULAR': 1.0,
            'PREMIUM': 1.2,
            'RECLINER': 1.5
        }
        return multipliers.get(seat_type.upper(), 1.0)
