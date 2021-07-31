import React,  { useState } from 'react'
import {Row, Col,InputNumber} from 'react'
import '../../App.css';
import CustomizedSlider from '../Slidingbar';
import jwt_decode from "jwt-decode";
import Swal from 'sweetalert2'
import getCookie from '../../functions/getCookie.js'


function makeid(length) {
  var result           = '';
  var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
     result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}


function addMinutes(minutes) {
  var today = new Date;
  return new Date(today.getTime() + minutes*60000);
}


class ChargeNow extends React.Component {
  constructor(props) {
    super(props);
    this.parentCallback = this.parentCallback.bind(this);
    this.validateAndProceedPayNow = this.validateAndProceedPayNow.bind(this);
    this.validateAndProceedPayLater = this.validateAndProceedPayLater.bind(this);
    this.state = {
      station: props.location.state.selected_station,
      point:props.location.state.selected_point,
      vehicle: {},
      selectedProgram:1,
      batper:10,
      current_kwh: 0,
      selectedCost: props.location.state.selected_point.cost_per_kwh * 1
    };
    
  }
  parentCallback = (newbat) => {
    this.setState({batper:newbat});
  }


  validateAndProceedPayNow(){
    if (this.state.batper <= this.state.vehicle.current_battery_percentage){
      Swal.fire({
        title: 'Invalid',
        text: "Invalid charging options",
        icon: 'error',
        customClass: "swal_ok_button",
        confirmButtonColor: "#242424"
      });
    }
    else {
      var decoded = jwt_decode( getCookie('charge_evolution_token'));
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");
      myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));


      var kwh_delivered = this.state.vehicle.usable_battery_size  * (this.state.batper/100 - this.state.vehicle.current_battery_percentage/100);
      var data = JSON.stringify({
        payment_timestamp : new Date().toISOString().slice(0, 19).replace('T', ' '),
        amount : kwh_delivered * this.state.selectedCost,
        payment_method : "Cash",
        price_policy : "Receipt"
      });

      var requestOptions = { method: 'POST', headers: myHeaders, redirect: 'follow' , body:data  };  
      console.log(data);


