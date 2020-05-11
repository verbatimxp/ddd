import React, {Component} from 'react';
import TimerService from './TimerService';

const customersService = new TimerService();

class TimerPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            timer_data: '',
        };
    }

    get_data(data) {
        var  self  =  this;
        customersService.getTimer(data).then(function (result) {
            self.setState({timer_data: result});
        });
    }

    render() {

        return (

            <div className="container-fluid">
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
                  <a className="header_title"  href="/">Async Timer</a>
                  <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                  </button>
                  <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div className="navbar-nav">

                    </div>
                  </div>
                </nav>


                <div className="container-fluid container-list-header">
                    <h4 id='123'>Successfully connected to Websocket</h4>

                        <div className="row container-list" >
                            <div className="col-sm-3 container-button-timer">
                                <a onClick={()=> this.get_data('start')} className="btn btn-primary">Start timer</a>

                            </div>

                            <div className="col-sm-3 container-button-timer">
                                <a onClick={()=> this.get_data('get')} className="btn btn-primary"> Get Values</a>

                            </div>
                            <div className="col-sm-3 container-button-timer">
                                <a onClick={()=> this.get_data('stop')} className="btn btn-primary"> Stop Timer</a>
                            </div>
                        </div>
                </div>
                <div>
                    {this.state.timer_data && <span>{this.state.timer_data}</span>}
                </div>
            </div>

        );
    }
}

export default TimerPage;