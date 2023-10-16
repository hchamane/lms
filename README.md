# Team Unity - LMS application

## Welcome

This project is the repository for the LMS application.

## Running with docker

Make sure you have docker running locally, otherwise download the desktop application from the docker [website](https://www.docker.com/products/docker-desktop/).

Spin up compose:
```bash
docker compose up
```

Create a launch.json file inside .vscode if you want hot-reload and debugging:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask via Docker",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "0.0.0.0",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ]
        }
    ]
}
```

You're good to go 🎉
<br>
You can now select Flask via Docker in the Run And Debug tab and start debugging away 🤗


Stop docker-compose:

```bash
docker-compose down -v --remove-orphans
```

## Running without docker-compose
### Prerequisites

Make sure you have python 3.11 installed and running on your computer, otherwise download the latest version either
via pyenv or via the python [website](https://www.python.org/downloads/release/python-3116/)

### Install Python via pyenv
Click [here](https://github.com/pyenv/pyenv#basic-github-checkout) and follow step 2, 3 and 4

Install python (we currently run 3.11.6) and make it your default version:

```bash
pyenv install 3.11.6
pyenv global 3.11.6
```

Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the python requirements:

```bash
python3 -m pip install -r requirements.txt -r tests/requirements.txt
```

### Run the app

You should now be able to run the app locally:

<details>
<summary>Visual Studio Code configuration</summary>

Create a new `launch.json` inside `.vscode`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "lms/app.py",
                "FLASK_ENV": "development",
                "DEBUG": "1"
            },
            "args": [
                "run",
                "--port=5002"
            ],
            "jinja": true
        }
    ]
}
```

You'll then be able to start the application via the debugger

The app should be running on http://127.0.0.1:5002

</details>

<details>
<summary>Other editors</summary>

```bash
flask --app lms.app run
```

The app should be running on http://127.0.0.1:5000
</details>

<br>
