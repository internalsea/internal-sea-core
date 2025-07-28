# React Frontend

This is the React frontend for the Internal Sea Core project.

## Features

- Modern React 18 with TypeScript
- React Router for navigation
- Context API for state management
- Axios for API communication
- Responsive design with CSS
- JWT authentication integration
- Protected routes

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   └── Navbar.css
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Home.css
│   │   ├── Login.tsx
│   │   ├── Login.css
│   │   ├── Dashboard.tsx
│   │   ├── Dashboard.css
│   │   ├── Items.tsx
│   │   └── Items.css
│   ├── App.tsx
│   ├── App.css
│   ├── index.tsx
│   ├── index.css
│   └── reportWebVitals.ts
├── package.json
└── README.md
```

## Pages

- **Home** (`/`) - Welcome page with feature overview
- **Login** (`/login`) - User authentication
- **Dashboard** (`/dashboard`) - User dashboard with statistics (protected)
- **Items** (`/items`) - Item management (protected)

## Authentication

The app uses JWT tokens for authentication. The `AuthContext` manages:
- User login/logout
- Token storage in localStorage
- Protected route access
- User state across the application

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`. The proxy configuration in `package.json` handles CORS during development.

## Styling

The app uses custom CSS with:
- Responsive design
- Modern card-based layouts
- Consistent color scheme
- Hover effects and transitions
- Mobile-friendly navigation 