import React, { useState, useEffect } from 'react';
import './Loading.css';


  


const LoadingBar = () => {
    const [processedText, setProcessedText] = useState(false);
    const [filename, setFilename] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [fileSize, setfileSize] = useState(false);

  let text = "";

const handleUploadConversion = (event) => {
    // prevent default behavior of form submission
    event.preventDefault();

    // access the first file in the input field
    const file = event.target.files[0];

    // create a new instance of FileReader
    const reader = new FileReader();

    // handle the load event after reading the file
    reader.onload = (e) => {
      // set the contents of the file as the text value
      text = e.target.result;
      // call the handleSubmit function
      console.log(text, "is the text")
    };
    setfileSize(document.getElementById("conversion-input").files[0].size);
    
    console.log("File size:", fileSize);

    // start reading the file as text
    reader.readAsText(file);
  };

const handleSubmit = () => {
fetch('http://192.168.0.135:8000//automaticConversion', {
    method: 'POST',
    body: JSON.stringify({ "text": text }),
    headers: { 'Content-Type': 'application/json' },
})
    .then(response => response.json())
    .then(data => {
    if (data) {
        console.log(data)
        if (data === '[]') {
        console.log("Im IF")
        return
        }
    }
        console.log(data)
        setFilename("processed_text.txt")
        setProcessedText(data)
        
    })
    .catch(error => {
    console.error(error);
    });
};

function downloadTextFile(content, filename) {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
  
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

  const startConversion = () => {
    setIsLoading(true);
    setShowSuccessMessage(false);
    handleSubmit();
    setfileSize(document.getElementById("conversion-input").files[0].size);
    
    console.log("File size:", fileSize);


    // Simulate a loading effect
    setTimeout(() => {
      setIsLoading(false);
      setShowSuccessMessage(true);

      // Hide the success message after 10 seconds
      setTimeout(() => {
        setShowSuccessMessage(false);
      }, 4000);
    }, (fileSize * 10)); // Reduced the loading time for demonstration purposes
  };

  useEffect(() => {
    if (!isLoading && !showSuccessMessage) {
      setIsLoading(false);
    }
  }, [isLoading, showSuccessMessage]);

  return (
    <div className="suggestion-box">
      {!isLoading && !showSuccessMessage && (
        <div>

        <div className="button">
          <button onClick={startConversion}>Start Conversion</button>
        </div>
        <label htmlFor="conversion-input" className="apple-btn">
        Select .txt file
        </label>
        <input type="file" id="conversion-input" accept=".txt , .tex" onChange={handleUploadConversion} />

      </div>
      )}
      {isLoading && (
        <div className="loading-bar-container">
          <div className="loading-bar"
          style={{ animation: `loading-animation ${fileSize / 120}s linear forwards` }}>
            </div>
        </div>
      )}
      {showSuccessMessage && (
        <div className="conversion-success">
          <div className="success-message">CONVERSION SUCCESSFUL</div>
          <div className="button">
            <button onClick={downloadTextFile(processedText, filename)}>Download File</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LoadingBar;
