# Project Constitution

## Version 1.0.0

This document outlines the core principles and conventions governing this project. Adherence to these principles is mandatory for all contributions.

### 1. **Simplicity First**
- All code, architecture, and documentation should be as simple as possible, but no simpler. Avoid premature optimization and unnecessary complexity.

### 2. **In-Memory Data Store**
- The application must operate on an in-memory data model. No external databases, files, or persistent storage mechanisms are to be used unless explicitly approved as a core feature change.

### 3. **CLI-Centric Interface**
- The primary interface for this application is the command-line (CLI). All core functionality must be accessible and usable through the terminal.

### 4. **PEP 8 Compliance**
- All Python code must strictly adhere to the PEP 8 style guide. Code should be clean, readable, and consistent.

### 5. **Modularity and Separation of Concerns**
- **models.py**: Defines the data structures (the "nouns").
- **services.py**: Contains the business logic (the "verbs").
- **cli.py**: Handles user interaction and presentation.

### 6. **Testing**
- While not implemented in the initial build, all new features or bug fixes should ideally be accompanied by corresponding tests in the `/tests` directory.

### Phase III Addendum
- The architecture has evolved to a Full-stack Web application using FastAPI for the backend and Next.js for the frontend
- Persistent storage is now handled by Neon PostgreSQL database
- The CLI-centric interface is deprecated in favor of web-based interfaces
- New modules and services should be designed with web scalability in mind
