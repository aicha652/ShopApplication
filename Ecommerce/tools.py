from werkzeug.security import generate_password_hash, check_password_hash



def hash_pass(password):
    password_hash = generate_password_hash(password)
    return password_hash

def verify_pass(provided_password, stored_password):
    pwhash = stored_password
    password = provided_password
    return check_password_hash(pwhash, password)