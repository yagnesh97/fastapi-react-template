# FastAPI + React TypeScript Template

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg?logo=typescript)](https://www.typescriptlang.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-6-47A248.svg?logo=mongodb)](https://www.mongodb.com)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg?logo=redis)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-🐋-2496ED.svg?logo=docker)](https://www.docker.com)
[![Poetry](https://img.shields.io/badge/Poetry-1.6-60A5FA.svg?logo=poetry)](https://python-poetry.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A modern web application template using FastAPI for the backend API, React TypeScript for the frontend, MongoDB as the database, and Redis for caching.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Development Environment](#development-environment)
  - [Docker Only Setup](#docker-only-setup)
  - [Hybrid Setup](#hybrid-setup)
- [Development Commands](#development-commands)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)

## Prerequisites

### Python Setup

1. Install Python 3.11

   - Download from [Python Official Website](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. Install Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Verify installation: `poetry --version`

### Node.js Setup

1. Install Node.js

   - Download from [Node.js Official Website](https://nodejs.org/)
   - Verify installation: `node --version`

2. Install Yarn
   ```bash
   npm install -g yarn
   ```
   Verify installation: `yarn --version`

### Docker Setup

1. Install Docker and Docker Compose
   - Follow instructions at [Docker Official Documentation](https://docs.docker.com/get-docker/)
   - Verify installation:
     ```bash
     docker --version
     docker-compose --version
     ```

## Project Setup

### Environment Configuration

1. Backend Environment Setup

   ```bash
   cd backend
   cp .env-example .env
   ```

   Configure the following variables in `.env`:

   ```plaintext
   ENVIRONMENT=production
   MONGO_URI=mongodb://foo:bar@localhost:27017/  # Use 'mongo' as host if not working
   MONGO_DB=database
   REDIS_HOST=localhost  # Use 'redis' as host if not working
   REDIS_PASSWORD=password
   JWT_SECRET_KEY=secret
   ```

2. Database Environment Setup
   ```bash
   cd database
   cp .env-example .env
   ```
   Configure the following variables in `.env`:
   ```plaintext
   MONGO_INITDB_ROOT_USERNAME=username
   MONGO_INITDB_ROOT_PASSWORD=password
   MONGO_INITDB_DATABASE=database
   MONGO_INITDB_ROOT_EMAIL=user@example.com
   REDIS_PASSWORD=password
   ```

## Development Environment

### Docker Only Setup

Run the entire stack using Docker:

```bash
docker-compose -f docker-compose.yml up --build -d
```

### Hybrid Setup

Run only MongoDB and Redis in Docker, with local development servers:

1. Start Required Services

   ```bash
   docker-compose -f docker-compose.yml up mongo redis --build -d
   ```

2. Setup Backend

   ```bash
   cd backend
   poetry install
   ./cmd.sh start  # Alternative: poetry run python -m app.main
   ```

3. Setup Frontend
   ```bash
   cd frontend
   yarn install
   yarn start
   ```

## Development Commands

### Code Formatting

#### Format backend code:

```bash
cd backend
./cmd.sh format
```

#### Format frontend code:

```bash
cd frontend
yarn lint
```

### Service URLs

- Backend API: `http://localhost:8000`
- Frontend Application: `http://localhost:3000`

## Production Deployment

Deploy the entire stack for production:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## API Documentation

When the backend is running, access the API documentation at:

- Swagger UI: `http://localhost:8000`
- ReDoc: `http://localhost:8000/redoc`
