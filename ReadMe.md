# fastapi-postgres-compose

This repository contains an Todo API implementation, built with the Python programming language. The API leverages the FastAPI framework, renowned for its high performance and easy-to-use asynchronous features. Persistent data storage is handled by a PostgreSQL database, ensuring robust and scalable data management. The entire application stack is containerized using Docker Compose, facilitating straightforward local development, testing, and deployment across diverse server environments. The api supports user login and authentication. Manages token generation and expiration for secure sessions and is configured with a volume (postgres_data) to ensure that data remains intact across container restarts and redeployments.

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

## Deploy to a on-premise server

To deploy this Docker Compose application to an on-premise server, you can follow the below steps:

1.Transfer files: Use scp to copy the Docker Compose files (docker-compose.yml), environment variables file (.env), and the source code (app/ directory) to the server. 
2.SSH into the server: Use ssh to connect to the server.
3.Navigate to the destination: Change directory to the location where the files were transferred on the server.
4.Build and start the application: Use docker-compose to build and start the application in detached mode (-d) with the --build option to ensure that the latest changes are included.
5.Monitor logs: Use docker-compose logs -f to monitor the logs and ensure that the application starts up successfully.

Here's a basic script that outlines these steps. 

```sh
#!/bin/bash

# Transfer Docker Compose files and source code to the server
scp -r docker-compose.yml app/ user@example.com:/app

# SSH into the server
ssh user@example.com << 'EOF'

# Navigate to the directory containing Docker Compose files
cd /app

# Build and start the application using Docker Compose
docker-compose up -d --build

# Monitor logs to ensure successful startup
docker-compose logs -f

EOF

```

Replace user@example.com with the SSH username and IP address or hostname of your on-premise server. Adjust the paths and commands as needed based on your specific setup.

Remember to make the script executable (chmod +x deploy.sh) before running it. Additionally, ensure that SSH key-based authentication is properly set up to allow seamless SSH access to the on-premise server without requiring manual password input.

## CI CD Workflow

The "Build Tox Test Compose" GitHub Action is designed for automated integration and testing of Python-based applications on docker compose. This workflow is triggered by activities such as pull requests and pushes to the master branch, and it can also be manually initiated. It consists of sequential jobs that set up the environment, build the project, run Tox for multi-environment testing, and conduct application tests within Docker containers.

#### Workflow Activation Triggers
Pull Request Events: Activates when a pull request is submitted to the master branch.
Push Events: Triggers when new commits are pushed to the master branch.
Manual Dispatch: Allows the workflow to be started manually from the GitHub interface.
Job Descriptions

#### Job 1: Build
The initial job prepares the project for testing by setting up the Python environment and installing project dependencies.

#### Job 2: Tox
Following a successful build, the Tox job initiates to validate the application across different environments, ensuring compatibility and identifying any environment-specific issues.

#### Job 3: Test
This final job uses Docker to create a realistic service environment for end-to-end testing, essential for verifying the application's operational behavior.

Clean-up: Terminates and removes all services started by Docker Compose to maintain a clean slate.


## License
MIT

