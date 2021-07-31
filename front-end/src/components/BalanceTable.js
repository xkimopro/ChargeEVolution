import BootstrapTable from 'react-bootstrap-table-next';
import ReactHtmlParser from "react-html-parser";
import ToolkitProvider from 'react-bootstrap-table2-toolkit';


import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import 'react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit.min.css';
// import 'bootstrap/dist/css/bootstrap.min.css';
import './BalanceTable.css';
import HtmlParser from 'react-html-parser';




function exportF(){
        var htmls = "";
        var uri = 'data:application/vnd.ms-excel;base64,';
        var template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'; 
        var base64 = function(s) {
            return window.btoa(unescape(encodeURIComponent(s)))
        };

        var format = function(s, c) {
            return s.replace(/{(\w+)}/g, function(m, p) {
                return c[p];
            })
        };
        var tableElem = document.getElementById("table1");
        htmls = tableElem.outerHTML;

        var ctx = {
            worksheet : 'Worksheet',
            table : htmls
        }


        var link = document.createElement("a");
        link.download = "export.xls";
        link.href = uri + base64(format(template, ctx));
        link.click();
}



function htmlAndFormatbalance(raw){
    raw = parseFloat(raw);
    if (parseInt(raw) > 0)   return HtmlParser("<div class='balance-red'>" + raw.toFixed(2) + "</div>");  
    if (parseInt(raw) == 0)  return HtmlParser("<div class='balance-neutral'>" + raw.toFixed(2) + "</div>");  
    if (parseInt(raw) < 0)   return HtmlParser("<div class='balance-green'>" + raw.toFixed(2) + "</div>");  
}

function findTransactionForSession(transaction_id,transactions){
    for (const t of transactions){
        if (t['transaction_id'] === transaction_id) return t;
    }
    return {
        'payment_method': '*',
        'price_policy': '*'
    }
}

function formatBalance(transactions,sessions){
    var balance = [];
    for (const session of sessions){
        var transactionOfSession = findTransactionForSession(session.transaction_id,transactions);
        balance.push({
            'activity_type': 'Charging session',
            'activity_timestamp': session.disconnection_time,
            'payment_method': transactionOfSession.payment_method,
            'amount' : (session.cost_per_kwh * session.kwh_delivered).toFixed(2),
            'price_policy': transactionOfSession.price_policy,
            'activity_id': session.session_id,
            'balance' : 0
        });
    }
    for (const transaction of transactions){
        balance.push({
            'activity_type': 'Transaction',
            'activity_timestamp': transaction.payment_timestamp,
            'payment_method':   transaction.payment_method ,
            'amount' : -transaction.amount,
            'price_policy': transaction.price_policy,
            'activity_id': transaction.transaction_id,
            'balance' : 0
        });
    }
    balance.sort((a, b) => (a.activity_timestamp < b.activity_timestamp) ? 1 : -1)


    var last = balance.length - 1; 

    // // Object.assign(balance[2].balance,balance[2].amount)


    for (var i = last; i >=0; i--) {
        if (i == last) balance[i].balance = parseFloat(balance[i].amount);
        else balance[i].balance = parseFloat(balance[i].amount) + balance[i+1].balance;    
    }
    
    var latest_balance = -1.91;
    for (var i = last; i >=0; i--) {
        if (i===0) latest_balance = balance[i].balance;
        balance[i].balance = htmlAndFormatbalance(balance[i].balance);
    }




    return [balance,latest_balance];
}



const BalanceTable = (props)  => {

    const [newSessions,latest_balance] = formatBalance(props.transactions, props.sessions);
    console.log(latest_balance);
    props.parentCallback(latest_balance.toFixed(2));
        const columns = [ 
    {
        dataField: 'activity_type',
        text: 'activity_type'
    },

    {
        dataField: 'activity_timestamp',
        text: 'activity_timestamp'
    },
    {
        dataField: 'payment_method',
        text: 'payment_method'
    },
    {
        dataField: 'amount',
        text: 'amount'
    }, 
    {
        dataField: 'price_policy',
        text: 'price_policy'
    },
    {
        dataField: 'activity_id',
        text: 'activity_id'
    },
    {
        dataField: 'balance',
        text: 'Balance'
    }
    ];

    
    return (
        <>
        <div>
            <div className="export-button-container">
            <button id="downloadLink" className="btn--large5" onClick={exportF}>Export to excel</button>
            </div>
            <div className="balance-table-container">
            
            <ToolkitProvider
            keyField="id"
            data={ newSessions }
            columns={ columns }
            >
            {
                props =>
                <BootstrapTable  id="table1" classes="table-dark balance-table"  hover 
                             { ...props.baseProps } />
            }
            </ToolkitProvider>



            </div>
        </div>
        </>
    );

}

export default BalanceTable;
  