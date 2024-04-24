import logo from './logo..png';
import './App.css';
import { useState, useEffect, useRef } from 'react';
import PDFViewer from './pdfInput';
import Main from './components/Main';


function App() {
  
  const [inputState, setInputState] = useState('');

  const [data, setData] = useState({
    name: "",
    date: "", 
    embeddings: "", 
    pdf: ""
  });

  useEffect (() => {
  try{  
    fetch("http://127.0.0.1:5000/data").then((res) =>
      res.json().then((data) => {
      //setting data from the api
      setData({
        name:data.Name,
        date: data.Date, 
        embeddings: data.Embeddings, 
        pdf: data.pdf
      });
    })
  );}
  catch (e){
    console.log(e, e.stack)
  }
  }, []);

  
  
  
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
        <div></div>
        
      <Main className="main"></Main>
      </header>
      
    </div>
  );
}

export default App;
