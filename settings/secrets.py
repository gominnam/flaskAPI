from google.cloud import secretmanager

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/minjunko/Downloads/dunkinguys-ad0fb2c23505.json"


def read_secret(secret_id, version_id="latest"):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/dunkinguys/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')