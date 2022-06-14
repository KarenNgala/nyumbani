# BOOKIE

## Getting Started
To get a copy of the project up and running on your local machine for development and testing purposes,

- For `WINDOWS` users:
  - [Follow this article](https://animesh.blog/setting-up-an-existing-django-project-on-windows/)

- For `LINUX` users:
1. **clone** this repository 
   ``` 
   git clone https://github.com/KarenNgala/nyumbani
   ```
2. Install and actvate a virtual environment
   ```bash
   $ python3.6 -m venv --without-pip virtual

   $ source virtual/bin/activate
   ```

3. Install **pip** and project **dependencies**
   ```sh
   (virtual) $ curl https://bootstrap.pypa.io/get-pip.py | python
   virtual) $ pip install -r requirements.txt
    ```
* See deployment for notes on how to deploy the project on a live system.

### Database requirements
1.  To get a development env running, use the **.env.example** file to create **your own** `.env` file.
2.  Create a **postgres** db and add the credentials to the .env file
```
(virtual)$ psql
pc-name=#  CREATE DATABASE <name>;
```
3.  Apply initial migrations
```sh 
(virtual) $ python manage.py migrate 
```
4. Run migrations to your database
```sh
(virtual) $ python manage.py makemigrations application
(virtual) $ python manage.py migrate
```
5. Create admin account
```
(virtual) $ python manage.py createsuperuser
```
6.  Start development server
```
 (virtual) $ python3 manage.py runserver
 ```

## Running the tests

Run automated tests for this system

```sh
(virtual) $ python3 manage.py test application
```

## Deployment

With all environment variables changed to suit your local copy of this repository, deploy the application to [Heroku](https://medium.com/@hdsingh13/deploying-django-app-on-heroku-with-postgres-as-backend-b2f3194e8a43) to see it live

## Built With

* [Django 3.1](https://www.djangoproject.com/) - The web framework used
* [Heroku](https://www.heroku.com/platform) -  Deployment platform
* [Python3](https://www.python.org/) - Backend logic
* [Postresql](https://www.postgresql.org/) - Database system

## License
This project is licensed under the MIT License - see the LICENSE.md file for details