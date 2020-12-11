import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { TableWrapper } from "../style.js";

const VenueView = () => {
  const [venues, setVenues] = useState([]);
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

  return (
    <TableWrapper>
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
                <TableRow key={venue.id}>
                  <TableCell component="th" scope="row">
                    {venue.name}
                  </TableCell>
                  <TableCell align="right">{venue.city}</TableCell>
                  <TableCell align="right">{venue.state}</TableCell>
                  <TableCell align="right">{venue.address}</TableCell>
                  <TableCell align="right">{venue.races}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </TableWrapper>
  );
};

export default VenueView;
