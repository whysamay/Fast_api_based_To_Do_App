# Todo Hub - Full-Stack Todo Application

A modern, full-stack todo application built with FastAPI backend and React frontend, featuring user authentication, priority management, and real-time updates.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure JWT-based authentication system
- **Todo Management**: Create, read, update, and delete todos
- **Priority System**: 5-level priority management (Very High to Very Low)
- **User Profiles**: Edit personal information and preferences
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Technical Features
- **Real-time Updates**: Instant UI updates without page refresh
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Data Validation**: Client and server-side validation
- **Security**: Password hashing, JWT tokens, and CORS protection

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **SQLite**: Lightweight, serverless database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for secure authentication
- **bcrypt**: Password hashing for security
- **Alembic**: Database migration tool

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling with responsive design
- **Context API**: State management for authentication

### Development Tools
- **Uvicorn**: ASGI server for FastAPI
- **npm**: Package manager for Node.js
- **Git**: Version control

## 📁 Project Structure

```
Fast-API-Proj/
├── ToDoApp/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLAlchemy database models
│   ├── database.py             # Database configuration
│   ├── routers/                # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── todos.py           # Todo CRUD operations
│   │   ├── users.py           # User profile management
│   │   └── admin.py           # Admin functionality
│   ├── todo-frontend/          # React frontend application
│   │   ├── src/
│   │   │   ├── components/    # React components
│   │   │   ├── contexts/      # React contexts
│   │   │   ├── services/      # API service layer
│   │   │   └── App.js         # Main React component
│   │   └── package.json       # Frontend dependencies
│   └── requirements.txt        # Python dependencies
└── README.md                   # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd ToDoApp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd ToDoApp/todo-frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:3000`

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/token` - OAuth2 token endpoint

### Todo Endpoints
- `GET /todos/` - Get all todos for authenticated user
- `POST /todos/` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

### User Endpoints
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile

## 🔧 Configuration

### Environment Variables
The application uses default configurations, but you can customize:

- `REACT_APP_API_URL`: Frontend API base URL (default: http://localhost:8000)
- Database connection settings in `database.py`

### Database
The application uses SQLite by default. For production, consider:
- PostgreSQL for better performance
- Environment variables for database credentials
- Proper database backup strategies

## 🧪 Testing

### Backend Testing
```bash
cd ToDoApp
python -m pytest test/
```

### Frontend Testing
```bash
cd ToDoApp/todo-frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
1. Set up a production server (Ubuntu, CentOS, etc.)
2. Install Python and dependencies
3. Use Gunicorn with Uvicorn workers
4. Set up reverse proxy (Nginx)
5. Configure environment variables

### Frontend Deployment
1. Build the production version: `npm run build`
2. Deploy to static hosting (Netlify, Vercel, AWS S3)
3. Configure API endpoint for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- React team for the powerful frontend library
- SQLAlchemy for robust database operations

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ using FastAPI and React** 