from app import app


@app.cli.command("setup-db")
def setup_database():
    # Execute your Flask-Migrate commands as subprocesses
    import subprocess

    db_init = subprocess.run(
        ["flask", "db", "init"], capture_output=True, text=True
    )
    if db_init.returncode != 0:
        print("Error during 'flask db init':\n{}".format(db_init.stderr))
        return

    db_migrate = subprocess.run(
        ["flask", "db", "migrate", "-m", "users and gameplay tables"],
        capture_output=True,
        text=True,
    )
    if db_migrate.returncode != 0:
        print("Error during 'flask db migrate':\n{}".format(db_migrate.stderr))
        return

    db_upgrade = subprocess.run(
        ["flask", "db", "upgrade"], capture_output=True, text=True
    )
    if db_upgrade.returncode != 0:
        print("Error during 'flask db upgrade':\n{}".format(db_upgrade.stderr))
        return

    print("Database setup complete.")
