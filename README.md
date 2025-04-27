# Epic-X Horoscope

A modern web application for horoscope calculations and matchmaking, built with React, TypeScript, and Ant Design.

## Features

- Horoscope calculation with detailed birth details
- Matchmaking compatibility analysis
- Multilingual support (English, Malayalam, Tamil)
- PDF report generation
- Responsive design with Tailwind CSS
- Form validation and error handling
- Loading states and user feedback

## Tech Stack

- React 18
- TypeScript
- Ant Design 5
- React Router 6
- i18next for internationalization
- Axios for API calls
- Tailwind CSS for styling
- Day.js for date handling

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/epic-x-horoscope.git
cd epic-x-horoscope
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`.

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── forms/
│   │   │   ├── HoroscopeForm.tsx
│   │   │   └── MatchMakingForm.tsx
│   │   ├── results/
│   │   │   ├── HoroscopeResult.tsx
│   │   │   └── MatchMakingResult.tsx
│   │   ├── common/
│   │   │   ├── AppLayout.tsx
│   │   │   ├── LanguageSelector.tsx
│   │   │   └── LoadingSpinner.tsx
│   ├── hooks/
│   │   └── useApi.ts
│   ├── services/
│   │   └── api.ts
│   ├── utils/
│   │   └── pdfUtils.ts
│   ├── locales/
│   │   ├── en.json
│   │   ├── ml.json
│   │   └── ta.json
│   ├── App.tsx
│   ├── index.tsx
│   └── i18n.ts
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Epic-X Horoscope Backend

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd Epic-X_Horoscope
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Backend
```
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 5001
```

## API Usage

### Calculate Horoscope
- **Endpoint:** `POST /api/horoscope/calculate`
- **Content-Type:** `application/json`
- **Body Example:**
```json
{
  "name": "Vinay",
  "gender": "M",
  "date_of_birth": "1987-03-20",
  "time_of_birth": "02:15:00",
  "place_id": 18
}
```
- **Returns:** Horoscope data including planetary positions and an `id`.

### Get South Indian Chart Image
- **Endpoint:** `GET /api/horoscope/chart/south/{horoscope_id}`
- **Returns:** PNG image of the South Indian style Rasi chart.

### Example Workflow
1. **POST** to `/api/horoscope/calculate` with the JSON body above.
2. Get the `id` from the response (e.g., `id: 42`).
3. **GET** `/api/horoscope/chart/south/42` to download/view the chart image.

## Dependencies
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- swisseph
- matplotlib
- numpy
- pytz
- python-multipart

## Notes
- Make sure the Swiss Ephemeris library (`swisseph`) is installed and available for your Python environment.
- The `place_id` should correspond to a valid entry in your places table.
- For development, you can use SQLite or any other supported database.

## License
MIT
