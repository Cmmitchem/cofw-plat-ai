import React from 'react';
import { useState } from 'react';


class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      filePath : "", 
      file : "",
      prompt : "", 
      response : ""
    };
    

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }


  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.filePrompt.value);
    
    console.log(this.filePrompt.value)
    console.log(this.state)

    fetch("http://127.0.0.1:5000/upload", {
      method: 'POST',
       body: data, 
       
    }).then((response) => {
      
      if (response.ok) {
        return response.json(); // Parse the JSON only if the response was successful
    }
    throw new Error('Failed to fetch: ' + response.statusText); // Throw an error if the response was not ok
    }).then(json => {
    // Assuming json is the parsed JSON object
    if (json.plat_list && json.plat_list.length > 0) {
        const latestResponse = json.plat_list[0]; // Access the first item of the plat_list array
        this.setState({
            filePath: latestResponse.FilePath, 
            file: latestResponse.File, 
            prompt: latestResponse.Prompt,
            response: latestResponse.Response // Make sure it matches the JSON structure
        });
        console.log(latestResponse);
    } else {
        console.log("No data found in the response.");
    }
    }).catch(error => {
    // Handle any errors that occur during the fetch process
      console.error("Error fetching data:", error);
  });
  }

  fetchResponse = async () => {
    try{
      const res = await fetch("http://127.0.0.1:5000/upload") 
      const json = await res.json();

      if (json.responses && json.responses.length > 0){
        const latestResponse = json.responses[0];
        this.setState({
          filePath: latestResponse.FilePath, 
          file: latestResponse.File, 
          prompt: latestResponse.Prompt,
          response: latestResponse.response
        })
        console.log(this.state)
      }
    } catch (e){
      console.error("Failed to fetch response:", e);
    }
  };


  render() {
    return (
      <div>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <div>
          <input ref={(ref) => { this.filePrompt = ref; }} type="text" placeholder="Enter prompt here" className='prompt'/>
        </div>
        <br />
        <div>
          <button onClick={this.handleUploadImage} className='upload'>Upload File</button>
          <div>{this.state.response}</div>
          
        </div>
        
      </div>
    );
  }
}

export default Main;