import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { Wrapper } from "../style.js";

const RaceView = () => {
  const [races, setRaces] = useState([]);
  var getVenues = () => {
    axios
      .get("/api/races")
      .then(function (response) {
        // handle success
        console.log(response.data);
        setRaces(response.data.races);
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
    <Wrapper>
      <h1>Races</h1>

      {races.length == 0 ? (
        <div>no races</div>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Race</TableCell>
                <TableCell align="right">Division</TableCell>
                <TableCell align="right">Prize</TableCell>
                <TableCell align="right">Start Time</TableCell>
                <TableCell align="right">Venue</TableCell>
                <TableCell align="right">City</TableCell>
                <TableCell align="right">State</TableCell>
                <TableCell align="right">Racers</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {races.map((race) => (
                <TableRow key={race.id}>
                  <TableCell component="th" scope="row">
                    <a href={"/races/" + race.id}>{race.name}</a>
                  </TableCell>
                  <TableCell align="right">{race.division}</TableCell>
                  <TableCell align="right">{race.prize}</TableCell>
                  <TableCell align="right">{race.start_time}</TableCell>
                  <TableCell align="right">{race.venue.name}</TableCell>
                  <TableCell align="right">{race.venue.city}</TableCell>
                  <TableCell align="right">{race.venue.state}</TableCell>
                  <TableCell align="right">{race.racers.length}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Wrapper>
  );
};

export default RaceView;
