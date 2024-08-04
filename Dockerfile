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

# Check if plugins/plugins.txt exists and install plugins if it does
RUN if [ -f plugins/plugins.txt ]; then pip install -r plugins/plugins.txt; fi

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["fastapi", "run"]
