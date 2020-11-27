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


## Testing

pyenv run pytest app/tests/


## TODO list

- Search for all 'todo's in codebase for more ideas.
- Make actions realtime by using websockets
- Validate moves (e.g. have to follow suits)
- Add the 'exchange cards' part of the game.
- Keep score
- Add concept of more than one round in a game.
- Add ability to join someone else's game.
- Make the AI not completely dumb
- Make AI player names (and game uuids) more fun (e.g red-penguin-2342)
- Ensure this works on a phone as well as computer.
- Upload to heroku
- Add database storage for games so that reloading the server doesn't wipe out all existing games.
- Add python and js linters.
- Add auto-test runner as pre-commit hook.
