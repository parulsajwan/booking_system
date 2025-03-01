# Django Booking System

A web application built with Django REST Framework to manage **inventory bookings** for members.
1. Upload **CSV files** (`members.csv` & `inventory.csv`) via a management command  
2. Book an **inventory item** for a member with constraints (`MAX_BOOKINGS = 2`)  
3. Cancel a **booking** via API  


## Setup Instructions

### Clone the Repository
```bash
git clone <repository-url>
cd booking_system
```

### Create & Activate Virtual Environment
```bash
python -m venv env
source env/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Apply Migrations
```bash
python manage.py migrate
```

### Load Data from CSV
Place `members.csv` and `inventory.csv` in the project root, then run:
```bash
python manage.py load_csv
```


### Start the Server
```bash
python manage.py runserver
```
API will be available at **`http://127.0.0.1:8000/api/v1/`**  


## 📌 API Endpoints

### Book an Inventory Item
- **URL:** `/api/v1/book/`  

### Cancel a Booking
- **URL:** `/api/v1/cancel/`  


### Get Booking List
- **URL:** `/api/v1/booking/` 


### Get Booking by member id
- **URL:** `/api/v1/booking/?member_id=x` 