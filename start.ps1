# Start all containers
docker-compose up -d

if (!$?){
    exit 1
}

# Activate the virtual environment
& .\env\Scripts\Activate

# Change the directory to food_allocation
cd .\food_allocation