# Data Model: Task Web App

## Entities

### User
Represents a registered user in the system.
- **id**: Integer (Primary Key)
- **email**: String (Unique, Indexed)
- **password_hash**: String
- **created_at**: DateTime (Auto-generated)

### Task
Represents an item created by a user.
- **id**: Integer (Primary Key)
- **user_id**: Integer (Foreign Key -> User.id)
- **title**: String (Required)
- **description**: String (Optional)
- **status**: Boolean (Default: False)
- **category**: String (Optional, e.g., "Work", "Personal")
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated)

## Relationships
- **User -> Task**: One-to-Many (A user can have many tasks).

## Database Schema (SQLModel/PostgreSQL)

```sql
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "task" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    description TEXT,
    status BOOLEAN DEFAULT FALSE,
    category VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
