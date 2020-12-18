import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import MenuItem from "@material-ui/core/MenuItem";

import {
  Wrapper,
  Row,
  BigBackground,
  FormContainer,
  InputText,
  InputSelect,
  Label,
  FormButton,
} from "../style.js";

import { States } from "./States.js";

const VenueView = () => {
  const [venues, setVenues] = useState([]);
  const [newVenue, setNewVenue] = useState({
    name: "",
    city: "",
    state: "",
    address: "",
  });
  const [open, setOpen] = React.useState(false);

  var getVenues = () => {
    axios
      .get("/api/venues")
      .then(function (response) {
        // handle success
        console.log(response.data);
        setVenues(response.data.venues);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
  };
  useEffect(() => {
    getVenues();
  }, []);

  const handleClick = (e) => {
    console.log("here", e);
  };

  const handleChange = (e) => {
    e.preventDefault();
    console.log("name", e.target.name);
    console.log("value", e.target.value);

    // console.log("o name", venues);
    setNewVenue((prevVal) => {
      return {
        ...prevVal,
        [e.target.name]: e.target.value,
      };
    });
    // setNewVenue({ [e.target.name]: e.target.value });
  };

  const submitVenue = (e) => {
    e.preventDefault();
    console.log("name", newVenue.name);
    console.log("city", newVenue.city);
    console.log("tot", newVenue);
    axios
      .post("/api/venues", newVenue)
      .then(function (response) {
        // handle success
        console.log(response.data);
        setVenues((prevVenues) => [...prevVenues, newVenue]);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  return (
    <BigBackground>
      <Wrapper>
        <h1>Venues</h1>

        {venues.length == 0 ? (
          <div>no venues</div>
        ) : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Venue</TableCell>
                  <TableCell align="right">City</TableCell>
                  <TableCell align="right">State</TableCell>
                  <TableCell align="right">Address</TableCell>
                  <TableCell align="right">Races</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {venues.map((venue) => (
                  <Row key={venue.id} onClick={(e) => handleClick(e)}>
                    <TableCell component="th" scope="row">
                      <a href={"/venues/" + venue.id}>{venue.name}</a>
                    </TableCell>
                    <TableCell align="right">{venue.city}</TableCell>
                    <TableCell align="right">{venue.state}</TableCell>
                    <TableCell align="right">{venue.address}</TableCell>
                    <TableCell align="right">{venue.races}</TableCell>
                  </Row>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Wrapper>
      <Wrapper>
        <h2>Add a New Venue</h2>
        <FormContainer>
          <form onSubmit={submitVenue}>
            <InputText label="Venue Name" name="name" onChange={handleChange} />
            <InputText label="City" name="city" onChange={handleChange} />
            <Label id="demo-controlled-open-select-label">State</Label>
            <InputSelect
              labelId="demo-controlled-open-select-label"
              id="demo-controlled-open-select"
              open={open}
              name="state"
              onClose={handleClose}
              onOpen={handleOpen}
              value={newVenue.state}
              onChange={handleChange}
            >
              {Object.keys(States).map((ab) => (
                <MenuItem value={ab} id={ab} key={ab}>
                  {States[ab]}
                </MenuItem>
              ))}
            </InputSelect>
            <InputText label="Address" name="address" onChange={handleChange} />
            <FormButton type="submit" value="Submit" variant="contained">
              Submit
            </FormButton>
          </form>
        </FormContainer>
      </Wrapper>
    </BigBackground>
  );
};

export default VenueView;
