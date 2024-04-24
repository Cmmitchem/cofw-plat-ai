import React from "react";

class MongoDB extends React.Component{

    getData(){
        fetch("http://127.0.0.1:5000/api/v1/movies/all_movies", {
        method: 'GET',
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
}

export default MongoDB;