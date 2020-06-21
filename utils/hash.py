import hashlib
import uuid

__all__ = [
    'hash',
    'generate_username',
    'generate_password'
]


def hash(text):
    """Make a hash of the text

    :param text: text to make the hash
    :returns: hashed version of the text
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def generate_username():
    """Generate a new password.

    :returns: new username
    """
    return str(uuid.uuid1())


def generate_password():
    """Generate a random password.

    :returns: random password
    """
    return hash(str(uuid.uuid1()))
