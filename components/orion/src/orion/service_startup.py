import inspect, os

from nexus.core.application.logging import LoggingBootstrap
from orion.application.config.uvicorn import UvicornConfig
from orion.application.settings import app_logger
from orion.infrastructure.fast_api.service import SimpleFastAPIProfile

"""
What is Orion?

Orion is the main API for the prototype, containing only the essential
endpoints required for the challenge:

- Creation of Qdrant Clusters (Async) - returns a 202 HTTP Status Code
- Creation of API-KEYS to access newly created clusters (Sync) - returns a 201 
  HTTP Status Code

The API has been designed as closely as possible to mirror the current 
Qdrant Cloud product. These similarities are intentional, and any additional
endpoints have been deliberately omitted to keep the prototype as small and
focused as possible.
"""

if __name__ == "__main__":
   current_path = os.path.dirname(os.path.abspath(
      inspect.getfile(inspect.currentframe())))
   logging_file = os.path.join(
      f'{current_path}/../../../', 'logging.yaml')
   LoggingBootstrap.configure(logging_file)

   app_logger.info(f"Bootstrap: Initializing Orion service")

   # Simple FastAPI application for the prototype purposes
   service = SimpleFastAPIProfile(

      # Default Uvicorn Config, this can be modeled externally using dotenv files
      # or config files.
      settings=UvicornConfig()
   )

   service.run()
