"""File with constants used in the SDK."""

# Constant used to add extra timeout to token calculation.
# If the token expiration is lower than this constant, request a new token.
TOKEN_EXTRA_TIME = 10

# REST API only accepts 1MB payload
REST_API_MAXIMUM_CHUNK_SIZE = 1048576