      fetch("http://localhost:5000/api/users/payment/"+ decoded.id  , requestOptions)
      .then(response => response.json())
      .then(result => {
          if (result.status == 200){



            var minutes = (this.state.batper/this.state.selectedProgram).toFixed(2)
            var data = JSON.stringify({
              point_id : this.state.point.point_id,
              station_id : this.state.station.station_id,
              transaction_id : result.transaction_id,
              plate_number : this.state.vehicle.plate_number,
              cost_per_kwh : parseFloat(this.state.selectedCost),
              connection_time : new Date().toISOString().slice(0, 19).replace('T', ' '),
              disconnection_time : addMinutes(minutes).toISOString().slice(0, 19).replace('T', ' '),
              kwh_delivered : kwh_delivered,
              fast_charging: this.state.selectedProgram == 1.3 ? 1 : 0
            });

            var requestOptions = { method: 'POST', headers: myHeaders, redirect: 'follow' , body:data  };  
            console.log(data);
        
            fetch("http://localhost:5000/api/users/charge/"+ decoded.id  , requestOptions)
            .then(response => response.json())
            .then(result => {
                if (result.status == 200){
                  Swal.fire({
                    title: 'Success',
                    text: result.msg,
                    icon: 'success',
                    customClass: "swal_ok_button",
                    confirmButtonColor: "#000000"
                  });
                  

                }
                else {
                  Swal.fire({
                    title: 'Error during session upload!',
                    text: result.msg,
                    icon: 'error',
                    customClass: "swal_ok_button",
                    confirmButtonColor: "#000000"
                  })
                }
            })
            .catch(
              err => console.log("ERROR")
            )



          }
          else{
            Swal.fire({
              title: 'Error during Payment!',
              text: result.msg,
              icon: 'error',
              customClass: "swal_ok_button",
              confirmButtonColor: "#000000"
            })
          }
      })
      .catch(
        err => console.log("ERROR")
      )
    
    }
  }

  validateAndProceedPayLater(){
    if (this.state.batper <= this.state.vehicle.current_battery_percentage){
      Swal.fire({
        title: 'Invalid',
        text: "Invalid charging options",
        icon: 'error',
        customClass: "swal_ok_button",
        confirmButtonColor: "#242424"
      });
    }
    else {

        var decoded = jwt_decode( getCookie('charge_evolution_token'));
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));

        var kwh_delivered = this.state.vehicle.usable_battery_size  * (this.state.batper/100 - this.state.vehicle.current_battery_percentage/100);
        var minutes = (this.state.batper/this.state.selectedProgram).toFixed(2)
        var data = JSON.stringify({
          point_id : this.state.point.point_id,
          station_id : this.state.station.station_id,
          transaction_id : makeid(14),
          plate_number : this.state.vehicle.plate_number,
          cost_per_kwh : parseFloat(this.state.selectedCost),
          connection_time : new Date().toISOString().slice(0, 19).replace('T', ' '),
          disconnection_time : addMinutes(minutes).toISOString().slice(0, 19).replace('T', ' '),
          kwh_delivered : kwh_delivered,
          fast_charging: this.state.selectedProgram == 1.3 ? 1 : 0
        });

        var requestOptions = { method: 'POST', headers: myHeaders, redirect: 'follow' , body:data  };  
        console.log(data);
    
        fetch("http://localhost:5000/api/users/charge/"+ decoded.id  , requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.status == 200){
              Swal.fire({
                title: 'Success',
                text: result.msg,
                icon: 'success',
                customClass: "swal_ok_button",
                confirmButtonColor: "#000000"
              });
              

            }
            else {
              Swal.fire({
                title: 'Error during session upload!',
                text: result.msg,
                icon: 'error',
                customClass: "swal_ok_button",
                confirmButtonColor: "#000000"
              })
            }
        })
        .catch(
          err => console.log("ERROR")
        )


    }
  }

  componentDidMount(){
    console.log(this.state.point);
    var decoded = jwt_decode( getCookie('charge_evolution_token'));
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));
    var requestOptions = { method: 'GET', headers: myHeaders, redirect: 'follow' };
    fetch("http://localhost:5000/api/users/vehicles/"+ decoded.id  , requestOptions)
    .then(response => response.json())
    .then(result => {
        // console.log(result);
        this.setState({ batper:result[0].current_battery ,  vehicle:result[0] , batper:result[0].current_battery_percentage}, () => console.log(this.state.vehicle)  );
    })
    .catch(
      err => console.log("ERROR")
    )
  
  }

  
  render () {
    return (

      <div className="chargenowstyle">    
        <div className="chargenowstyle-title-container" >
          <i class="fas fa-car"></i> &nbsp;&nbsp;
          Vehicle specs
        </div>
        <br></br>
        <br></br>
        <div className="chargenowstyle-main-content">
          <p>Brand: {this.state.vehicle.brand}</p>
          <br></br>
          
          <p>Model: {this.state.vehicle.model + " " + this.state.vehicle.release_year} </p>
          <br></br>
          <p>Port AC :  {this.state.vehicle.ac_charger_ports_0}</p>
          <br></br>
          <p>Port DC :  {this.state.vehicle.dc_charger_0}</p>
          <br></br>
          <p>Plate number: {this.state.vehicle.plate_number}</p>
          
         
          <br></br>
          <p>Battery percentage: {this.state.vehicle.current_battery_percentage + "%"} </p>

        </div>
        <br></br>
        <br></br>
        <div className="chargenowstyle-title-container" >
        <i class="fas fa-tasks"></i> &nbsp;&nbsp;
          Choose program
        </div>
        <br></br>
        <br></br>
        <div className="rowchargenow">
          <div 
          className={this.state.selectedProgram===0.8 ? "programselection" : "columnchargenow" }
          type="button"
          onClick={()=>this.setState(  {selectedProgram:0.8,selectedCost:(this.state.point.cost_per_kwh * 0.8).toFixed(3)}  )}>
            <i class="fas fa-leaf"></i>&nbsp;&nbsp;
            <h2>Eco </h2>
            <br></br>
            
            <p>Cost per kWh: {(this.state.point.cost_per_kwh * 0.8).toFixed(3)}</p>
            <br></br>
            
          </div>
          <div 
          type="button"
          className={this.state.selectedProgram===1 ? "programselection" : "columnchargenow" }
          onClick={()=>this.setState({selectedProgram:1,selectedCost:this.state.point.cost_per_kwh})}>
            <i class="fas fa-check-circle"></i>&nbsp;&nbsp;
            <h2>Standard </h2>
            <br></br>
            
            <p>Cost per kWh: {this.state.point.cost_per_kwh}</p>
            <br></br>

          </div>
          <div 
          className={this.state.selectedProgram===1.3 ? "programselection" : "columnchargenow" }
          type="button" 
          onClick={()=>this.setState({selectedProgram:1.3,selectedCost:(this.state.point.cost_per_kwh * 1.3).toFixed(3)})}>
            <i class="fas fa-bolt"></i>&nbsp;&nbsp;
            <h2>Fast </h2>
            <br></br>
            <p>Cost per kWh: {(this.state.point.cost_per_kwh * 1.3).toFixed(3)}</p>
            <br></br>
            
          </div>
        </div>
        <br></br>
        <br></br>
        <div className="chargenowstyle-title-container" >
          <div className='fixedbox1'>
            <i class="fas fa-battery-three-quarters"></i>&nbsp;Charging&nbsp;
          </div>
          <div className='fixedbox2'>
            &nbsp;&nbsp;{this.state.batper} %
          </div>
        </div>
        <div className="chargenowstyle-title-container" >
          <div className='fixedbox3'>

            <i class="fas fa-coins"></i>&nbsp;Cost&nbsp;
          </div>
          <div className='fixedbox4'>
            &nbsp;&nbsp;{(this.state.batper*this.state.selectedProgram).toFixed(2)}&nbsp;€
          </div>      
        </div>
        <div className="chargenowstyle-title-container" >
          <div className='fixedbox5'>

          <i class="far fa-clock"></i>&nbsp;Time&nbsp;
          </div>
          <div className='fixedbox6'>
            {(this.state.batper/this.state.selectedProgram).toFixed(2)}&nbsp;min
          </div>      
        </div>
        
        <br></br>
        <br></br>
        <div className="chargenowstyle-main-content">
          <CustomizedSlider parentCallback={this.parentCallback} initial={this.state.vehicle.current_battery_percentage}  batper={this.state.batper}/>
        </div>
        <br></br>
        <br></br>
          <button type="button" className="programselection2"  onClick={ this.validateAndProceedPayNow }>
            <i class="fas fa-money-check-alt"></i>&nbsp;&nbsp;
            Pay now!
          </button>
          <button type="button" className="programselection2" onClick={ this.validateAndProceedPayLater }>
          <i class="fas fa-wallet"></i>&nbsp;&nbsp;
          Add to balance!</button>
      </div>

      
    )
  }
}

export default ChargeNow
