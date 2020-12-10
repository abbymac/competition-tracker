import logo from "./logo.svg";
import "./App.css";
import AthleteView from "./components/AthleteView";
import VenueView from "./components/VenueView";

import { BigBackground } from "./style.js";

function App() {
  return (
    <BigBackground>
      <div className="App">
        <AthleteView />
        <VenueView />
      </div>
    </BigBackground>
  );
}

export default App;
