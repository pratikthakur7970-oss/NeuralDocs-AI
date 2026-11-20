from Auth.auth_manager import (
    init_db,
    promote_user_to_admin
)

init_db()

email = input("Enter your registered email: ").strip()

success = promote_user_to_admin(email)

if success:
    print("SUCCESS: Admin role assigned!")
else:
    print("ERROR: User not found!")