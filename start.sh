# #!/bin/bash

# # Activate the Conda environment
# source /opt/conda/etc/profile.d/conda.sh
# conda activate playlette

# # Export environment variables from .env
# set -o allexport
# source /usr/src/app/.env
# set +o allexport

# # Start Flask in the background
# python app/main.py &

# # Start Jupyter Lab
# jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

#!/bin/bash

# Convert line endings if necessary
dos2unix /start.sh

# Activate the Conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate playlette

# Export environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Start Flask
python app/main.py &
# Start Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

