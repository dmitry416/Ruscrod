# Ruscord
### Ruscord is a full-fledged analog of Discord.

Ruscord implements the basic functionality of Discord, such as voice communication, text communication, the ability to create rooms, servers and add to friends.

![image](https://github.com/user-attachments/assets/58c61bd1-3289-4510-a6c9-dfc6b0f6e053)


#### Technologies used in the project:
1. Vue 3
2. DRF
3. Django Channels
4. Celery
5. Redis
6. PostgreSQL

#### docker-compose
Launch composition:
```shell
docker compose up
```

When it's done you should apply migrations

```shell
docker compose run backend python manage.py migrate
```
```shell
docker compose run backend python manage.py createsuperuser
```

#### frontend
Install Node.js & install frontend dependencies via command
```shell
npm install
```
Now you should be able to run frontend application
```shell
npm run preview
```
