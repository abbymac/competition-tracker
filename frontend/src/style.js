import styled from "styled-components";
import TableRow from "@material-ui/core/TableRow";
import TextField from "@material-ui/core/TextField";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import Button from "@material-ui/core/Button";

export const BigBackground = styled.div`
  display: flex;
  flex-direction: column;
  background: #f2f2f2;
  align-items: center;
  height: 100%;
  width: 100%;
  justify-content: ${(props) => (props.align ? props.align : "flex-start")};
`;

export const Wrapper = styled.div`
  width: 80%;
  margin: 0 auto;
`;

export const Row = styled(TableRow)`
  &:hover {
    background-color: #4682b4;
    color: #f4f4f4;
    cursor: pointer;
  }
  &:active {
    background-color: #4682b4;
    color: #f4f4f4;
    transition: all 0.2s linear;
  }
  transition: all 0.2s linear;
`;

export const InputText = styled(TextField)`
  margin-top: 10px;
  width: 100%;
`;

export const InputSelect = styled(Select)`
  width: 100%;
`;

export const Label = styled(InputLabel)`
  width: 100%;
  margin-top: 10px;
`;

export const FormContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
`;

export const FormButton = styled(Button)`
  margin-top: 10px !important;
`;

export const RowSection = styled.div`
  width: 100%;
  display: flex;
`;
