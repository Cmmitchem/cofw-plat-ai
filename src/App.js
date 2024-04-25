import logo from './logo..png';
import './App.css';
import { useState, useEffect, useRef } from 'react';
import PDFViewer from './pdfInput';
import Main from './components/Main';


function App() {
  
  const [inputState, setInputState] = useState('');

  const [data, setData] = useState({
    id: "",
    awards: "", 
    cast: [], 
    countries: []
  });


 /* useEffect (() => {
    const fetchData = async () => {
      
      try {
        const res = await fetch("http://127.0.0.1:5000/all_movies");
        const json = await res.json();

        if (json.movies && json.movies.length > 0) {
          const firstMovie = json.movies[0];
          setData({
            id: firstMovie._id.$oid, // Accessing the $oid value
            awardsText: firstMovie.awards.text, // Accessing the awards text
            cast: firstMovie.cast, // Accessing all cast members
            directors: firstMovie.directors // Accessing all directors
          });
        }
      } catch (e) {
        console.error("Failed to fetch movies:", e);
      }
    }; 
    fetchData();
  }, []);*/

    const fetchData = async () => {
      
      try {
        const res = await fetch("http://127.0.0.1:5000/all_movies");
        const json = await res.json();

        if (json.movies && json.movies.length > 0) {
          const firstMovie = json.movies[0];
          setData({
            id: firstMovie._id.$oid, // Accessing the $oid value
            awardsText: firstMovie.awards.text, // Accessing the awards text
            cast: firstMovie.cast, // Accessing all cast members
            directors: firstMovie.directors // Accessing all directors
          });
        }
      } catch (e) {
        console.error("Failed to fetch movies:", e);
      }
    }; 

 


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>COFW AI Plat Analyzer</h1>
        <a
          className="App-link"
          href="https://www.fortworthtexas.gov/departments/development-services/platting"
          target="_blank"
          rel="noopener noreferrer"
        >
          COFW Plat Information
        </a>
        <div>{data.id}</div>
        <div>{data.awardsText}</div>
        <button onClick={fetchData}>Fetch Movie Data</button>
        <p></p>
      <Main className="main"></Main>
      </header>
      
    </div>
  );
}

export default App;
