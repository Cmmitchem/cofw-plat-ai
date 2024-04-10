import logo from './logo.svg';
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

  function handleClick () {
    console.log(inputState)
  }
  
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <textarea onChange={e => setInputState(e.target.value)}></textarea>
        <button onClick={handleClick}>Sumbit Request</button>
        <PDFViewer></PDFViewer>
        <p>{data.name}</p>
      <p>{data.date}</p>
      <p>{data.embeddings}</p>
      <p>{data.pdf}</p>
      <Main></Main>
      </header>
      
    </div>
  );
}

export default App;
