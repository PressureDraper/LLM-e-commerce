#!/bin/bash

echo "Select an option:"
echo "1) Generate schema migration"
echo "2) Apply database migrations"
echo "3) Both"

read -p "Enter option [1-3]: " MODE

case $MODE in
    1)
        echo "Generating database schema migration..."
        docker exec -it ecommerce_api alembic revision --autogenerate -m "llm-db-schema"
        ;;
    2)
        echo "Applying database migrations..."
        docker exec -it ecommerce_api alembic upgrade head
        ;;
    3)
        echo "Generating database schema migration..."
        docker exec -it ecommerce_api alembic revision --autogenerate -m "llm-db-schema"

        echo "Applying database migrations..."
        docker exec -it ecommerce_api alembic upgrade head
        ;;
    *)
        echo "Invalid option."
        exit 1
        ;;
esac