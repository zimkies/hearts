# hearts

# To run:


https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react

1. Install pipenv

https://pipenv.pypa.io/en/latest/install/#using-installed-packages

2. Install python libraries:

within this project's directory:

```
pipenv install
```

3. Run the flask app

```
pipenv run flask run
```


## Development

After installing, above, for development:

```
FLASK_ENV=development pipenv run flask run
```

and in another terminal:

Within ~/$WORKSPACE/app/static/
```
npm run watch
```

Both of these commands will ensure live reloads of your backend/frontend code whenever you change the source code during development.

Note you'll still have to hard-refresh the page to see javascript changes though.
