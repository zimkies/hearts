import React from 'react';

class HelloWorld extends React.Component {

    createGame() {
      console.log("Creating Game")
      fetch('/api/games/', {method: 'POST'})
        .then(() => console.log("Created Game"));
    }

    render() {
        return (
          <div>
            <h1>Hello, World!</h1>
            <label>What is your name</label>
            <input></input>

            <button onClick={this.createGame}>Create game</button>
          </div>
        );
    }}
export default HelloWorld;
