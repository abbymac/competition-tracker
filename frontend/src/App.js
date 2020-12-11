import AthleteView from "./components/AthleteView";
import VenueView from "./components/VenueView";
import HomeView from "./components/HomeView";
import RaceView from "./components/RaceView";

import NavBar from "./components/NavBar";
import { useMediaQuery } from "react-responsive";
import React, { useEffect, useState, useRef } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import { BigBackground } from "./style.js";

function App() {
  const [navBackground, setNavBackground] = useState(false);

  const navRef = useRef();
  navRef.current = navBackground;

  useEffect(() => {
    const handleScroll = () => {
      const show = window.scrollY > 1;
      if (navRef.current !== show) {
        setNavBackground(show);
      }
    };
    document.addEventListener("scroll", handleScroll);
    return () => {
      document.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const isMobileSize = useMediaQuery({
    query: "(max-device-width: 768px)",
  });

  return (
    <BigBackground>
      {/* <div className="App"> */}
      <NavBar mobile={isMobileSize} transparent={navBackground} />
      <Router>
        <Switch>
          <Route path="/" exact component={HomeView} />
          <Route path="/athletes" exact component={AthleteView} />
          <Route path="/venues" exact component={VenueView} />
          <Route path="/races" exact component={RaceView} />
        </Switch>
      </Router>
      {/* <main>
        <AthleteView />
        <VenueView />
      </main> */}
      {/* </div> */}
    </BigBackground>
  );
}

export default App;
