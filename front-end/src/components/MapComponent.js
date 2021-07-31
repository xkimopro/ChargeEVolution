import React, { useState, memo } from "react";
import chargingMarker from "../charging-station-location-512.png";
import {
    withGoogleMap,
    withScriptjs,
    GoogleMap,
    GoogleApiWrapper,
    Marker,
    InfoWindow
  } from "react-google-maps";

  


  


//maps
const Map = (props) =>  {    

        const [station, setStation] = useState({});
        const [showTab, setshowTab] = useState(false);

        const onMarkerClick = (e) => {
          //  console.log(e);
           props.parentCallback(e);
        };  

        const areEqual = (prevProps, nextProps) => true;

        

        const markerItems = (props.stations).map((station) =>
        {
            return (<Marker  icon={{
                url: chargingMarker,
                scaledSize: {width: 60, height: 60}
                }}    
                position={{ lat: parseFloat(station.latitude), lng: parseFloat(station.longitude) }} 
                onClick={() => onMarkerClick(station)}
                /> );
            
        }
        
        );
        



        return (
          <GoogleMap 
            defaultZoom={5} 
            defaultCenter={{lat: 38.0177822, lng: 23.8570679}} 
            >
    
           {markerItems}
           </GoogleMap>
        );  
}

export default withScriptjs(withGoogleMap(React.memo(Map)));