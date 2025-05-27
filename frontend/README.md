# Epic-X Horoscope Frontend

This is the frontend application for the Epic-X Horoscope system, built with React, TypeScript, and Ant Design.

## Features

- Modern, responsive UI with Ant Design
- Horoscope calculation form
- Matchmaking analysis form
- Multilingual support (English, Malayalam, Tamil)
- PDF report generation and download
- Form validation and error handling
- Loading states and animations

## Prerequisites

- Node.js 16+
- npm or yarn package manager

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Create a `.env` file in the root directory with the following content:
   ```
   REACT_APP_API_URL=http://localhost:5001/api
   ```

## Running the Application

Start the development server:
```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── public/            # Static files
├── src/
│   ├── components/    # React components
│   │   ├── common/    # Shared components
│   │   ├── horoscope/ # Horoscope-related components
│   │   └── matchmaking/ # Matchmaking components
│   ├── hooks/         # Custom React hooks
│   ├── services/      # API services
│   ├── translations/  # Language files
│   ├── utils/         # Utility functions
│   ├── App.tsx        # Main application component
│   └── index.tsx      # Entry point
├── package.json       # Project dependencies
└── README.md         # This file
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
