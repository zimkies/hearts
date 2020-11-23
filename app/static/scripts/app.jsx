import React from 'react';
import { BrowserRouter, Route, Switch, Link, UseHistory } from "react-router-dom";


class Home extends React.Component {
    constructor(props) {
      super(props);

      this.createGame = this.createGame.bind(this)
    }

    createGame() {
      const { history } = this.props;

      console.log("Creating Game")
      fetch('/api/games/', {method: 'POST'})
        .then(response => response.json())
        .then((game) => {
          console.log(game);
          history.push(`/games/${game.id}`)})
    }

    render() {
        return (
            <button onClick={this.createGame}>Create game</button>
        );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);

    this.state = {game: null};

    this.gameId = props.match.params.gameId;
    console.log("Rendering game")

    this.startGame = this.startGame.bind(this);
    this.getGame = this.getGame.bind(this);

    this.getGame();

  }

  getGame() {
    fetch(`/api/games/${this.gameId}`)
        .then(response => response.json())
        .then((game) => { this.setState({game: game}) })
  }

  startGame() {
   const { history } = this.props;

   console.log("Creating Game")
   fetch(`/api/games/${this.gameId}/start`, {method: 'POST'})
     .then(response => response.json())
     .then((game) => { this.setState({game: game}) })
  }

  render() {

       const gameState = this.state.game == null ? null : this.state.game.state;
       return (
        <div>
          <h2>Game {this.gameId}</h2>
          <div>
          { (() => {
            switch (gameState) {
              case "STARTED": return <StartedGame game={this.state.game} />;
              default: return <button onClick={this.startGame}>Start game</button>;
            }

          })()}
          </div>
        </div>
       );
   }
}

class Card extends React.Component {

  render() {
    return (
      <div>{this.props.card}</div>
    )
  }
}

class StartedGame extends React.Component {

  render() {
    // TODO: don't return all hands from the backend, only this players.
    const playerHand = this.props.game.hand
    const renderedCards = playerHand.map((card) => <Card key={card} card={card} /> )

     return (
      <div>
        In started game

        {renderedCards}
      </div>
       );
   }
}


class App extends React.Component {

    render() {
        return (
          <BrowserRouter>
            <h1>Hi Hearts React!</h1>

            <Switch>
                  <Route path="/games/:gameId" component={Game} />
                  <Route path="/" component={Home} />
            </Switch>


          </BrowserRouter>
        );
    }
}
export default App;
