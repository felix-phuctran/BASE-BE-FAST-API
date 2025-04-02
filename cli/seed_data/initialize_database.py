from cli_service_impl import CliServiceImpl
from sqlalchemy.orm import Session

from database import SessionLocal  # Import session DB


def run_cli():
    # 1️⃣ Create database session
    db: Session = SessionLocal()

    # 2️⃣ Initialize CLI service
    cli_service = CliServiceImpl(db)

    # 3️⃣ Call each CLI function to run
    print("1. Initialize DB")
    print("2. Initialize User")
    print("3. Exit")

    choice = input("Select operation (1-3): ")

    if choice == "1":
        result = cli_service._initialize_db()
    elif choice == "2":
        result = cli_service._initialize_user(db)
    else:
        print("Exit program.")
        return

    print(f"✅ Result: {result}")


if __name__ == "__main__":
    run_cli()
