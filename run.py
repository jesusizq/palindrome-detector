from app import create_app
from flask_migrate import Migrate, upgrade

app = create_app()
migrate = Migrate(app)

if __name__ == "__main__":
    app.run()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
