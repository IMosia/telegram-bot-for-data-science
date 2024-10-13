#!/bin/bash

# Need for automatic creation of the admin user at the first start of the Airflow container
# And to avoid the need to manually create the admin user every time the container is started

# Check if the admin user already exists
airflow users list | grep -w admin > /dev/null

if [ $? -ne 0 ]; then
  echo "Creating Airflow admin user..."
  airflow users create \
    --role Admin \
    --username admin \
    --email admin \
    --firstname admin \
    --lastname admin \
    --password admin
else
  echo "Admin user already exists, skipping creation."
fi
