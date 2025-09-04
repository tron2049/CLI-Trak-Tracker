import argparse
from html import parser
from api import TaskManager
#Command Line user input

def cli_input():

    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="commands")
    
    list_tasks = subparsers.add_parser("list", help="List Tasks")
    list_tasks.add_argument("id",type=int,nargs="?", help="ID of the task to list")
    list_tasks.add_argument("--status", choices=["completed", "incomplete"], help="Status of the task")
    list_tasks.set_defaults(func=handle_lists)
    
    add_task = subparsers.add_parser("add", help="Add Task")
    add_task.add_argument("title", help="Title of the task")
    add_task.set_defaults(func=handle_add)

    del_task = subparsers.add_parser("delete", help="Delete Task")
    del_task.add_argument("id", type=int, help="ID of the task to delete")
    del_task.set_defaults(func=handle_delete)
    
    update_task = subparsers.add_parser("update", help="Update Task")
    update_task.add_argument("id",type=int, help="ID of the task to update")
    update_task.add_argument("-n", "--name", type=str,nargs="?", help="Update name Task")
    update_task.add_argument("--status",choices=["complete","incompleted"],nargs="?", help="Update state of Task")
    update_task.set_defaults(func=handle_update)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


task_manager = TaskManager("Tasks.json")

def format_task(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print(f"{'ID':<5}{'Name':<20}{'Status':<12}{'Date'}")
    print("-" * 60)
        
    for task in tasks:
        print(f"{task["id"]:<5}{task['name']:<20}{task['status']:<12}{task['date']}")

def handle_lists(args):
    tasks = task_manager.list_tasks(args.id, args.status)
    if tasks:
        return format_task(tasks)
    else:
        print("No tasks found.")

def handle_add(args):
    new_task = task_manager.add_task(args.title)
    print("Task added:")
    format_task([new_task])

def handle_delete(args):
    del_tasks = task_manager.delete_task(args.id)
    if del_tasks:
        print("Task deleted")
        format_task([del_tasks])
    else:
        print("Task not found.")
        
def handle_update(args):
    updated = task_manager.update_task(
        id=args.id,   
        title=args.name,   
        status=args.status 
    )
    if updated:
        print("Task updated")
        format_task([updated])
    else:
        print("Task not found.")



