import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from gatekeeper.application.settings import app_logger


class ApiKeyEnforcingService:
    """
    This Domain Service provides a service to validate api-keys against a known
    secret. The known secret is the api-key configured in the Qdrant cluster.
    Since Qdrant does not have a mechanism to generate api-keys at the
    collection level or associated with a specific user, they are at the cluster
    level.
    """

    @staticmethod
    def is_valid_api_key(api_key: str, secret: str) -> bool:
        """
        Validates the provided api-key using the Python cryptography module.

        Key components:

        'Salt' is a random byte sequence used to protect and enhance
        passwords or keys in cryptographic processes. Here, the first 16
        bytes of the decoded data are extracted as the salt.

        PBKDF2 (Password-Based Key Derivation Function 2) is a function
        used to derive keys from a password and salt. It uses a hash
        function, in this case SHA256, and is widely used in the industry.

        :param api_key: The api-key to verify, encoded in base64.
        :param secret: The secret used to generate the api-key
                       (the Qdrant cluster's api-key).
        :return: Boolean indicating whether the api-key is valid or not.
        """

        try:
            decoded_data = base64.urlsafe_b64decode(api_key + '==')
            salt = decoded_data[:16]
            key_original = decoded_data[16:]
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,  # Similar length of Qdrant Cloud api-keys.
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            kdf.verify(secret.encode(), key_original)
            app_logger.debug(
                f"{ApiKeyEnforcingService.__class__.__name__}: Validating ApiKey "
                f"Salt Hashing Api-Key: {api_key} using the the Qdrant API as "
                f"the secret: {secret}")
            return True
        except Exception:
            return False