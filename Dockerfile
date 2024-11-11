# Use the base image (e.g., Miniconda or Mambaforge)
FROM condaforge/mambaforge:latest

# Set work directory
WORKDIR /usr/src/app

# Copy the environment file
COPY environment.yaml .

# Create the Conda environment
RUN mamba env create -f environment.yaml

# Activate the environment
SHELL ["conda", "run", "-n", "playlette", "/bin/bash", "-c"]

# Copy the application code
COPY . .

# Expose ports
EXPOSE 5000 8888

# Copy and set permissions for the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start the application
CMD ["/start.sh"]
