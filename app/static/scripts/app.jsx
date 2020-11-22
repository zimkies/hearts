import React from 'react';
import { BrowserRouter, Route, Switch, Link } from "react-router-dom";


class Home extends React.Component {

    createGame() {
      console.log("Creating Game")
      fetch('/api/games/', {method: 'POST'})
        .then(() => console.log("Created Game"));
    }

    render() {
        return (
            <button onClick={this.createGame}>Create game</button>
        );
    }}


class App extends React.Component {

    render() {
        return (
          <div>
            <h1>Hi Hearts React!</h1>

            <Switch>
                  <Route exact path="" component={Home} />
                  <Route path="/games/:gameId" component={Game} />
            </Switch>

          </div>
        );
    }}
export default App;
