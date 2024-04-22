import React from 'react';

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);
    console.log(this.state)

    fetch("http://127.0.0.1:5000/upload", {
      method: 'POST',
      /*body: {
        file: ('file', this.uploadInput.files[0]), 
        name: ('filename', this.fileName.value)
      },*/
       body: data, 
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ imageURL: `http://127.0.0.1:5000/${body.file}` });
      });
    });
  }

  render() {
    return (
      <div>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div>
        <br />
        <div>
          <button onClick={this.handleUploadImage}>Upload</button>
        </div>
        
      </div>
    );
  }
}

export default Main;