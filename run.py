""" Main program """

from create_app import create_app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        app.run()        # Activate server