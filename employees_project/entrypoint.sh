#!/bin/sh

echo "Migrate the Database at startup of project"

# Wait for few minute and run db migraiton
while ! python manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done

echo "Collect static files"

while ! python manage.py collectstatic --noinput 2>&1; do
   echo "Collectstatic is in progress status"
   sleep 3
done

exec "$@"
