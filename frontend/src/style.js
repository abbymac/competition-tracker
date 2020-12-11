import styled from "styled-components";

export const BigBackground = styled.div`
  display: flex;
  flex-direction: column;
  background: #f2f2f2;
  align-items: center;
  height: 100%;
  justify-content: ${(props) => (props.align ? props.align : "flex-start")};
`;

export const TableWrapper = styled.div`
  width: 80%;
  margin: 0 auto;
`;
