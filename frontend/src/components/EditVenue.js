import React, { useState, useEffect } from "react";
import axios from "axios";
import MenuItem from "@material-ui/core/MenuItem";
import { States } from "./States.js";

import {
  Wrapper,
  Row,
  BigBackground,
  FormContainer,
  InputText,
  InputSelect,
  Label,
  FormButton,
  RowSection,
} from "../style.js";

const EditVenue = (props) => {
  var id = props.match.params.venueId;

  const [venue, setVenue] = useState({});
  const [error, setError] = useState(true);
  const [open, setOpen] = React.useState(false);

  const [newVenue, setNewVenue] = useState({
    name: "",
    city: "",
    state: "",
    address: "",
  });
  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };
  var getVenue = () => {
    console.log("any props?", props);
    console.log(" param?", props.match.params.venueId);
    axios
      .get(`/api/venues/` + id)
      .then(function (response) {
        // handle success
        console.log(response.data.venue);
        setVenue(response.data.venue);
        setNewVenue(response.data.venue);
        setError(false);
      })
      .catch(function (error) {
        // handle error
        console.log(error.code);
      })
      .then(function () {
        // always executed
      });
  };

  useEffect(() => {
    getVenue();
  }, []);

  const handleChange = (e) => {
    e.preventDefault();

    setNewVenue((prevVal) => {
      return {
        ...prevVal,
        [e.target.name]: e.target.value,
      };
    });
  };
  const submitVenue = (e) => {
    e.preventDefault();
    console.log("name", newVenue.name);
    console.log("city", newVenue.city);
    console.log("tot", newVenue);
    axios
      .patch(`/api/venues/` + id, newVenue)
      .then(function (response) {
        // handle success
        console.log(response.data);
        setVenue(newVenue);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
  };

  const deleteVenue = (e) => {
    e.preventDefault();
    console.log("name", newVenue.name);
    console.log("city", newVenue.city);
    console.log("tot", newVenue);
    axios
      .delete(`/api/venues/` + id)
      .then(function (response) {
        // handle success
        console.log(response.data);
        setVenue(undefined);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
  };
  if (!venue) {
    return <h1>No Venue Found</h1>;
  }
  return (
    <BigBackground>
      {!error ? (
        <Wrapper>
          <div>
            <h2>Current</h2>
            <div>Name: {venue.name}</div>
            <div>City: {venue.city}</div>
            <div>State: {venue.state}</div>
            <div>Address: {venue.address}</div>
          </div>
          <FormContainer>
            <h2>Edit Venue</h2>
            <form onSubmit={submitVenue}>
              <InputText
                label="Venue Name"
                name="name"
                defaultValue={venue.name}
                onChange={handleChange}
              />
              <InputText
                label="City"
                name="city"
                onChange={handleChange}
                defaultValue={venue.city}
              />
              <Label id="demo-controlled-open-select-label">State</Label>
              <InputSelect
                labelId="demo-controlled-open-select-label"
                id="demo-controlled-open-select"
                open={open}
                name="state"
                onClose={handleClose}
                onOpen={handleOpen}
                defaultValue={venue.state}
                value={newVenue.state}
                onChange={handleChange}
              >
                {Object.keys(States).map((ab) => (
                  <MenuItem value={ab} id={ab} key={ab}>
                    {States[ab]}
                  </MenuItem>
                ))}
              </InputSelect>
              <InputText
                defaultValue={venue.address}
                label="Address"
                name="address"
                onChange={handleChange}
              />
              <FormButton type="submit" value="Submit" variant="contained">
                Submit
              </FormButton>
            </form>
          </FormContainer>
          <FormButton onClick={deleteVenue}>Delete Venue</FormButton>
        </Wrapper>
      ) : (
        <div>
          <h2>No Venue found.</h2>
          <FormButton onClick={() => props.history.push("/venues")}>
            Back to Venues
          </FormButton>
        </div>
      )}
    </BigBackground>
  );
};

export default EditVenue;
