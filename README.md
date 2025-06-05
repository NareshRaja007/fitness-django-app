# fitness-django-app

# 🏋️ Fitness Booking Django App

A simple fitness class booking API built using Django and Django REST Framework. This app allows users to view upcoming fitness classes and book their slots.

---

## 🚀 Features

- View upcoming classes (Yoga, Zumba, HIIT, etc.)
- Book a class with client name & email
- View bookings filtered by email
- Timezone-aware scheduling (IST)
- Input validation, error handling & logging

---

## 🛠️ Tech Stack

- Python 3.10+
- Django 4+
- Django REST Framework
- SQLite (file-based)
- Logging (Python built-in)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone git@github.com-personal:NareshRaja007/fitness-django-app.git
cd fitness-django-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate

python manage.py shell

python manage.py runserver

 API Endpoints (Postman-Ready)
1. GET /api/classes/
📌 Get all upcoming classes

GET http://localhost:8000/api/classes/

[
  {
    "id": 1,
    "name": "Yoga",
    "instructor": "Aarthi",
    "scheduled_at": "2025-06-06T10:00:00Z",
    "available_slots": 10
  },
  ...
]
POST /api/book/
📌 Book a fitness class

POST http://localhost:8000/api/book/
Content-Type: application/json

{
  "class_id": 1,
  "client_name": "Naresh Raja",
  "client_email": "naresh@example.com"
}

Success Response:

{
  "status": true,
  "message": "Booking successful",
  "data": null
}

Failure Response:

{
  "status": false,
  "error": "No slots available"
}

GET /api/bookings?email=client@example.com
📌 Get all bookings by email

Request:


GET http://localhost:8000/api/bookings?email=naresh@example.com

[
  {
    "id": 1,
    "fitness_class": "Yoga",
    "client_name": "Naresh Raja",
    "client_email": "naresh@example.com",
    "booked_at": "2025-06-04T08:30:00Z"
  },

]

🧪 Testing
You can test endpoints using:

Postman

cURL

Browser (for GET)

📝 Notes
Class time is stored in IST (Asia/Kolkata) and converted appropriately based on the request’s timezone settings.

Basic error handling is included for:

Missing fields

Invalid class ID

Overbooking attempts

📁 Folder Structure

fitness-django-app/
├── api/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── fitness_booking/
│   └── settings.py
├── manage.py
└── requirements.txt
🧑‍💻 Author
Naresh Raja
🔗 GitHub Profile

📜 License
Free for educational use only.



---

Let me know if you want the **Postman Collection JSON export file** too. I can also help you automate seeding, add tests, or Dockerize this.




