"""Admin credential management script for Portfolio Engine.

Allows setting or updating the superuser administrator email, password, and name
either via command-line arguments or securely through interactive prompts.

Usage:
  python3 scripts/set_admin.py --email admin@example.com --password YourPassword123!
  python3 scripts/set_admin.py  (interactive prompt with secure hidden password input)
"""

import argparse
import getpass
import sys
from pathlib import Path

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def set_admin_credentials(
    email: str,
    password: str,
    full_name: str | None = None,
) -> None:
    db = SessionLocal()
    try:
        # Check for existing superuser first, or matching email
        user = db.query(User).filter(User.is_superuser.is_(True)).first()
        if not user:
            user = db.query(User).filter(User.email == email).first()

        if user:
            user.email = email
            user.hashed_password = hash_password(password)
            user.is_active = True
            user.is_superuser = True
            if full_name:
                user.full_name = full_name
            db.commit()
            db.refresh(user)
            print("✓ Successfully updated administrator account:")
        else:
            user = User(
                email=email,
                hashed_password=hash_password(password),
                full_name=full_name or "Yahaya Khalid",
                is_active=True,
                is_superuser=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("✓ Successfully created administrator account:")

        print(f"  • User ID: {user.id}")
        print(f"  • Email:   {user.email}")
        print(f"  • Name:    {user.full_name}")
        print(f"  • Role:    Superuser (Active)")
        print("✓ Password successfully updated and encrypted with Argon2.")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set or update Portfolio Engine administrator credentials.",
    )
    parser.add_argument(
        "--email",
        type=str,
        help="Administrator email address.",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="New administrator password.",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Administrator full name.",
    )

    args = parser.parse_args()

    email = args.email
    if not email:
        email = input("Enter admin email (e.g. khalidzak21@gmail.com): ").strip()
        if not email:
            print("Error: Email cannot be empty.", file=sys.stderr)
            sys.exit(1)

    password = args.password
    if not password:
        password = getpass.getpass("Enter new admin password: ").strip()
        if not password:
            print("Error: Password cannot be empty.", file=sys.stderr)
            sys.exit(1)
        confirm = getpass.getpass("Confirm new admin password: ").strip()
        if password != confirm:
            print("Error: Passwords do not match.", file=sys.stderr)
            sys.exit(1)

    if len(password) < 8:
        print("Warning: Password is shorter than 8 characters. Consider a stronger password.", file=sys.stderr)

    set_admin_credentials(email=email, password=password, full_name=args.name)


if __name__ == "__main__":
    main()
