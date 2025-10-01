# 1. ❓ Question

When we create a new show (e.g., Show 1 at 7 AM to 11 AM in Screen 1), we assign seats from Screen 1 layout.
Now, for the next show (e.g., Show 2 at 12 PM to 3 PM in the same Screen), do we need to recreate the seats again for that show?
---

### 💡 Key Idea

* **Seats are physical objects** tied to a **Screen**. They don’t change across shows.
* What changes across shows is only the **status** of each seat (available, booked, blocked).
* That’s why we **don’t recreate seats** for every show. Instead, we reuse the same `Seat` rows, but create **Show_Seat entries** to represent their availability for a specific show.

---

### 🏗 How It Works

#### Step 1: Define Seats (once per Screen)

Example: Screen 1 has 100 seats. You create 100 `Seat` records tied to `screen=Screen 1`.

```python
A1, A2, A3 ... A10  
B1, B2, B3 ... B10  
...  
```

These seats exist **once in DB** and are never recreated.

---

#### Step 2: Create a Show

Example:

* Show 1 → 7 AM to 11 AM on Screen 1
* Show 2 → 12 PM to 3 PM on Screen 1

When you create a show, you don’t create seats again. Instead, you create `Show_Seat` entries:

```python
for seat in Seat.objects.filter(screen=screen1):
    Show_Seat.objects.create(show=show1, seat=seat, status="AVAILABLE")
```

Same for Show 2.

---

#### Step 3: Booking Flow

* User selects a seat for a show.
* You look up the **Show_Seat** record (`seat_id + show_id`).
* Update its status to `"BOOKED"`.

---

### ✅ Example

* **Seats table** (static):

```
id | screen_id | seat_row | seat_number
1  | 1         | A        | 1
2  | 1         | A        | 2
3  | 1         | A        | 3
...
```

* **Show table**:

```
id | screen_id | movie_id | start_time | end_time
1  | 1         | 10       | 7am        | 11am
2  | 1         | 10       | 12pm       | 3pm
```

* **Show_Seat table** (dynamic):

```
id | show_id | seat_id | status
1  | 1       | 1       | AVAILABLE
2  | 1       | 2       | BOOKED
3  | 2       | 1       | AVAILABLE   <- same seat reused for new show
```

Notice 👆 `seat_id=1` (Screen 1, Seat A1) is reused across different shows.

---

### 🎯 So the answer:

👉 **You do not recreate seats multiple times.**
You create them **once per Screen**, and for every new show, you just create `Show_Seat` mappings that point to those same seats.

---

Would you like me to show you a **Django signal / helper function** that automatically creates all `Show_Seat` entries whenever you create a new `Show`? That way you don’t need to manually do the mapping each time.
