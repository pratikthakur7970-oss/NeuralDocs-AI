from Auth.auth_manager import (
    init_db,
    get_connection,
    promote_user_to_admin,
    DB_PATH
)

from contextlib import closing

email = "sanu85755@gmail.com"

init_db()

print("\nDATABASE PATH:")
print(DB_PATH)

with closing(get_connection()) as conn:
    user = conn.execute(
        "SELECT id, full_name, email, role FROM users WHERE email = ?",
        (email,)
    ).fetchone()

if user is None:
    print("\nERROR: User not found in this database.")

else:
    print("\nCURRENT USER:")
    print(dict(user))

    success = promote_user_to_admin(email)

    print("\nPROMOTION RESULT:", success)

    with closing(get_connection()) as conn:
        updated = conn.execute(
            "SELECT id, full_name, email, role FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    print("\nUPDATED USER:")
    print(dict(updated) if updated else "NOT FOUND")