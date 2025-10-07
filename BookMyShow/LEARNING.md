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
Sure! Here’s your content formatted with **Markdown** for clarity, headings, and tables:

---
# 2. ❓ Question

# 📄 Documentation: Django ORM – Persistence vs. Transience

## The Question (Refined for Technical Accuracy)

**Topic:** Django Models and Data Persistence

**Question:**

In Django, when a Python Model Class is defined in `models.py` (inheriting from `django.db.models.Model`), it represents a **database table schema**.

My confusion: Typical Python object instances are **transient** (created and destroyed in memory after a request). Why does Django require us to **permanently define and create a persistent database table** (via migrations) for this class?

Essentially: Why must the data structure be **hardcoded** (schema fixed in the database), and how does the **persistence and separation of schema (Model Class) from runtime object (Model Instance)** provide essential value in a real-world, scalable application?

---

## The Necessity of Persistence in Distributed Systems

Modern web development often uses **microservices architecture**, where different functionalities are handled by separate servers and processes. Persistence allows all these components to access and share data reliably.

| Component                   | Responsibility (Service)                    | Requirement for Persistence                      |
| --------------------------- | ------------------------------------------- | ------------------------------------------------ |
| Frontend/Web App            | Handles user requests (browsing, searching) | Needs to read data saved by other services       |
| Booking Engine Server       | Allocates seats, processes payments         | Needs to write data that other services will use |
| Analytics/Reporting Service | Tracks sold tickets, revenue, and trends    | Needs to read data written by the Booking Engine |

**Why it matters:**

If the data were **transient**, living only in memory of the Booking Engine service:

* Web App couldn’t display seat availability.
* Analytics service couldn’t track ticket sales.

The **database provides a single source of truth** for all services.

---

## BookMyShow Example: The Life of a Booking Object

Let’s trace how **persistence** of a single Ticket object enables the system to work across multiple services.

### 1️⃣ The Initial Action (Transient Object)

* **User Action:** A user clicks **"Book Now"** for a movie.
* **Service:** Web/API Server handles the request.
* **Object State:** A temporary Python `Ticket` object is created in memory. It is **transient** and holds temporary info, e.g., selected seats `A5, A6`.

---

### 2️⃣ Achieving Persistence (Shared Data)

* **Service:** Web/API Server sends data to the Booking Microservice.
* **Code:**

```python
Ticket.objects.create(seats='A5, A6', status='PENDING')
```

* **Result:**

  * The ORM converts the transient Python object into an SQL `INSERT` statement.
  * Database saves a new **persistent record** (row in the `Tickets` table).
  * The Python object can now be safely destroyed; the data survives.

---

### 3️⃣ Cross-Service Dependency (Reading the Persistent Data)

Immediately after the ticket is persisted, other services need this data:

| Service                  | Purpose                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Payment Service**      | Checks the database record to confirm ticket status is `PENDING` before charging the user. Updates status: `Ticket.objects.filter(id=123).update(status='PAID')` |
| **Seat Map Service**     | Reads persistent data to display that seats `A5` and `A6` are now taken and should be grayed out                                                                 |
| **Confirmation Service** | Reads persistent ticket record to generate/send booking confirmation via email/SMS                                                                               |

---

## ✅ Conclusion

Without **data persistence**, the Ticket object’s data would remain locked in the memory of the initial service.

**Benefits of persistence and ORM in Django:**

1. **Consistency across services:** Multiple services can read/write shared data reliably.
2. **Separation of schema and runtime objects:** Model class defines structure; object instance holds temporary data.
3. **Scalability:** Supports distributed and microservices architecture.
4. **Durability:** Data survives server restarts, crashes, and multiple requests.

The Django ORM acts as a **persistent handshake** between Python objects and the database, ensuring a **shared, consistent, and durable state** for real-world applications.

---

If you want, I can also create a **diagram showing transient vs persistent objects** in Django with multiple services — it makes this concept visually clear.

Do you want me to make that diagram?
