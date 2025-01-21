# Build requirements
FROM python:3.11-alpine AS requirements

# Install Poetry and export plugin
RUN pip install poetry \
    && poetry self add poetry-plugin-export

# Copy only necessary Poetry files
COPY ./pyproject.toml ./poetry.lock /
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev

# Final image
FROM python:3.11-alpine

# Install required utilities and certifi for CA certificates
RUN apk add --no-cache shadow \
    && pip install --upgrade certifi

# Add a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set working directory
WORKDIR /home

# Copy requirements from the requirements stage to the backend directory
COPY --from=requirements requirements.txt /home/app/

# Install dependencies
RUN python3 -m pip install --no-cache-dir --upgrade -r /home/app/requirements.txt

# Copy application code
COPY ./pyproject.toml /home/
COPY ./app /home/app

# Change ownership and switch user
RUN chown -R appuser:appgroup /home
USER appuser

# Start Uvicorn
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
