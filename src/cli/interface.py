"""
Command-line interface for the todo application.
"""

import sys
from typing import Optional
from src.services.task_service import TaskService


class TodoCLI:
    """
    Interactive command-line interface for todo app.
    """
    
    def __init__(self):
        """Initialize CLI with task service."""
        self.service = TaskService()
        self.running = True
    
    def display_banner(self):
        """Display welcome banner."""
        print("\n" + "="*60)
        print("  SMART TODO APPLICATION")
        print("="*60)
        print(f"  Total: {self.service.count_all()} tasks | "
              f"Complete: {self.service.count_complete()} | "
              f"Incomplete: {self.service.count_incomplete()}")
        print("="*60 + "\n")
    
    def display_help(self):
        """Display help message with available commands."""
        help_text = """
Available Commands:
  add <task>          Add a new task (supports tags, priority, dates)
  list                List all tasks
  list incomplete     List incomplete tasks
  list complete       List complete tasks
  list --tag <tag>    List tasks by tag
  list --priority <p> List tasks by priority (high/medium/low)
  search <keyword>    Search tasks by keyword
  complete <id>       Mark task as complete
  incomplete <id>     Mark task as incomplete
  delete <id>         Delete a task
  update <id>         Update a task
  clear complete      Clear all completed tasks
  stats               Show statistics
  help                Show this help message
  exit                Exit the application

Examples:
  add Buy milk @shopping #high due:tomorrow
  list --tag work
  complete 1
  search meeting
        """
        print(help_text)
    
    def display_task(self, task, show_id=True):
        """
        Display a single task.
        
        Args:
            task: Task object to display
            show_id: Whether to show task ID
        """
        status = "✓" if task.is_complete else "○"
        
        # Build output
        output = f"[{status}] {task.description}"
        
        # Add metadata
        meta = []
        if task.tags:
            meta.append(f"Tags: {', '.join(task.tags)}")
        if task.priority:
            meta.append(f"Priority: {task.priority}")
        if task.due_date:
            meta.append(f"Due: {task.due_date}")
        if task.time:
            meta.append(f"Time: {task.time}")
        if task.assigned_to:
            meta.append(f"Assigned: {task.assigned_to}")
        
        if meta:
            output += "\n    " + " | ".join(meta)
        
        if show_id:
            output += f"\n    ID: {task.id[:8]}..."
        
        print(output)
        print()
    
    def display_tasks(self, tasks, title="Tasks"):
        """
        Display a list of tasks.
        
        Args:
            tasks: List of Task objects
            title: Title for the list
        """
        if not tasks:
            print(f"No {title.lower()} found.\n")
            return
        
        print(f"\n{title} ({len(tasks)}):")
        print("-" * 60)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. ", end="")
            self.display_task(task, show_id=True)
    
    def cmd_add(self, args):
        """
        Add a new task.
        
        Args:
            args: Task string from user input
        """
        if not args:
            print("Error: Task description required.\n")
            return
        
        task_string = ' '.join(args)
        task_id = self.service.add_task_from_string(task_string)
        
        if task_id:
            task = self.service.get_task(task_id)
            print("\n✓ Task added successfully!")
            self.display_task(task)
        else:
            print("\n✗ Failed to add task.\n")
    
    def cmd_list(self, args):
        """
        List tasks with optional filters.
        
        Args:
            args: Filter arguments
        """
        if not args:
            tasks = self.service.list_all()
            self.display_tasks(tasks, "All Tasks")
        
        elif args[0] == "incomplete":
            tasks = self.service.list_incomplete()
            self.display_tasks(tasks, "Incomplete Tasks")
        
        elif args[0] == "complete":
            tasks = self.service.list_complete()
            self.display_tasks(tasks, "Complete Tasks")
        
        elif args[0] == "--tag" and len(args) > 1:
            tag = args[1].lstrip('@')
            tasks = self.service.list_by_tag(tag)
            self.display_tasks(tasks, f"Tasks tagged '{tag}'")
        
        elif args[0] == "--priority" and len(args) > 1:
            priority = args[1]
            tasks = self.service.list_by_priority(priority)
            self.display_tasks(tasks, f"Tasks with priority '{priority}'")
        
        else:
            print("Error: Invalid list command. Use 'help' for usage.\n")
    
    def cmd_search(self, args):
        """
        Search tasks by keyword.
        
        Args:
            args: Search keyword
        """
        if not args:
            print("Error: Search keyword required.\n")
            return
        
        keyword = ' '.join(args)
        tasks = self.service.search_tasks(keyword)
        self.display_tasks(tasks, f"Search results for '{keyword}'")
    
    def cmd_complete(self, args):
        """
        Mark task as complete.
        
        Args:
            args: Task ID or partial ID
        """
        if not args:
            print("Error: Task ID required.\n")
            return
        
        task_id = self._find_task_id(args[0])
        if not task_id:
            print(f"Error: Task '{args[0]}' not found.\n")
            return
        
        success = self.service.mark_complete(task_id)
        if success:
            print(f"\n✓ Task marked as complete!\n")
        else:
            print(f"\n✗ Failed to mark task as complete.\n")
    
    def cmd_incomplete(self, args):
        """
        Mark task as incomplete.
        
        Args:
            args: Task ID or partial ID
        """
        if not args:
            print("Error: Task ID required.\n")
            return
        
        task_id = self._find_task_id(args[0])
        if not task_id:
            print(f"Error: Task '{args[0]}' not found.\n")
            return
        
        success = self.service.mark_incomplete(task_id)
        if success:
            print(f"\n✓ Task marked as incomplete!\n")
        else:
            print(f"\n✗ Failed to mark task as incomplete.\n")
    
    def cmd_delete(self, args):
        """
        Delete a task.
        
        Args:
            args: Task ID or partial ID
        """
        if not args:
            print("Error: Task ID required.\n")
            return
        
        task_id = self._find_task_id(args[0])
        if not task_id:
            print(f"Error: Task '{args[0]}' not found.\n")
            return
        
        # Confirm deletion
        task = self.service.get_task(task_id)
        print(f"\nDelete this task?")
        self.display_task(task, show_id=False)
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        
        if confirm == 'yes':
            success = self.service.delete_task(task_id)
            if success:
                print("\n✓ Task deleted!\n")
            else:
                print("\n✗ Failed to delete task.\n")
        else:
            print("\nDeletion cancelled.\n")
    
    def cmd_update(self, args):
        """
        Update a task interactively.
        
        Args:
            args: Task ID or partial ID
        """
        if not args:
            print("Error: Task ID required.\n")
            return
        
        task_id = self._find_task_id(args[0])
        if not task_id:
            print(f"Error: Task '{args[0]}' not found.\n")
            return
        
        task = self.service.get_task(task_id)
        print("\nCurrent task:")
        self.display_task(task, show_id=False)
        
        print("Enter new values (press Enter to keep current):\n")
        
        # Get new description
        new_desc = input(f"Description [{task.description}]: ").strip()
        
        # Get new priority
        new_priority = input(f"Priority [{task.priority}] (high/medium/low): ").strip()
        
        # Build updates
        updates = {}
        if new_desc:
            updates['description'] = new_desc
        if new_priority:
            updates['priority'] = new_priority
        
        if updates:
            success = self.service.update_task(task_id, **updates)
            if success:
                print("\n✓ Task updated!\n")
                updated_task = self.service.get_task(task_id)
                self.display_task(updated_task)
            else:
                print("\n✗ Failed to update task.\n")
        else:
            print("\nNo changes made.\n")
    
    def cmd_clear(self, args):
        """
        Clear tasks.
        
        Args:
            args: 'complete' to clear completed tasks
        """
        if args and args[0] == "complete":
            count = self.service.count_complete()
            if count == 0:
                print("\nNo completed tasks to clear.\n")
                return
            
            confirm = input(f"Clear {count} completed task(s)? (yes/no): ").strip().lower()
            if confirm == 'yes':
                self.service.clear_complete()
                print(f"\n✓ Cleared {count} completed task(s)!\n")
            else:
                print("\nCancelled.\n")
        else:
            print("Error: Use 'clear complete' to clear completed tasks.\n")
    
    def cmd_stats(self, args):
        """Display statistics."""
        total = self.service.count_all()
        complete = self.service.count_complete()
        incomplete = self.service.count_incomplete()
        overdue = len(self.service.list_overdue())
        
        print("\n" + "="*60)
        print("  STATISTICS")
        print("="*60)
        print(f"  Total tasks:      {total}")
        print(f"  Completed:        {complete}")
        print(f"  Incomplete:       {incomplete}")
        print(f"  Overdue:          {overdue}")
        
        if total > 0:
            completion_rate = (complete / total) * 100
            print(f"  Completion rate:  {completion_rate:.1f}%")
        
        print("="*60 + "\n")
    
    def _find_task_id(self, partial_id: str) -> Optional[str]:
        """
        Find full task ID from partial ID.
        
        Args:
            partial_id: Partial task ID (first few characters)
            
        Returns:
            Full task ID or None
        """
        all_tasks = self.service.list_all()
        for task in all_tasks:
            if task.id.startswith(partial_id):
                return task.id
        return None
    
    def process_command(self, command_line: str):
        """
        Process a command from user input.
        
        Args:
            command_line: Raw command string
        """
        if not command_line.strip():
            return
        
        parts = command_line.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        commands = {
            'add': self.cmd_add,
            'list': self.cmd_list,
            'search': self.cmd_search,
            'complete': self.cmd_complete,
            'incomplete': self.cmd_incomplete,
            'delete': self.cmd_delete,
            'update': self.cmd_update,
            'clear': self.cmd_clear,
            'stats': self.cmd_stats,
            'help': lambda _: self.display_help(),
            'exit': lambda _: self.exit_app(),
            'quit': lambda _: self.exit_app(),
        }
        
        if cmd in commands:
            try:
                commands[cmd](args)
            except Exception as e:
                print(f"\nError: {e}\n")
        else:
            print(f"\nUnknown command: '{cmd}'. Type 'help' for available commands.\n")
    
    def exit_app(self):
        """Exit the application."""
        print("\nGoodbye! 👋\n")
        self.running = False
    
    def run(self):
        """Main run loop."""
        self.display_banner()
        print("Type 'help' for available commands.\n")
        
        while self.running:
            try:
                command = input("> ").strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print("\n")
                self.exit_app()
            except EOFError:
                self.exit_app()


def main():
    """Entry point for CLI."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()