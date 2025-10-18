# Smart Todo Application - Architecture Documentation

## Overview

The Smart Todo Application is built with a modular, layered architecture emphasizing separation of concerns, testability, and maintainability.

## Architecture Layers
```
┌─────────────────────────────────────────────────────┐
│                  CLI Interface                       │
│              (User Interaction Layer)                │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                 Task Service                         │
│            (Business Logic Layer)                    │
└─────────┬───────────────────────────┬───────────────┘
          │                           │
┌─────────▼─────────┐       ┌────────▼────────────────┐
│    TodoList       │       │  Storage Service        │
│  (Data Manager)   │       │  (Persistence Layer)    │
└─────────┬─────────┘       └─────────────────────────┘
          │
┌─────────▼─────────┐
│    Task Model     │
│   (Data Layer)    │
└───────────────────┘

┌───────────────────────────────────────────────────┐
│              Parser Subsystem                      │
│  ┌──────────────┐  ┌──────────────┐              │
│  │ Task Parser  │  │  Validator   │              │
│  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                       │
│  ┌──────▼───────┐  ┌──────▼───────┐              │
│  │ Date Parser  │  │Regex Patterns│              │
│  └──────────────┘  └──────────────┘              │
└───────────────────────────────────────────────────┘
```

## Component Details

### 1. Models Layer

#### Task (`src/models/task.py`)
- **Responsibility**: Represents a single todo item
- **Key Features**:
  - Dataclass-based for immutability and clarity
  - Auto-generated UUID for unique identification
  - Timestamp tracking (created_at, updated_at)
  - Property methods (is_complete, is_overdue, is_high_priority)
  - Serialization support (to_dict/from_dict)
  
#### TodoList (`src/models/todo_list.py`)
- **Responsibility**: Manages collection of tasks
- **Key Features**:
  - Dictionary-based storage for O(1) lookups
  - CRUD operations
  - Filtering and searching
  - Bulk operations (clear_all, clear_complete)

### 2. Parser Subsystem

#### Regex Patterns (`src/parsers/regex_patterns.py`)
- **Responsibility**: Define all regex patterns
- **Patterns**:
  - Tags: `@(\w+)`
  - Priority: `#(high|medium|low)`
  - Dates: `due:(\d{4}-\d{2}-\d{2})`
  - Email: `assigned:([email pattern])`
  - Time: `(at|by)\s+(\d{1,2}):?(\d{2})?\s*(am|pm)?`

#### Task Parser (`src/parsers/task_parser.py`)
- **Responsibility**: Main orchestrator for parsing
- **Process**:
  1. Extract metadata using regex
  2. Parse dates via date_parser
  3. Validate via validator
  4. Clean description (remove metadata)
  5. Return structured data

#### Date Parser (`src/parsers/date_parser.py`)
- **Responsibility**: Convert various date formats
- **Supports**:
  - Exact dates (YYYY-MM-DD)
  - Relative dates (today, tomorrow)
  - Offset dates (3 days, 2 weeks)

#### Validator (`src/parsers/validator.py`)
- **Responsibility**: Validate all task components
- **Validations**:
  - Email format
  - Priority levels
  - Date formats
  - Tag formats

### 3. Services Layer

#### Storage Service (`src/services/storage_service.py`)
- **Responsibility**: JSON file persistence
- **Features**:
  - Auto-create directories
  - Error handling
  - Backup/restore functionality
  - UTF-8 encoding

#### Task Service (`src/services/task_service.py`)
- **Responsibility**: High-level API combining TodoList + Storage
- **Features**:
  - Automatic persistence on all operations
  - Natural language task creation
  - Search functionality
  - Statistics

### 4. CLI Layer

#### CLI Interface (`src/cli/interface.py`)
- **Responsibility**: User interaction
- **Features**:
  - Command parsing
  - Pretty output formatting
  - Interactive confirmations
  - Help system

## Data Flow Examples

### Adding a Task
```
User: "add Buy milk @shopping #high due:tomorrow"
  │
  ▼
CLI.cmd_add()
  │
  ▼
TaskService.add_task_from_string()
  │
  ▼
TaskParser.create_task_from_string()
  │
  ├─→ extract_tags() → ["shopping"]
  ├─→ extract_priority() → "high"
  ├─→ extract_due_date() → "2025-10-18"
  ├─→ remove_metadata() → "Buy milk"
  └─→ validate_task_data() → (True, [])
  │
  ▼
Task.from_dict() → Task object
  │
  ▼
TodoList.add_task()
  │
  ▼
StorageService.save() → JSON file
  │
  ▼
CLI: "✓ Task added successfully!"
```

