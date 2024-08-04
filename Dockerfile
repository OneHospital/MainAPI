FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the FastAPI application code
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt
RUN pip install -r plugins/plugins.txt

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["fastapi", "run"]
