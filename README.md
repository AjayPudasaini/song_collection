# song_collection

A Simple Admin panel to manage records of artists with their songs collection

 ## Requirements
    - Docker
    - Docker Compose

# To run this project local environment follow these steps:
    * switch branch
    - git checkout develop
    * build
    - sudo docker compose -f local.yml --build
    * create superuser
    - sudo docker compose -f local.yml run --rm django python manage.py createsuperuser
    * up container
    - sudo docker compose -f local.yml up
