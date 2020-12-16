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

const AthleteView = () => {
  const [athletes, setAthletes] = useState([]);
  var getAthletes = () => {
    axios
      .get("/api/athletes")
      .then(function (response) {
        // handle success
        console.log(response.data);
        setAthletes(response.data.athletes);
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
    getAthletes();
  }, []);

  return (
    <Wrapper>
      <h1>Athletes</h1>

      {athletes.length == 0 ? (
        <div>no athletes</div>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Athlete</TableCell>
                <TableCell align="right">Age</TableCell>
                <TableCell align="right">City</TableCell>
                <TableCell align="right">State</TableCell>
                <TableCell align="right">Phone</TableCell>
                <TableCell align="right">Division</TableCell>
                <TableCell align="right">Races</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {athletes.map((athlete) => (
                <TableRow key={athlete.id}>
                  <TableCell component="th" scope="row">
                    {athlete.name}
                  </TableCell>
                  <TableCell align="right">{athlete.age}</TableCell>
                  <TableCell align="right">{athlete.city}</TableCell>
                  <TableCell align="right">{athlete.state}</TableCell>
                  <TableCell align="right">{athlete.phone}</TableCell>
                  <TableCell align="right">{athlete.division}</TableCell>
                  <TableCell align="right">{athlete.races}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Wrapper>
  );
};

export default AthleteView;
