## FastAPI Docker Template

This project provides a template for running a FastAPI application inside a Docker container, with modern Python dependency management using uv and pyproject.toml.

### Features
- FastAPI app with a simple health check endpoint
- Dockerfile for development and production
- uv for fast dependency management
- Example Makefile for build and up commands

### Quick Start
1. Build the Docker image:
	```sh
	make build-dev
	```
2. Start the development container:
	```sh
	make dev-up
	```

The app will be available at http://localhost:8080.

### Project Structure
- `src/app/main.py`: FastAPI app entry point
- `provision/Dockerfile.dev`: Development Dockerfile
- `provision/entrypoint.sh`: Entrypoint script
- `pyproject.toml`: Python dependencies

### Health Check
Visit `/` to check if the app is running:
```
GET /
Response: "ok"
```
