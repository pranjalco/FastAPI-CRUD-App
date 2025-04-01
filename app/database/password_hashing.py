import bcrypt


# Function for creating hash password
def create_hash_password(password: str) -> str:
    """Create hash password using a bcrypt"""
    salt_gen = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt_gen)
    return hashed_password.decode('utf-8')

















