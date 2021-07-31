import React from 'react';
import '../../App.css';
import ProfileSection from '../ProfileSection';
import getCookie from '../../functions/getCookie.js'
import jwt_decode from "jwt-decode";


class Profile extends React.Component {
  componentDidMount(){
    var myHeaders = new Headers();
    var decoded = jwt_decode( getCookie('charge_evolution_token'));
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));
    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };


    fetch("http://localhost:5000/api/users/user/"+ decoded.id, requestOptions)
    .then(response => response.json())
    .then(result => this.setState({profile:result}))
    .catch(error => console.log('error', error));

    fetch("http://localhost:5000/api/users/vehicles", requestOptions)
    .then(response => response.json())
    .then(result => this.setState({allvehicles:result}, () => console.log(result)
    ))
    .catch(error => console.log('error', error));

    fetch("http://localhost:5000/api/users/vehicles/"+ decoded.id, requestOptions)
    .then(response => response.json())
    .then(result => {
      if (result.length === 0) {
        this.setState({
          hascars: false
        });
      }
      else {
        this.setState({
          vehicles:result,hascars: true});
        };
    })
    .catch(error => console.log('error', error));
    

  }

  constructor(props) {
      super(props);
      this.state = {
          profile: {},
          vehicles: [],
          allvehicles:[],
          hascars:false
      };
  }
 render(){
   return(
     
      <ProfileSection profile={this.state.profile}
      vehicles ={this.state.vehicles}
      allvehicles={this.state.allvehicles}
        />
   )
 }
 
}

export default Profile;