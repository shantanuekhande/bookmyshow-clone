from django.contrib import admin
from .models import (
    Location, Theater, Screen, Seat,
    Movie, Show, ShowSeat
)

# 🏙 Location
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "country", "zip_code")
    search_fields = ("name", "city", "state", "country")


# 🎭 Theater
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ("name", "city_name", "total_screens", "total_seats")
    search_fields = ("name", "location__city")

    def city_name(self, obj):
        return obj.location.city
    city_name.short_description = "City"


# 🎬 Screen
class SeatInline(admin.TabularInline):
    model = Seat
    extra = 5  # how many seats to show by default
    fields = ("row", "number", "seat_type")
    show_change_link = True


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ("name", "theater_name", "total_seats", "screen_type")
    list_filter = ("screen_type", "theater__location__city")
    search_fields = ("name", "theater__name")
    inlines = [SeatInline]

    def theater_name(self, obj):
        return obj.theater.name
    theater_name.short_description = "Theater"


# 🎟 Seat
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("screen", "row", "number", "seat_type")
    list_filter = ("seat_type", "screen__theater__location__city")
    search_fields = ("screen__name", "row", "number")


# 🎞 Movie
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "genre", "duration_minutes", "release_date")
    search_fields = ("title", "language", "genre")


# 🕒 Show
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ("movie", "screen", "start_time", "end_time", "base_price")
    list_filter = ("screen__theater__location__city", "movie__language")
    search_fields = ("movie__title", "screen__name")


# 💺 ShowSeat
@admin.register(ShowSeat)
class ShowSeatAdmin(admin.ModelAdmin):
    list_display = ("show", "seat", "status", "price")
    list_filter = ("status", "show__movie__language", "seat__seat_type")
    search_fields = ("show__movie__title", "seat__row", "seat__number")
