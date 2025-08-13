# Internal Sea Core Frontend

This is the frontend application for the Internal Sea Core project.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

## Login Page Background Image

The login page now uses the beautiful ocean wave background image `fabian-jones-HWe3f8xIJq0-unsplash.jpg`.

**To complete the setup:**
1. Download the image `fabian-jones-HWe3f8xIJq0-unsplash.jpg` (the ocean wave image)
2. Place it in the `frontend/public/` directory
3. The CSS is already configured to use this image

The background image creates a stunning visual effect with:
- Dark, moody ocean waves
- Subtle blue overlay for better text readability
- Professional, atmospheric aesthetic
- Perfect contrast for the white login form

## Features

- **Modern Login Page**: Beautiful two-column layout with ocean background image
- **Responsive Design**: Works on all device sizes
- **Form Validation**: Built-in form validation and error handling
- **Authentication**: Integrated with the backend authentication system
- **Navigation**: Conditional navbar (hidden on login page)

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
src/
├── components/     # Reusable UI components
├── contexts/      # React contexts (Auth, etc.)
├── pages/         # Page components
│   ├── Login.tsx  # Main login page (now the home page)
│   ├── Home.tsx   # Home page (accessible via /home)
│   ├── Dashboard.tsx
│   └── Items.tsx
└── App.tsx        # Main app component with routing
```

## Styling

The login page uses modern CSS features including:
- CSS Grid and Flexbox for layout
- Background image with overlay effects
- Modern form styling with focus states
- Responsive design with media queries
- Professional color scheme and typography

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest) 