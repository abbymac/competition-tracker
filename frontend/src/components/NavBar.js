import React from "react";
import styled from "styled-components";
// import { Link } from "react-scroll";
import { NavLink } from "react-router-dom";

const NavBar = ({ transparent, mobile }) => {
  return (
    <NavContain transparent={transparent}>
      <Left>
        {/* <NavItem
          activeClass="active"
          to="experiences"
          spy={true}
          smooth={true}
          offset={mobile ? 0 : -60}
          duration={500}
        >
          Athletes
        </NavItem>
        <NavItem
          activeClass="active"
          to="skills"
          spy={true}
          smooth={true}
          offset={mobile ? 0 : -60}
          duration={500}
        >
          Venues
        </NavItem>
        <NavItem
          activeClass="active"
          to="about"
          spy={true}
          smooth={true}
          offset={mobile ? 0 : -60}
          duration={500}
        >
          Races
        </NavItem>
        <NavItem
          activeClass="active"
          to="projects"
          spy={true}
          smooth={true}
          offset={mobile ? 0 : -60}
          duration={500}
        >
          Projects
        </NavItem> */}
        <NavItem to="/">Home</NavItem>
        <NavItem to="/athletes">Athletes</NavItem>
        <NavItem to="/venues">Venues</NavItem>
        <NavItem to="/races">Races</NavItem>
      </Left>
    </NavContain>
  );
};

export default NavBar;

const Left = styled.div`
  flex-grow: 1;
  padding-left: 20px;
`;

const NavContain = styled.div`
  position: initial;
  top: 0px;
  width: 100%;
  max-width: 100vw;
  height: 60px;
  z-index: 1000;
  box-shadow: ${(props) =>
    !props.transparent ? "none" : "0 0px 4px 0 rgba(0, 0, 0, 0.15)"};
  display: inline-flex;
  align-items: center;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  transition: background-color 0.5s ease;

  background-color: ${(props) =>
    !props.transparent ? "rgba(0,0,0,0)" : "rgb(11, 13, 17)"};
  justify-content: flex-start;

  @media (max-width: 768px) {
    display: none;
  }
`;

const NavItem = styled(NavLink)`
  color: black;
  text-decoration: none;
  margin: 0 10px;
  &:hover {
    color: #75829e;
    cursor: pointer;
  }
  &.active {
    color: #5c80a3;
    transition: all 0.2s linear;
  }
`;
