# Developer Portal Frontend

Production-grade React frontend built with Vite, Material UI, and Context API.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Material UI** - Component library
- **React Router v6** - Routing
- **Axios** - HTTP client
- **Context API** - State management

## Features

- ✅ Enterprise folder structure
- ✅ Reusable component architecture
- ✅ Context API for state management
- ✅ API service abstraction layer
- ✅ Material UI theming
- ✅ Responsive design
- ✅ Environment-driven configuration
- ✅ Error handling and notifications
- ✅ Loading states
- ✅ Clean code (no comments in code)

## Prerequisites

- Node.js 18+ and npm

## Installation

```bash
npm install
```

## Environment Setup

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8080/api/v1
```

## Development

```bash
npm run dev
```

Access at: http://localhost:5173

## Build

```bash
npm run build
```

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable UI components
├── config/          # Configuration files
├── contexts/        # Context API providers
├── layouts/         # Page layouts
├── pages/           # Page components
├── routes/          # Routing configuration
├── services/        # API service layer
├── App.jsx          # Root component
└── main.jsx         # Entry point
```

## Available Routes

- `/` - Home page
- `/projects` - Project list
- `/projects/create` - Create project
- `/projects/:id` - Project details
- `/projects/:id/edit` - Edit project
- `/tasks` - Task list
- `/tasks/create` - Create task
- `/tasks/:id` - Task details
- `/tasks/:id/edit` - Edit task

## Architecture Highlights

### Context API
- **AppContext**: Global state (loading, notifications)
- **ProjectContext**: Project CRUD operations
- **TaskContext**: Task CRUD operations

### Service Layer
- **httpClient**: Axios instance with interceptors
- **projectService**: Project API abstraction
- **taskService**: Task API abstraction

### Component Structure
- **Common Components**: Button, Card, Loader, Notification
- **Layout Components**: Header, Footer
- **Page Components**: Feature-specific pages

## Why This Architecture?

### Context API Benefits
1. No prop drilling
2. Centralized state management
3. Reusable custom hooks
4. Clean component code

### API Abstraction Benefits
1. Single source of truth for endpoints
2. Easy to maintain and test
3. Centralized error handling
4. Environment flexibility

### Scalability Features
1. Feature-based organization
2. Reusable components
3. Separation of concerns
4. Clean code principles

## Code Quality Standards

- No comments inside code (self-documenting)
- No massive components (single responsibility)
- No business logic in UI components
- Consistent naming conventions
- Proper error handling
- Loading states for async operations

## Documentation

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## API Integration

Backend services:
- API Gateway: http://localhost:8080
- Project Service: http://localhost:8001
- Task Service: http://localhost:8002

All requests go through API Gateway at `/api/v1` prefix.
