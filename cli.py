import click
import requests

API_BASE_URL = "http://localhost:5001"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx) -> None:
    """LMS Command Line Interface"""

    click.echo("If this is the first time you use this application, you can use the admin credentials")
    click.echo("username=admin, password=admin")
    click.echo("")

    while True:
        click.echo("Available actions:")
        click.echo("1. Login to the app")
        click.echo("2. Register a new user")
        click.echo("3. List all current users")
        click.echo("4. Create a Module")
        click.echo("5. Create an Assignment")
        click.echo("6. Submit a Grade")
        click.echo("7. View Grades as a Student")
        click.echo("8. Logout")
        click.echo("9. Exit")

        choice = click.prompt("Please select an action", type=int)

        if choice == 1:
            login()
        elif choice == 2:
            register_user()
        elif choice == 3:
            list_all_users()
        elif choice == 4:
            create_module()
        elif choice == 5:
            create_assignment()
        elif choice == 6:
            submit_grade()
        elif choice == 7:
            view_grades()
        elif choice == 8:
            logout()
        elif choice == 9:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice. Please select again.")


def register_user() -> None:
    """Register a new user."""
    username = click.prompt("Please enter a username", type=str)
    password = click.prompt("Please enter a password", type=str, hide_input=True)
    role = click.prompt("Please enter a role (Admin, Teacher, Student)", type=str)
    first_name = click.prompt("Please enter your first name", type=str)
    last_name = click.prompt("Please enter your last name", type=str)
    email = click.prompt("Please enter your email", type=str)
    click.echo("")

    user_data = {
        "username": username,
        "password": password,
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }

    response = requests.post(f"{API_BASE_URL}/users/create", json=user_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


def login() -> None:
    """Login to the system"""
    username = click.prompt("Please enter a username", type=str)
    password = click.prompt("Please enter a password", type=str, hide_input=True)
    click.echo("")

    user_data = {"username": username, "password": password}

    response = requests.post(f"{API_BASE_URL}/login", json=user_data)

    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


def list_all_users() -> None:
    """List all available users in the system"""

    response = requests.get(f"{API_BASE_URL}/users/list")
    data = response.json()

    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        start_number = 1

        click.echo("")
        click.echo("Current users in the system:")
        for user in data:
            click.echo(
                f'- User {start_number}. first name: {user.get("first_name")}, '
                f'last name: {user.get("last_name")}, username: {user.get("username")}'
            )
            start_number += 1

    click.echo("")


def create_module() -> None:
    """Create a new module."""
    title = click.prompt("Please enter the module title", type=str)
    description = click.prompt("Please enter the module description", type=str)
    click.echo("")

    module_data = {"title": title, "description": description}

    response = requests.post(f"{API_BASE_URL}/modules/create", json=module_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


def create_assignment() -> None:
    """Create a new assignment."""
    title = click.prompt("Please enter the assignment title", type=str)
    description = click.prompt("Please enter the assignment description", type=str)
    module_id = click.prompt("Please enter the module ID", type=int)
    due_date = click.prompt("Please enter the due date (YYYY-MM-DD)", type=str)
    click.echo("")

    assignment_data = {"title": title, "description": description, "module_id": module_id, "due_date": due_date}

    response = requests.post(f"{API_BASE_URL}/assignments/create", json=assignment_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


def submit_grade() -> None:
    """Submit a grade."""
    student_id = click.prompt("Please enter the student ID", type=int)
    assignment_id = click.prompt("Please enter the assignment ID", type=int)
    score = click.prompt("Please enter the score", type=float)
    click.echo("")

    grade_data = {"student_id": student_id, "assignment_id": assignment_id, "score": score}

    response = requests.post(f"{API_BASE_URL}/grades/submit", json=grade_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


def view_grades() -> None:
    """View all grades as a student."""
    response = requests.get(f"{API_BASE_URL}/grades/view")
    data = response.json()
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        click.echo("")
        click.echo("Your grades:")
        for grade in data:
            click.echo(f'- Assignment ID: {grade.get("assignment_id")}, Score: {grade.get("score")}')
    click.echo("")


def logout() -> None:
    """Log out of the app"""
    click.echo("")
    response = requests.put(f"{API_BASE_URL}/logout")
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


if __name__ == "__main__":
    cli()
