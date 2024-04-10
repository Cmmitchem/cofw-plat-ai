import { Document, Page } from '@react-pdf/renderer';
import React from 'react';
//https://react-pdf.org 
//https://www.shecodes.io/athena/12109-how-to-upload-a-pdf-file-in-react#:~:text=To%20upload%20a%20PDF%20file%20in%20React%2C%20you%20can%20create,in%20React%20component%20using%20state.&text=Then%2C%20you%20can%20send%20the,party%20library%20like%20react%2Dpdf.


class PDFViewer extends React.Component {
  state = {
    selectedFile: null,
    numPages: null,
    pageNumber: 1,
  }

  onFileLoad = ({ target: { result } }) => {
    this.setState({ pdfData: result });
  }

  onDocumentLoadSuccess = ({ numPages }) => {
    this.setState({ numPages });
  }

  render() {
    const { pageNumber, numPages, pdfData } = this.state;
    return (
      <>
        <input type="file" accept=".pdf" onChange={(event) => this.onFileLoad(event)} />

        {pdfData && (
          <Document file={pdfData} onLoadSuccess={this.onDocumentLoadSuccess}>
            <Page pageNumber={pageNumber} />
          </Document>
        )}

        {pdfData && (
          <p>Page {pageNumber} of {numPages}</p>
        )}
      </>
    );
  }
}

export default PDFViewer;