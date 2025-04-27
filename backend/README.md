# Epic-X Horoscope Backend

This is the backend service for the Epic-X Horoscope application, built with FastAPI and MySQL.

## Features

- Horoscope calculation
- Matchmaking analysis
- PDF report generation
- Multilingual support
- Database integration with Indian districts data

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment template and configure:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your database credentials and API configuration.

5. Initialize the database:
   ```bash
   python -m app.db.init_places
   ```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5001
```

The API will be available at `http://localhost:5001`

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:5001/docs`
- ReDoc: `http://localhost:5001/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration
│   ├── db/            # Database models and initialization
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic models
│   └── services/      # Business logic
├── tests/             # Test files
├── .env.example       # Environment variables template
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

## Requirements

fastapi
uvicorn
sqlalchemy
pydantic
swisseph
matplotlib
numpy
pytz
python-multipart 

### 4. Initialize the Database

#### Option A: Python Script 

This will create the tables and seed the `places` table with sample data.