# Video Streaming Application

A full-stack video streaming application built with Flask backend and React Native frontend, featuring user authentication and video management capabilities.

## Technology Stack

### Backend
- **Framework**: Flask
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **API**: RESTful API with CORS support
- **Environment**: Python 3.x with dotenv for configuration

### Frontend
- **Framework**: React Native with Expo
- **State Management**: Async Storage
- **Navigation**: React Navigation (Stack & Native)
- **HTTP Client**: Axios
- **Platforms**: iOS, Android, Web

### Additional Dependencies
- Flask-CORS for cross-origin resource sharing
- PyJWT for token authentication
- Expo CLI for mobile development

## Setup Instructions

### Backend Setup

#### Prerequisites
- Python 3.8 or higher
- MongoDB (local or remote instance)
- pip (Python package manager)

#### Installation Steps

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors python-dotenv flask-pymongo pyjwt bcrypt
   ```

4. **Create a .env file** in the backend directory
   ```
   MONGO_URI=mongodb://localhost:27017/videoapp
   SECRET_KEY=your_secret_key_here
   JWT_SECRET=your_jwt_secret_here
   ```

5. **Run the Flask application**
   ```bash
   python app.py
   ```

The backend server will start at `http://localhost:5000`

#### Backend Project Structure
- `app.py` - Flask application factory and entry point
- `auth.py` - Authentication endpoints and logic
- `routes.py` - API endpoints for video management
- `models.py` - Data models and database schemas
- `extensions.py` - Flask extensions initialization
- `test_backend.py` - Unit tests for backend functionality

### Frontend Setup

#### Prerequisites
- Node.js and npm
- Expo CLI (`npm install -g expo-cli`)
- iOS Simulator (macOS) or Android Emulator for testing

#### Installation Steps

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Update API configuration** in `config.js`
   - Set the backend API URL to match your Flask server (e.g., `http://localhost:5000`)

4. **Start the Expo development server**
   ```bash
   npm start
   ```

5. **Run on your preferred platform**
   ```bash
   # For Android
   npm run android

   # For iOS
   npm run ios

   # For Web
   npm run web
   ```

#### Frontend Project Structure
- `App.js` - Main application component
- `index.js` - Entry point
- `config.js` - Configuration settings (API URLs, etc.)
- `app.json` - Expo configuration file
- `screens/` - Application screens
  - `AuthScreen.js` - User login/registration
  - `DashboardScreen.js` - Video listing and selection
  - `VideoPlayerScreen.js` - Video playback interface
  - `SettingsScreen.js` - User settings

## API Documentation Summary

### Authentication Endpoints
- **POST** `/auth/register` - Register a new user
  - Body: `{ username, password, email }`
  - Returns: User ID and authentication token

- **POST** `/auth/login` - Authenticate user
  - Body: `{ username, password }`
  - Returns: JWT token for authenticated requests

- **POST** `/auth/logout` - Log out user
  - Headers: `Authorization: Bearer <token>`

### Video Endpoints
- **GET** `/dashboard` - Retrieve featured videos
  - Returns: Array of video objects with metadata

- **GET** `/videos` - Get all available videos
  - Returns: List of video objects

- **GET** `/videos/<id>` - Get video details
  - Returns: Single video object with full metadata

- **POST** `/videos` - Create new video (admin)
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ title, description, youtube_id }`

- **PUT** `/videos/<id>` - Update video metadata
  - Headers: `Authorization: Bearer <token>`
  - Body: Video fields to update

- **DELETE** `/videos/<id>` - Delete video (admin)
  - Headers: `Authorization: Bearer <token>`

### Response Format
All API responses follow a standard JSON format:
```json
{
  "id": "video_id",
  "title": "Video Title",
  "description": "Video description",
  "youtube_id": "YouTube video ID",
  "thumbnail": "URL to thumbnail image",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "is_active": true
}
```

## Getting Started

1. Start the MongoDB server locally or configure a remote connection
2. Set up and run the backend server following the Backend Setup instructions
3. Set up and run the frontend application following the Frontend Setup instructions
4. Access the application through the Expo client on your device or emulator

## Environment Configuration

Create `.env` files in both backend and frontend directories as needed:

**Backend `.env` example:**
```
MONGO_URI=mongodb://localhost:27017/videoapp
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-change-in-production
FLASK_ENV=development
```

**Frontend `config.js` example:**
```javascript
export const API_BASE_URL = 'http://localhost:5000';
export const API_TIMEOUT = 10000;
```

## Testing

Run backend tests:
```bash
cd backend
python -m pytest test_backend.py
```

## License

This project is private and not licensed for external distribution.
