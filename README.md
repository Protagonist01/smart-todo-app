# Smart Todo Application

A command-line todo application with advanced features powered by regular expressions for intelligent task parsing and management.

## Features

- ✅ Smart task parsing with natural language input
- 🏷️ Tag-based organization (@work, @personal, @shopping)
- ⚡ Priority levels (#high, #medium, #low)
- 📅 Due date support (due:YYYY-MM-DD)
- 👤 Task assignment (assigned:email@example.com)
- 🔍 Powerful regex-based search and filtering
- 💾 Persistent JSON storage
- 🧪 Comprehensive test coverage

## Project Status

🚧 **Under Development** - Week 1 Intermediate Cohort 4 Project

## Requirements

- Python 3.10+
- Poetry (dependency management)

## Installation
```bash
# Clone the repository
git clone git@github.com:YOUR-USERNAME/smart-todo-app.git
cd smart-todo-app

# Install dependencies
poetry install

# Run the application
poetry run python src/main.py
```

## Usage Examples
```bash
# Add a task with smart parsing
> add "Complete project @school #high due:2025-10-20 assigned:alice@example.com"
✓ Task added: Complete project
  Tags: school | Priority: high | Due: 2025-10-20

# List tasks
> list

# Search by tag
> search "@work"

# Mark task as complete
> complete 1
```

## Development

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
poetry run black src/ tests/

# Lint code
poetry run flake8 src/ tests/

# Type checking
poetry run mypy src/
```

## Project Structure
```
todo-app/
├── src/
│   ├── models/          # Data models
│   ├── parsers/         # Regex parsing logic
│   ├── services/        # Business logic
│   ├── utils/           # Helper functions
│   └── cli/             # CLI interface
├── tests/               # Unit tests
├── data/                # Data storage
└── docs/                # Documentation
```

## Author

Fadeni Taiwo Henry

## License

MIT License