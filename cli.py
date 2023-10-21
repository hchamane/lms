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
        click.echo("3. Exit")

        choice = click.prompt("Please select an action", type=int)

        if choice == 1:
            login()
        elif choice == 2:
            register_user()
        elif choice == 3:
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


if __name__ == "__main__":
    cli()
