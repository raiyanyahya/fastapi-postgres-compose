# fastapi-postgres-compose

This repository contains an advanced Todo API implementation, crafted with the Python programming language. The API leverages the FastAPI framework, renowned for its high performance and easy-to-use asynchronous features. Persistent data storage is handled by a PostgreSQL database, ensuring robust and scalable data management. The entire application stack is containerized using Docker Compose, facilitating straightforward local development, testing, and deployment across diverse server environments. The api supports user login and authentication. Manages token generation and expiration for secure sessions and is configured with a volume (postgres_data) to ensure that data remains intact across container restarts and redeployments.

## Local Deployment Instructions

Prior to local deployment, ensure Docker and Docker Compose are installed on your machine. This setup is vital for the seamless execution of the application in a containerized environment.

The application configuration relies on a set of environment variables for secure and flexible operations. These are as follows:

POSTGRES_USER: Specifies the username for the PostgreSQL database.
POSTGRES_PASSWORD: Sets the password for your PostgreSQL user.
POSTGRES_DB: Defines the name of your PostgreSQL database.
SECRET_KEY: A secure key utilized by the application, crucial for maintaining data integrity and security.
It is essential to define these environment variables before initiating the application either locally or in a production setting.

Execute the following commands in your terminal to clone the repository and launch the service stack:

```bash

git clone https://github.com/raiyanyahya/fastapi-postgres-compose.git
cd fastapi-postgres-compose
docker-compose up

```

Documentation pages are generated automatically from your FastAPI code, including all the routes, parameters, bodies, etc., leveraging the OpenAPI standards. They are extremely useful for both development and testing phases, providing a clear and interactive interface for your API's consumers.
FastAPI automatically generates and hosts interactive API documentation for your application. This is accessed by default at the `/docs endpoint of your application


## CI CD Workflow

The "Build Tox Test Compose" GitHub Action is designed for automated integration and testing of Python-based applications on docker compose. This workflow is triggered by activities such as pull requests and pushes to the master branch, and it can also be manually initiated. It consists of sequential jobs that set up the environment, build the project, run Tox for multi-environment testing, and conduct application tests within Docker containers.

### Workflow Activation Triggers
Pull Request Events: Activates when a pull request is submitted to the master branch.
Push Events: Triggers when new commits are pushed to the master branch.
Manual Dispatch: Allows the workflow to be started manually from the GitHub interface.
Job Descriptions

 #### Job 1: Build
The initial job prepares the project for testing by setting up the Python environment and installing project dependencies.

Environment: The job runs on the latest Ubuntu virtual environment provided by GitHub Actions.

Key Operations:

Repository Checkout: Clones the repository's code into the GitHub Actions runner.
Python Setup: Installs Python 3.9 to ensure consistency with the project's runtime environment.
Dependency Installation: Installs required Python packages from requirements.txt using pip.

 #### Job 2: Tox
Following a successful build, the Tox job initiates to validate the application across different environments, ensuring compatibility and identifying any environment-specific issues.

Dependencies: This job depends on the completion of the Build job.

Environment: Executes on the latest Ubuntu virtual environment.

Key Operations:

Repository Checkout: Re-fetches the codebase to ensure the latest version is tested.
Python Setup: Configures the runner with Python 3.9, aligning with the build environment.
Tox Execution: Installs Tox and runs tests across multiple environments, specified within the Tox configuration.

 #### Job 3: Test
This final job uses Docker to create a realistic service environment for end-to-end testing, essential for verifying the application's operational behavior.

Dependencies: Activates after the Tox job finishes successfully.

Environment: Utilizes the latest Ubuntu virtual machine.

Key Operations:

Repository Checkout: Ensures the most current version of the code is used for testing.
Docker Environment Setup: Prepares Docker containers as specified by the project's Docker Compose configurations.
Service Initialization: Boots up the service stack, applying environment variables for the testing context.
Health Check and Endpoint Testing: Executes a delay to allow services to initialize, followed by a series of curl requests to validate the responsiveness and functionality of the application endpoints.
Clean-up: Terminates and removes all services started by Docker Compose to maintain a clean slate.


## License
MIT

