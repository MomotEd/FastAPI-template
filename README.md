# FastAPI Template

This is a template project for FastAPI with Docker and Docker-compose support.

## Getting Started

### Prerequisites

Make sure you have Docker and Docker-compose installed on your system.

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker-compose Installation Guide](https://docs.docker.com/compose/install/)

### Running the Project

1. Clone the repository:

   ```bash
   git clone git@github.com:MomotEd/FastAPI-template.git
   cd fastAPI-template

2. Build and run the Docker containers. This command will build the Docker image and start the FastAPI application:

   ```bash
   docker-compose up --build


3. Access the FastAPI application:

    Open your browser and go to http://localhost:8000 to access the FastAPI Swagger documentation.



#### Additionally, here is a basic Makefile that you can include in your project:

```make
# Makefile for FastAPI Template

.PHONY: build run stop clean

build:
	docker-compose build

run:
	docker-compose up

stop:
	docker-compose down

clean:
	docker-compose down --volumes --remove-orphans
