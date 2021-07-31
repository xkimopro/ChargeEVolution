import React, { useEffect, useRef } from "react";
import '../../App.css';
import getCookie from '../../functions/getCookie.js'
import chargingMarker from "../../station-icon.png";
import {
    withGoogleMap,
    withScriptjs,
    GoogleMap,
    GoogleApiWrapper,
    Marker,
    InfoWindow
} from "react-google-maps";
import Map from '../MapComponent.js'  
import SlidingPane from "react-sliding-pane";
import "react-sliding-pane/dist/react-sliding-pane.css";
import { Link } from 'react-router-dom';


import dummy from "../../walmart-charging-station.jpg" ;



// const WrappedMap = withScriptjs(withGoogleMap(Map));
  
class Charge extends React.Component {    

      constructor(props) {
        super(props);
        this.parentCallback = this.parentCallback.bind(this);
        this.state = {
          stations: [],
          isPaneOpen: false,
          paneContent: {},
          points:[],
          haspoints: false
        };
        
      }


      async componentDidMount(){
          const response = await fetch('http://localhost:5000/api/stations/');
          const json = await response.json();
          await this.setState({
            stations: json
          })
          // await console.log(this.state.stations);

      
            }

      parentCallback = (data) => {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));
        var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
        };

        fetch("http://localhost:5000/api/stations/points/"+ data.station_id, requestOptions)
        .then(response => response.json())
        .then(result => {
          if (result.length === 0) {
            this.setState({
              haspoints: false
            });
            console.log('result', result);
          }
          else {
            this.setState({
              points: result,
              haspoints: true
            });
          }
        })
        .catch(error => console.log('error', error));
          this.setState({
            isPaneOpen:true,
            paneContent: data
          })

      }




      render () {
            return (
                <div>
                    <div className = "menumap">
                        <div className="map" style={{display: 'flex',  justifyContent:'center'}}>
                            <Map
                            googleMapURL={'https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyC7Gc6r0zfRF_0unVl39qCFXzs4Ap7rkik'} // using api key
                            loadingElement = {<div style={{height:"100%"}} />}
                            containerElement = {<div style={{height: "100%", width: "100%"}} />}
                            mapElement = {<div style={{height:"100%"}} />}
                            stations = {this.state.stations}
                            parentCallback = {this.parentCallback}
                            />
                        </div>
                    </div>
                    <SlidingPane
                      className="sliding-pane-station"
                      overlayClassName="sliding-pane-station-overlay"
                      isOpen={this.state.isPaneOpen}
                      title="Hey, it is optional pane title.  I can be React component too."
                      subtitle="Optional subtitle."
                      onRequestClose={() => {
                        // triggered on "<" on left top click or on outside click
                        this.setState({ isPaneOpen: false, haspoints: false });
                      }}
                    >
                    <div className="pane-title-container" >
                      <h2>{this.state.paneContent.station_name}</h2>
                    </div>
                      
                   
                    <img className="dummy" src={dummy} />
                    <br></br>
                    <br></br>
                    <div className="pane-main-content">
                      <p>Address: {this.state.paneContent.address}</p>
                      
                      <p>Town: {this.state.paneContent.town}</p>
                     
                      <p>Country: {this.state.paneContent.country}</p>

                      <p>Postcode: {this.state.paneContent.postcode}</p>

                      <p>Email: {this.state.paneContent.email}</p>

                      <p>Contact Phone: {this.state.paneContent.phone}</p>
                    </div>
                    <br></br>
                    <br></br>
                    
                    {this.state.haspoints &&
                    this.state.points.map(point => 
                    <div>
                    <div key={point.point_id} className="pane-main-content"> 
                      <p>Cost per kWh: {point.cost_per_kwh} €</p>
                      
                      <p>Connector Type: {point.type}</p>
                     
                      <p>Current: {point.current}</p>

                      <p>Fast charging: {point.fast_charging}</p>

                      <p>Level: {point.level}</p>

                      <p>Quantity: {point.quantity}</p>
                    <br></br> 
                    <br></br>
                    <div>
                      
                        <Link to= {
                          {
                              pathname: "/chargenow", 
                              state: {
                                selected_point : point,
                                selected_station: this.state.paneContent
                              }
                          }
                          
                        } type="button"  className="btn--large2" >
                          <i class="fas fa-plug"></i>
                          &nbsp;&nbsp;Charge now!
                        </Link>
                      
                      
                        <Link to={ {
                              pathname: "/rendezvous", 
                              state: {
                                selected_point : point,
                                selected_station: this.state.paneContent
                              }
                              }} 
                              type="button"  
                              className="btn--large2" >

                          <i class="fas fa-calendar-check"></i>
                          &nbsp;&nbsp;Book charging slot!
                        </Link>
                      
                   
                    </div>                    
                    </div>
                    <br></br>
                    </div>
                    ) 
                    
                    }
                    {this.state.haspoints === false &&
                    <div className="pane-title-container" >
                      <h2>Unfortunately this station does not have active charging points :(... Try another station!</h2>
                    </div>
                    }

                    </SlidingPane>
                </div>
            );
      }

}
export default Charge;