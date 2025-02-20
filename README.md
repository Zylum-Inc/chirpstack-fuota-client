# Chirpstack Client

This client is used by the Thin application server for interacting with Chirpstack and FUOTA server.

## Local Development

- **Create and Set env variables in `.env` file**:

  Example:

  ```sh
  SERVER_ADDRESS="localhost:8080"
  API_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6ImJjNjhjZTY1LWM2YjItNDM0MS1hZjA5LTJkZGZlYjA4YzZlZSIsInR5cCI6ImtleSJ9.I5H7U1XZhOIZ2JKWUHkRwIH0Z8ChlvjeZKm1Owetdbk"
  FUOTA_SERVER_ADDRESS="localhost:8070"
  ```

- **Install dependencies and setup virtual env**:

> [!NOTE]
> Poetry is required! install it from [here](https://python-poetry.org/docs/#installation).

```sh
make install
```

- **Format and lint codebase**:

  ```sh
  make check
  ```

- **Execute Basic [Examples](./examples/basic.py)**:

  ```sh
  make basic_example
  ```
