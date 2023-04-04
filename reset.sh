docker-compose down
docker volume rm $(docker volume ls -qf dangling=true)
docker-compose build --no-cache
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose run web python manage.py loaddata data.json
