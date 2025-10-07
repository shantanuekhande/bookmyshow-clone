from django.db import models
# -------------------
# User / Location / Theatre / Screen / Seat
# -------------------

class User_Type(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    ADMIN = 'admin', 'Admin'


class User(models.Model): # ---------------------------- System/Admin
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10,choices=User_Type.choices)

    def __str__(self):
        return self.username


class Location_Type(models.TextChoices): # ---------------------------- System/Admin
    THEATRE = 'theatre', 'Theatre'
    STADIUM = 'stadium', 'Stadium'
    AUDITORIUM = 'auditorium', 'Auditorium'

class Location(models.Model):# ---------------------------- System/Admin
    name = models.CharField(max_length=100)
    address = models.TextField()
    location_type = models.CharField(max_length=20, choices=Location_Type.choices)

    def __str__(self):
        return self.name


class Theatre(models.Model):# ---------------------------- System/Admin
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Screen_Type(models.TextChoices):# ---------------------------- System/Admin
    TWO_D = '2D', '2D'
    THREE_D = '3D', '3D'
    IMAX = 'IMAX', 'IMAX'

class Screen(models.Model):# ---------------------------- System/Admin
    name = models.CharField(max_length=100)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    seating_capacity = models.IntegerField()
    screen_type = models.CharField(max_length=10, choices=Screen_Type.choices)

    def __str__(self):
        return f"{self.name} - {self.theatre.name}"

class Seat_Type(models.TextChoices):# ---------------------------- System/Admin
    REGULAR = 'regular', 'Regular'
    PREMIUM = 'premium', 'Premium'
    VIP = 'vip', 'VIP'
    RECLINER = "RECLINER", "Recliner"

# seat layout
class Seat(models.Model):# ---------------------------- System/Admin
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    seat_row = models.CharField(max_length=5)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=10, choices=Seat_Type.choices,default=Seat_Type.REGULAR)

    def __str__(self):
        return f"{self.seat_number} - {self.screen.name}"


# -------------------
# Movie / Show / ShowSeat
# -------------------

class Movie_Genre(models.TextChoices):# ---------------------------- System/Admin
    ACTION = 'action', 'Action'
    COMEDY = 'comedy', 'Comedy'
    DRAMA = 'drama', 'Drama'
    HORROR = 'horror', 'Horror'
    ROMANCE = 'romance', 'Romance'
    SCI_FI = 'sci_fi', 'Sci-Fi'
    THRILLER = 'thriller', 'Thriller'
    ANIMATION = 'animation', 'Animation'
    DOCUMENTARY = 'documentary', 'Documentary'
    FANTASY = 'fantasy', 'Fantasy'
    MUSICAL = 'musical', 'Musical'
    WESTERN = 'western', 'Western'
    ADVENTURE = 'adventure', 'Adventure'
    BIOGRAPHY = 'biography', 'Biography'
    CRIME = 'crime', 'Crime'
    FAMILY = 'family', 'Family'
    HISTORY = 'history', 'History'
    MYSTERY = 'mystery', 'Mystery'
    SPORT = 'sport', 'Sport'
    WAR = 'war', 'War'
    OTHER = 'other', 'Other'

class Movies(models.Model):# ---------------------------- System/Admin
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=Movie_Genre.choices)
    duration_minutes = models.IntegerField()
    description = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Show_Status(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class Show(models.Model):# ---------------------------- System/Admin
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Show_Status.choices)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

class show_seat_status(models.TextChoices):# ---------------------------- System/Admin
    AVAILABLE = 'available', 'Available'
    BOOKED = 'booked', 'Booked'
    BLOCKED = 'blocked', 'Blocked'

class Show_Seat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=show_seat_status.choices)

    def __str__(self):
        return f"{self.seat.seat_number} - {self.show.screen.name} ({self.status})"

# -------------------
# User / Booking / Ticket / Payment
# -------------------*

class Booking_Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    COMPLETED = 'completed', 'Completed'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Booking_Status.choices)
    # seats = models.ManyToManyField('Show_Seat') # many reference suggest many to many relationship , but i couldn't understand why thats the reason i used ForeignKey
    seat = models.ForeignKey(Show_Seat, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Booking {self.id} by {self.user.username} for {self.show.movie_name.title}"


class Payment_Method(models.TextChoices):
    CREDIT_CARD = 'credit_card', 'Credit Card'
    DEBIT_CARD = 'debit_card', 'Debit Card'
    NET_BANKING = 'net_banking', 'Net Banking'
    UPI = 'upi', 'UPI'
    WALLET = 'wallet', 'Wallet'
    CASH = 'cash', 'Cash'

class Payment_Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Payment_Method.choices)
    status = models.CharField(max_length=10, choices=Payment_Status.choices)

    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id}"

class Bill(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill {self.id} for Booking {self.booking.id}"

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    issue_time = models.DateTimeField(auto_now_add=True)
    # qr_code = models.CharField(max_length=100)  # In real scenario, this could be an image or a file
    seat = models.ForeignKey(Show_Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Booking_Status.choices)
    # def generate_qr_code(self):
    #     # Placeholder for QR code generation logic
    #     return f"QR-{self.id}"
    # qr_code = models.CharField(max_length=100, default=generate_qr_code)
    # def save(self, *args, **kwargs):
    #     if not self.qr_code:
    #         self.qr_code = self.generate_qr_code()
    #     super().save(*args, **kwargs)


    def __str__(self):
        return f"Ticket {self.id} for Booking {self.booking.id}"



