import base64, os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from nexus.core.domain.ports import DBClusterRepository
from orion.application.settings import app_logger


class DBaaSApiKeyService:
    """
    This application service is responsible for generating salt-hashing based
    API keys for provisioned Qdrant DB clusters, which will be consumable by the
    reverse-proxy GateKeeper.
    """

    def __init__(self,  db_cluster_repository: DBClusterRepository):
        self.db_cluster_repository = db_cluster_repository

    def create_api_key(self, db_cluster_id: str) -> str:
        """
        Retrieves the API key of a previously provisioned Qdrant cluster and uses
        it as a secret to generate a salt-hashing key similar to those used in
        Qdrant's private cloud.

        :param db_cluster_id: The unique identifier of the DB cluster.
        :return: A salt-hashing based API key.
        """

        # Not Implemented: Validation when the ID is incorrect or non-existent.
        db_cluster = self.db_cluster_repository.get_by_id(
            db_cluster_id=db_cluster_id
        )

        app_logger.debug(f"{self.__class__.__name__}: Retrieving API key "
                         f"for {db_cluster_id} from the DBClusterRepository.")

        return self._generate_salt_hashing_api_key(
            secret=db_cluster.db_cluster_api_key)

    def _generate_salt_hashing_api_key(self, secret: str) -> str:
        """
        Based on a secret (in our case, the 32-character API key
        provisioned for the Qdrant cluster), generate a salt-hashing key
        that the GateKeeper component can validate.

        Key concepts:

        - 'Salt' is a random byte sequence used to protect and enhance
          passwords or keys in cryptographic processes. Here, the first 16
          bytes of the decoded data are extracted as the salt.

        - PBKDF2 (Password-Based Key Derivation Function 2) is a function
          used to derive keys from a password and salt. It uses a hash
          function, in this case SHA256, and is widely used in the industry.

        :param secret: The secret used to generate the API key
                       (the Qdrant cluster's API key).
        :return: A base64-encoded salt-hashing based API key.
        """

        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(secret.encode())
        api_key = base64.urlsafe_b64encode(salt + key).decode().rstrip('=')

        app_logger.debug(f"{self.__class__.__name__}: Generated salt-hashing "
                         f"api-key: {api_key[:5]}")

        return api_key