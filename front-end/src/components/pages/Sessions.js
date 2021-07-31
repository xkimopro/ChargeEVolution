import React from "react";
import '../../App.css';

import SlidingPane from "react-sliding-pane";

import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file
import "react-sliding-pane/dist/react-sliding-pane.css";

import BalanceTable from '../BalanceTable.js'  
import getCookie from '../../functions/getCookie.js'
import jwt_decode from "jwt-decode";
import { DateRangePicker } from 'react-date-range';



class Sessions extends React.Component {    

    constructor(props) {
      super(props);
      this.state = {
        transactions:[],
        sessions:[],
        start_date: new Date(),
        end_date:  new Date(),
        current_balance: 0,
        current_wallet: 0,
        balance_fetched: false
      };
      
      this.handleSelect = this.handleSelect.bind(this);
      this.fetchDataApi = this.fetchDataApi.bind(this);
      this.fetchDataApi2 = this.fetchDataApi2.bind(this);
      this.parentCallback = this.parentCallback.bind(this);
    }


    fetchDataApi(){
        var decoded = jwt_decode( getCookie('charge_evolution_token'));
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));
        var requestOptions = { method: 'GET', headers: myHeaders, redirect: 'follow' };
        fetch("http://localhost:5000/api/users/transactions/"+ decoded.id + "/2000-01-01/3000-01-01" , requestOptions)
        .then(response => response.json())
        .then(result => {
            // console.log(result);
            this.setState({transactions:result}, () => console.log(this.state.transactions)  );
        })
        .catch(
          err => console.log("ERROR")
        )
        fetch("http://localhost:5000/api/users/sessions/"+ decoded.id + "/2000-01-01/3000-01-01" , requestOptions)
        .then(response => response.json())
        .then(result => {
            this.setState({sessions:result});
        });
        
        fetch("http://localhost:5000/api/users/wallet/"+ decoded.id  , requestOptions)
        .then(response => response.json())
        .then(result => {
            this.setState({current_wallet:result.wallet});
            console.log(result)
        })
        .catch(e => {
          console.log(e)
        });
    }
    
    fetchDataApi2(from,to){
      var decoded = jwt_decode( getCookie('charge_evolution_token'));
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");
      myHeaders.append("charge_evolution_token",  getCookie('charge_evolution_token'));
      var requestOptions = { method: 'GET', headers: myHeaders, redirect: 'follow' };
      fetch("http://localhost:5000/api/users/transactions/"+ decoded.id + "/" + from + "/" + to, requestOptions)
      .then(response => response.json())
      .then(result => {
          // console.log(result);
          this.setState({transactions:result}, () => console.log(this.state.transactions)  );
      })
      .catch(
        err => console.log("ERROR")
      )
      fetch("http://localhost:5000/api/users/sessions/"+ decoded.id + "/" + from + "/" + to, requestOptions)
      .then(response => response.json())
      .then(result => {
          this.setState({sessions:result});
      });        
    }
 

    componentDidMount(){
      this.setState({
        balance_fetched:false
      });
      this.fetchDataApi();
      }

    parentCallback = (data) => {
      if (this.state.balance_fetched) return;
      console.log(data)
      this.setState({
        balance_fetched:true,
        current_balance:data
        
      });
    }

    handleSelect(ranges){
      this.fetchDataApi2(ranges.selection.startDate.toISOString().slice(0,10),ranges.selection.endDate.toISOString().slice(0,10));
      this.setState({
        start_date: ranges.selection.startDate,
        end_date: ranges.selection.endDate
      });
    }


    

    render () {
      
        const selectionRange = {
          startDate: this.state.start_date,
          endDate: this.state.end_date,
          key: 'selection',
        }

          return (
            <div>
            <div className="balance-title-container">
              <div className="balance-title"><h1><i class="fas fa-search-dollar"></i> &nbsp;&nbsp;Sessions overview</h1></div>
            </div>
            </div>

          );
    }

}
export default Sessions;