# 📚 Books
I have a lots of books. They're everywhere in my live. This project helps me keep track of them.

## 🎯 About the project
I have three goals with this project. I would like to improve my sqlalchemy skills. For this reason, the project is based on sqlalchemy ORM. <br>
I also want to learn more about deployment. That is why the project is running in containers. In future, it will run in the cloud. <br>
Finally, the project is intended to manage my books.
<br>
So far, building a frontend has not been priority. That is why the user interface is a simple CLI.

## 📖 Features
The app has five sections. Each section has features for add, update, delete and search. If an object does not exist, it will be created. 

## 📋 Requirements
- Windows, Linux, Mac
- Python 3.x

## 💾 Installation
### 1. Clone the repository
```bash
git clone https://github.com/Flex0152/books.git
cd books
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
```

```bash
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install uv
uv sync
```

### 4. Initialize the database
```bash
uv run database.py
```

## 🚀 Quick Start
All commands follow this structure:

```
uv run cli.py <resource> <command> [arguments]
```

### Books

| Command | Description |
|---|---|
| `Books add <title> <author> <genre> <state> <location>` | Add a new book |
| `Books update <title> [options]` | Update an existing book |
| `Books delete <title>` | Delete a book |
| `Books search <title>` | Search for a book by title |
| `Books all` | List all books |

**Options for `Books update`:**

| Option | Description |
|---|---|
| `--new-title` | Rename the book |
| `--new-author` | Change the author |
| `--genre` | Change the genre |
| `--state` | Change the reading state |
| `--location` | Change the shelf location |
| `--published` | Change the publication date (`YYYY-MM-DD`) |

**Examples:**

```bash
# Add a book
uv run cli.py Books add "The Pragmatic Programmer" "David Thomas" "Tech" "unread" "Shelf A" --published 1999-10-20

# Update a book's state
uv run cli.py Books update "The Pragmatic Programmer" --state "read"

# Delete a book (provide author if the title is ambiguous)
uv run cli.py Books delete "The Pragmatic Programmer" "David Thomas"
```

---

### Authors

```bash
uv run cli.py Authors add <name>
uv run cli.py Authors update <name> <new-name>
uv run cli.py Authors delete <name>
uv run cli.py Authors search <name>
uv run cli.py Authors all
```

### Genres

```bash
uv run cli.py Genres add <name>
uv run cli.py Genres update <name> <new-name>
uv run cli.py Genres delete <name>
uv run cli.py Genres search <name>
```

### Locations

```bash
uv run cli.py Locations add <shelf>
uv run cli.py Locations update <shelf> <new-shelf>
uv run cli.py Locations delete <shelf>
uv run cli.py Locations search <shelf>
```

### States

```bash
uv run cli.py States add <name>
uv run cli.py States update <name> <new-name>
uv run cli.py States delete <name>
uv run cli.py States search <name>
uv run cli.py States all
```

## 📄 License
This Project is released under the MIT [./LICENSE].