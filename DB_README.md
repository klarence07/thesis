# Database Documentation

The application uses **SQLite** for data storage. The database file is named `codeventures.db` and is located in the `thesis/Codeventures/` directory.

## Credentials

**Username:** None
**Password:** None

Since this is a file-based SQLite database, no authentication credentials are required to connect to it by default. The application handles the connection automatically using the `db_utils.py` module.

## Accessing the Database

You can view or edit the database content using any SQLite client (e.g., *DB Browser for SQLite*, *DBeaver*) or via the command line:

```bash
sqlite3 codeventures.db
```

## Tables

- **questions**: Stores the trivia questions used in the game.
    - `key` (TEXT PRIMARY KEY): The topic identifier.
    - `question` (TEXT): The question text.
    - `answer` (TEXT): The expected answer.
    - `hint` (TEXT): A hint for the player.
