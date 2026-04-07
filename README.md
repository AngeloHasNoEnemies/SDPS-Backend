# SDPS Backend — Smart Drainage Protection System

A Django REST Framework backend for the Smart Drainage Protection System (SDPS), providing APIs for drainage monitoring, sensor data, flood alerts, and maintenance reports.

---

## Requirements

Make sure you have the following installed before starting:

- Python 3.11 or 3.12 (⚠️ avoid Python 3.14 — compatibility issues with Django)
- pip
- git

### Python packages to install

Run this in your terminal inside the project folder:

```bash
pip install django
pip install djangorestframework
pip install httpie
```

Or if a `requirements.txt` is present:

```bash
pip install -r requirements.txt
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AngeloHasNoEnemies/SDPS-Backend.git
cd SDPS-Backend
```

### 2. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 4. Run the development server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000`

---

## Important Links

| Page | URL |
|---|---|
| API Root | http://127.0.0.1:8000/api/ |
| Django Admin Panel | http://127.0.0.1:8000/admin/ |
| Drainage Locations | http://127.0.0.1:8000/api/locations/ |
| Sensor Data | http://127.0.0.1:8000/api/sensor-data/ |
| Alerts | http://127.0.0.1:8000/api/alerts/ |
| Maintenance Reports | http://127.0.0.1:8000/api/maintenance/ |
| Register | http://127.0.0.1:8000/api/auth/register/ |
| Login | http://127.0.0.1:8000/api/auth/login/ |
| Profile | http://127.0.0.1:8000/api/auth/profile/ |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and get token |
| GET | `/api/auth/profile/` | View your profile |

### Drainage Locations

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/locations/` | List all locations |
| POST | `/api/locations/` | Add a new location |
| GET | `/api/locations/{id}/` | Get a single location |
| PUT | `/api/locations/{id}/` | Update a location |
| DELETE | `/api/locations/{id}/` | Delete a location |
| GET | `/api/locations/{id}/sensor_data/` | Get sensor readings for a location |
| GET | `/api/locations/{id}/alerts/` | Get alerts for a location |

### Sensor Data

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/sensor-data/` | List all sensor readings |
| POST | `/api/sensor-data/` | Submit new sensor reading |

### Alerts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/alerts/` | List all alerts |
| POST | `/api/alerts/` | Create a new alert |
| POST | `/api/alerts/{id}/resolve/` | Mark an alert as resolved |

### Maintenance Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/maintenance/` | List all reports |
| POST | `/api/maintenance/` | Submit a new report |

---

## Testing with httpie

### Register a user
```bash
http POST http://127.0.0.1:8000/api/auth/register/ username="testuser" email="test@test.com" first_name="Test" last_name="User" password="pass1234" password2="pass1234"
```

### Login and get token
```bash
http POST http://127.0.0.1:8000/api/auth/login/ username="testuser" password="pass1234"
```

### Access a protected endpoint
```bash
http GET http://127.0.0.1:8000/api/locations/ "Authorization: Token your-token-here"
```

---

## Project Structure

```
sdps-backend/
├── manage.py
├── sdps_project/          # Project settings
│   ├── settings.py
│   ├── urls.py            # Main URL router
│   ├── wsgi.py
│   └── asgi.py
└── sdps/                  # Main app
    ├── models.py          # DrainageLocation, SensorData, Alert, MaintenanceReport
    ├── serializers.py     # JSON converters
    ├── views.py           # API ViewSets
    ├── urls.py            # App URL routes
    └── admin.py           # Admin panel config
```

---

## Models Overview

| Model | Description |
|---|---|
| `DrainageLocation` | Stores drainage site info (name, coordinates, status) |
| `SensorData` | Records water level, flow rate, blockage, turbidity readings |
| `Alert` | Flood warnings and system alerts per location |
| `MaintenanceReport` | Maintenance requests and resolution logs |

---

## Notes

- All API endpoints require a token in the `Authorization` header except `/api/auth/register/` and `/api/auth/login/`
- Token format: `Authorization: Token <your-token>`
- This backend is built to support the SDPS web and mobile UI in future integration activities
