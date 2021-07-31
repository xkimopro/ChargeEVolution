import React from 'react';
import PropTypes from 'prop-types';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Slider from '@material-ui/core/Slider';
// import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';

const useStyles = makeStyles((theme) => ({
  root: {
    width: 'inherit'
  },
  margin: {
    height: theme.spacing(3),
  },
}));

function ValueLabelComponent(props) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
}

ValueLabelComponent.propTypes = {
  children: PropTypes.element.isRequired,
  open: PropTypes.bool.isRequired,
  value: PropTypes.number.isRequired,
};






const PrettoSlider = withStyles({
  root: {
    color: '#64d7d6',
    height: 8,
  },
  thumb: {
    height: 34,
    width: 34,
    backgroundColor: '#fff',
    border: '2px solid currentColor',
    marginTop: -8,
    marginLeft: -12,
    '&:focus, &:hover, &$active': {
      boxShadow: 'inherit',
    },
  },
  active: {},
  valueLabel: {
    left: 'calc(-20% + 4px)',
  },
  track: {
    height: 18,
    borderRadius: 8,
  },
  rail: {
    height: 18,
    borderRadius: 8,
  },
})(Slider);


const CustomizedSlider = (props)=> {
  const classes = useStyles();
  const [value, setValue] = React.useState(props.batper);
  const handleChange = (event, newValue) => {
    setValue(newValue);
    props.parentCallback(newValue);
  };


  return (
    <div className={classes.root}>
      
      {/* <Typography gutterBottom>pretto.fr</Typography> */}
      <PrettoSlider 
        valueLabelDisplay="auto"
        aria-label="pretto slider"
        defaultValue={props.initial}
        value={value} 
        onChange={handleChange} 
        />
      
    </div>
  );
}
export default CustomizedSlider;