### Listing Tasks
```
User: "list --tag work"
  │
  ▼
CLI.cmd_list(["--tag", "work"])
  │
  ▼
TaskService.list_by_tag("work")
  │
  ▼
TodoList.list_by_tag("work")
  │
  ▼
Filter: [t for t in tasks if "work" in t.tags]
  │
  ▼
CLI.display_tasks() → Formatted output
```

## Design Patterns

### 1. Repository Pattern
- `TodoList` acts as in-memory repository
- `StorageService` handles persistence
- Separation of data access from business logic

### 2. Service Layer Pattern
- `TaskService` provides high-level API
- Encapsulates complex operations
- Automatic persistence

### 3. Strategy Pattern
- Different parsers for different formats
- Pluggable validation strategies

### 4. Command Pattern
- CLI commands as discrete operations
- Easy to extend with new commands

## Key Design Decisions

### 1. Dictionary-based Storage
**Decision**: Use dict for task storage in TodoList
**Rationale**: O(1) lookups by ID, simple serialization
**Trade-off**: No ordering (use list() when needed)

### 2. Dataclass for Task
**Decision**: Use Python dataclass for Task model
**Rationale**: Built-in features (init, repr), immutability options
**Trade-off**: Python 3.11+ required

### 3. Regex-based Parsing
**Decision**: Use regex for metadata extraction
**Rationale**: Fast, flexible, no external dependencies
**Trade-off**: Complex patterns harder to maintain

### 4. Auto-save on Every Operation
**Decision**: Save to disk after each modification
**Rationale**: Never lose data, simple consistency model
**Trade-off**: Performance hit (acceptable for CLI app)

### 5. UUID for Task IDs
**Decision**: Use UUID4 for task identification
**Rationale**: Guaranteed uniqueness, no coordination needed
**Trade-off**: Not human-friendly (mitigated with partial ID matching)

## Error Handling Strategy

### Parser Layer
- Raise `ValueError` for invalid input
- Return `None` for optional fields
- Provide detailed error messages

### Service Layer
- Catch exceptions, return boolean success
- Print error messages for user feedback
- Never crash the application

### CLI Layer
- Try/except around all commands
- User-friendly error messages
- Graceful degradation

## Testing Strategy

### Unit Tests
- Each module tested independently
- Mock external dependencies
- Cover edge cases in most module

### Integration Tests
- Test component interactions
- End-to-end workflows
- Persistence verification

### Test Coverage
- Target: >90% coverage
- Critical paths: 100% coverage
- Focus on business logic

## Performance Considerations

### Time Complexity
- Add task: O(1)
- Get task: O(1)
- Delete task: O(1)
- List all: O(n)
- Filter: O(n)
- Search: O(n)

### Space Complexity
- Storage: O(n) where n = number of tasks
- No caching currently (not needed for CLI)

### Optimization Opportunities
1. Index tasks by tags for faster filtering
2. Cache search results
3. Lazy load from JSON
4. Batch save operations

## Extensibility Points

### Easy to Add
- New commands in CLI
- New regex patterns
- New validation rules
- New list filters

### Moderate Effort
- New storage backends (database, cloud)
- New input formats
- Recurring tasks
- Task dependencies

### Significant Refactoring
- Multi-user support
- Real-time sync
- Plugin system
- Web interface

## Security Considerations

### Current Implementation
- No authentication (single-user CLI)
- Local file storage only
- No network communication
- Input validation prevents injection

### Future Considerations
- Encrypt storage file
- Add user authentication
- Sanitize email addresses
- Rate limiting for operations

## Deployment

### Local Development
```bash
poetry install
poetry run python src/main.py
```

### Distribution
- PyPI package (future)
- Docker container (future)
- Standalone executable (PyInstaller)

## Maintenance

### Adding New Features
1. Create issue in GitHub
2. Create feature branch
3. Implement with tests
4. Update documentation
5. Create PR
6. Merge to main

### Bug Fixes
1. Create bug report issue
2. Write failing test
3. Fix bug
4. Verify test passes
5. Create PR

## Dependencies

### Production
- Python 3.11+
- python-dateutil (date parsing)

### Development
- pytest (testing)
- pytest-cov (coverage)
- black (formatting)
- flake8 (linting)
- mypy (type checking)

## Conclusion

This architecture balances:
- **Simplicity**: Easy to understand and modify
- **Modularity**: Components can be tested/changed independently
- **Extensibility**: New features can be added without major refactoring
- **Maintainability**: Clear separation of concerns
