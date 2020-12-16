import styled from "styled-components";
import TableRow from "@material-ui/core/TableRow";

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
