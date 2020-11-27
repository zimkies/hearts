import React from 'react';
import { BrowserRouter, Route, Switch, Link, UseHistory } from "react-router-dom";
import ReactHeart from '../icons/icon-heart.svg';
import ReactSpade from '../icons/icon-spade.svg';
import ReactClub from '../icons/icon-club.svg';
import ReactDiamond from '../icons/icon-diamond.svg';
import '../css/app.scss';
import '../css/game-table.scss';
import '../css/hand.scss';


class Home extends React.Component {
    constructor(props) {
        super(props);

        this.createGame = this.createGame.bind(this);
    }

    createGame() {
        const { history } = this.props;

        console.log("Creating Game");
        fetch('/api/games/', {method: 'POST'})
            .then(response => response.json())
            .then((game) => {
                history.push(`/games/${game.id}`);
            })
    }

    render() {
        return (
            <div className="menu-btns-container">
                <div className="btn menu-btn" onClick={this.createGame}>Play</div>
                <div className="btn menu-btn">Join</div>
                <div className="btn menu-btn">Offline</div>
                <div className="btn menu-btn">Rules</div>
            </div>
        );
    }
}

class Game extends React.Component {
    constructor(props) {
        super(props);

        this.state = {game: null};

        this.gameId = props.match.params.gameId;
        console.log("Rendering game");

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

        console.log("Creating Game");
        fetch(`/api/games/${this.gameId}/start`, {method: 'POST'})
            .then(response => response.json())
            .then((game) => { this.setState({game: game}) })
    }

    render() {
        const gameState = this.state.game == null ? null : this.state.game.state;

        return (
            <div className="game-room">
                <div className="game-room__id">Game ID {this.gameId}</div>

                <div className="game-table">
                    <div className="player player--1">
                        <div className="player__name">Ben</div>
                    </div>
                    <div className="player player--2">
                        <div className="player__name">Pule</div>
                    </div>
                    <div className="game-table__board"></div>
                    <div className="player player--3">
                        <div className="player__name">Michael</div>
                    </div>
                    <div className="player player--self">
                        <div className="player__name">Ada</div>

                        {(() => {
                            switch (gameState) {
                                case "STARTED": return <StartedGame game={this.state.game} gameId={this.gameId} />;
                                default: return <div className="btn" onClick={this.startGame}>Start</div>;
                            }
                        })()}
                    </div>
                </div>
            </div>
        );
    }
}

class Card extends React.Component {
    constructor(props) {
        super(props);

        this.makeMove = this.makeMove.bind(this);
    }

    makeMove() {
        console.log('message', this.props.gameId, this.props.card);
        fetch(`/api/games/${this.props.gameId}/move`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              card: this.props.card
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        });
    }

    render() {
        return (
            <div className="player__card" onClick={this.makeMove}>
                {this.props.card[0]}
                {(() => {
                    switch (this.props.card[1]) {
                        case "d": return <ReactDiamond className="card__suit icon-diamond" />;
                        case "s": return <ReactSpade className="card__suit icon-spade" />;
                        case "c": return <ReactClub className="card__suit icon-club" />;
                        default: return <ReactHeart className="card__suit icon-heart" />;
                    }
                })()}
            </div>
        )
    }
}

class StartedGame extends React.Component {
    render() {
        // TODO: don't return all hands from the backend, only this players.
        const playerHand = this.props.game.hand
        const renderedCards = playerHand.map((card) => <Card key={card} card={card} gameId={this.props.game.id} /> )

        return (
            <div className="player__hand">
                {renderedCards}
            </div>
        );
    }
}

class App extends React.Component {

    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route path="/games/:gameId" component={Game} />
                    <Route path="/" component={Home} />
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;
