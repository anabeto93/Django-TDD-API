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

## Special Notes
I added `192.168.99.100` to the list of `ALLOWED_HOSTS` in the `app/settings.py` file since I'm using docker to run this on my local machine

## Sample URLS and Endpoints

`/api/user/create` takes you to the `DRF` page for creating a user account.

`/api/user/token` is used to create a token based on an existing user account.
