from django.db import models

# Create your models here.

class Location(models.Model):
    name  = models.CharField(max_length=100)
    city  = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    total_screens = models.IntegerField()
    total_seats = models.IntegerField()
    amenities = models.TextField(blank=True, null=True)  # e.g., "3D, IMAX, Dolby Atmos"

    def __str__(self):
        return self.name

class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # e.g., "Screen 1"
    total_seats = models.IntegerField()
    screen_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., "IMAX", "3D"

    def __str__(self):
        return f"{self.theater.name} - {self.name}"

class Seat(models.Model):
    class SeatType(models.TextChoices):
        REGULAR = 'regular', 'Regular'
        PREMIUM = 'premium', 'Premium'
        RECLINER = 'recliner', 'Recliner'

    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="seats")
    row = models.CharField(max_length=5)
    number = models.IntegerField()
    seat_type = models.CharField(max_length=20, choices=SeatType.choices, default=SeatType.REGULAR)

    def __str__(self):
        return f"{self.row}{self.number} ({self.seat_type}) - {self.screen.name}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    language = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return self.title


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="shows")
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="shows")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    offer = models.CharField(max_length=100, blank=True, null=True)  # e.g., "10% off"

    def __str__(self):
        return f"{self.movie.title} - {self.screen.name} at {self.start_time}"

class Status(models.TextChoices):
     AVAILABLE = 'available', 'Available'
     LOCKED = 'locked', 'Locked'
     BOOKED = 'booked', 'Booked'

class ShowSeat(models.Model):

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="show_seats")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.seat} - {self.show} - {self.status}"

