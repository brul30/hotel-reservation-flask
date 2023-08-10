# Hotel Reservation Flask

Welcome to the **Hotel Reservation Flask** project! Follow these steps to set up your Python development environment and run the project locally.

## Prerequisites

- [Python](https://www.python.org/downloads/) installed on your system.
  
## Getting Started

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/brul30/hotel-reservation-flask
    cd hotel-reservation-flask
    ```

2. Make sure you have Flask and SQLAlchemy installed:

   ```bash
   pip install Flask Flask-SQLAlchemy
   ```

4. Create a Virtual Environment:

    For Python 3.3+:

    ```bash
    python3 -m venv venv
    ```

    Alternatively, you can use `virtualenv`:

    ```bash
    pip install virtualenv  # If virtualenv is not installed
    virtualenv venv
    ```

5. Activate the Virtual Environment:

    On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

    On Windows:

    ```bash
    venv\Scripts\activate
    ```

6. Install Python Dependencies:

    ```bash
    pip install -r requirements.txt
    ```
7. Create the database:

    ```bash
    flask shell
    from src.extension import db
    db.create_all()
    exit()
    ```

8. Run the Application:

    ```bash
    flask run
    ```

9. Open your web browser and navigate to `http://localhost:3000` to see the application in action.




## Deactivate the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
