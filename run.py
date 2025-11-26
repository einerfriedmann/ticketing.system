# This file initialises and runs the Flask application. It sets up the app context, creates the db tables and provides the shell context.

from app import create_app
from app import db
from app.models import User, Ticket, Comment

# Creates the Flask application instance using the factory function
app = create_app()

# Defines a shell context for the Flask Command Line Interface
@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Ticket': Ticket, 'Comment': Comment}

if __name__ == '__main__':
    # This makes sure the application context is active for database operations
    app.run()