# ToDo App Frontend

A modern React frontend for the ToDo application with authentication, task management, and user profile features.

## Features

- 🔐 **User Authentication**: Login and registration with JWT tokens
- ✅ **Todo Management**: Create, read, update, and delete todos
- 🎯 **Task Filtering**: Filter todos by status (All, Active, Completed)
- 👤 **User Profile**: View and edit user information
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Clean and intuitive user interface

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Context API**: State management for authentication
- **CSS3**: Modern styling with flexbox and grid

## Project Structure

```
src/
├── components/          # React components
│   ├── Auth.css        # Authentication styles
│   ├── Login.js        # Login component
│   ├── Navbar.css      # Navigation styles
│   ├── Navbar.js       # Navigation component
│   ├── Profile.css     # Profile styles
│   ├── Profile.js      # Profile component
│   ├── PrivateRoute.js # Route protection
│   ├── TodoForm.css    # Todo form styles
│   ├── TodoForm.js     # Todo form component
│   ├── TodoItem.css    # Todo item styles
│   ├── TodoItem.js     # Todo item component
│   ├── TodoList.css    # Todo list styles
│   └── TodoList.js     # Todo list component
├── contexts/           # React contexts
│   └── AuthContext.js  # Authentication context
├── services/           # API services
│   └── api.js         # Axios configuration
├── App.css            # App styles
├── App.js             # Main app component
├── index.css          # Global styles
├── index.js           # App entry point
└── reportWebVitals.js # Performance monitoring
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd todo-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

### Available Scripts

- `npm start`: Start the development server
- `npm build`: Build the app for production
- `npm test`: Run tests
- `npm eject`: Eject from Create React App (not recommended)

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

### Authentication
- `POST /auth/login`: User login
- `POST /auth/register`: User registration

### User Management
- `GET /users/me`: Get current user profile
- `PUT /users/me`: Update user profile

### Todo Management
- `GET /todos/`: Get all todos for current user
- `POST /todos/`: Create a new todo
- `PUT /todos/{id}`: Update a todo
- `DELETE /todos/{id}`: Delete a todo

## Features in Detail

### Authentication
- JWT token-based authentication
- Automatic token refresh
- Protected routes
- Persistent login state

### Todo Management
- Create todos with title and description
- Mark todos as complete/incomplete
- Edit todo details
- Delete todos with confirmation
- Filter todos by status

### User Profile
- View user information
- Edit profile details
- Update contact information

### Responsive Design
- Mobile-first approach
- Responsive navigation
- Touch-friendly interface
- Optimized for all screen sizes

## Environment Variables

Create a `.env` file in the root directory to configure the API URL:

```
REACT_APP_API_URL=http://localhost:8000
```

## Deployment

### Build for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

### Deploy to Static Hosting

The app can be deployed to any static hosting service:

- **Netlify**: Drag and drop the `build` folder
- **Vercel**: Connect your GitHub repository
- **GitHub Pages**: Use `gh-pages` package
- **AWS S3**: Upload the `build` folder

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 