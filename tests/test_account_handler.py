from server.account_handler import register_user, user_authentification, get_user_id

#Test user registration
user_id = register_user("test_user", "secure_password")
print(f"Test Registration: {'Success' if user_id else 'Failed'}")

#Test authentication
auth_success = user_authentification("test_user", "secure_password")
auth_failure = user_authentification("test_user", "wrong_password")

print(f"Test Authentication (Correct Password): {'Success' if auth_success else 'Failed'}")
print(f"Test Authentication (Wrong Password): {'Success' if not auth_failure else 'Failed'}")

#Test getting the user ID
retrieved_user_id = get_user_id("test_user")
print(f"Test User ID Retrieval: {'Success' if retrieved_user_id else 'Failed'}")
