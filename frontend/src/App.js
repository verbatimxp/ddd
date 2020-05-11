import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom'
import { Route, Link } from 'react-router-dom'
import  TimerPage from './TimerPage'
import './App.css';

const BaseLayout = () => (

    <div className="content">
      <Route path="/" exact component={TimerPage} />
    </div>
)

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <BaseLayout/>
      </BrowserRouter>
    );
  }
}

export default App;