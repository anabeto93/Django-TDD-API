# Django-TDD-API
Some API I haven't settled on yet, but just to do TDD with Django

## Setup and Installation
Simply run the below command

Ensure to change directory to where the source code is and do or run the following

```bash
docker build .
```
The `.` simply represents or means the current directory, so it will look out for the `Dockerfile`

You need a little patience and internet at this stage for it to complete.

Once that is done, just remeber you don't have to run the same commands any longer, just this once. Now, everytime you need to run this app, kindly run the command below

```bash
docker-compose up
```

## Running Tests
You can run the tests which have been written for each individual app with the followin command

```bash
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

The Flake8 is to check for linting, since I am going with `PEP 8`

## Special Notes
I added `192.168.99.100` to the list of `ALLOWED_HOSTS` in the `app/settings.py` file since I'm using docker to run this on my local machine

## Sample URLS and Endpoints

`/api/user/create` takes you to the `DRF` page for creating a user account.

`/api/user/token` is used to create a token based on an existing user account.

`/api/user/me` but you will need the ModHeader extension to add `Authorization: Token some_token_here` before you can visit this in your browser. The `some_token_here` is obtained when you have visited the `/api/user/token` endpoint.
