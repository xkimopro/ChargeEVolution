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


class Balance extends React.Component {    

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
            <>
            <div className="balance-title-container">
              <div className="balance-title"><h1><i class="fas fa-balance-scale"></i> &nbsp;&nbsp;Balance overview</h1></div>
            </div>
            <div className='date-range-container'>
                <div className="wallet-container">
                <div className="wallet-pane">
                      <br></br>
                      <h1><i class="fas fa-balance-scale-right"></i>&nbsp;&nbsp;My Balance</h1>
                      <h1>{this.state.current_balance}&nbsp;€</h1>
                      <br></br>
                      <br></br>
                      <br></br>
                      <br></br>
                      <h1><i class="fas fa-wallet"></i>&nbsp;&nbsp;My Wallet {process.env.REACT_APP_SSL_KEY_FILE}</h1>
                      <h1>{this.state.current_wallet}&nbsp;€</h1>
                    </div>
                </div>
                <DateRangePicker
                  ranges={[selectionRange]}
                  onChange={this.handleSelect}
                />
            </div>
            <BalanceTable 
                transactions={this.state.transactions}
                sessions={this.state.sessions}
                parentCallback = {this.parentCallback}
                >

            </BalanceTable>
            </>

          );
    }

}
export default Balance;