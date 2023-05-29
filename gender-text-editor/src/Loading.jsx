import React, { useState, useEffect } from 'react';
import './Loading.css';

const LoadingBar = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  const startConversion = () => {
    setIsLoading(true);
    setShowSuccessMessage(false);

    // Simulate a loading effect
    setTimeout(() => {
      setIsLoading(false);
      setShowSuccessMessage(true);

      // Hide the success message after 10 seconds
      setTimeout(() => {
        setShowSuccessMessage(false);
      }, 10000);
    }, 6000); // Reduced the loading time for demonstration purposes
  };

  useEffect(() => {
    if (!isLoading && !showSuccessMessage) {
      setIsLoading(false);
    }
  }, [isLoading, showSuccessMessage]);

  return (
    <div className="suggestion-box">
      {!isLoading && !showSuccessMessage && (
        <div className="button">
          <button onClick={startConversion}>Start Conversion</button>
        </div>
      )}
      {isLoading && (
        <div className="loading-bar-container">
          <div className="loading-bar"></div>
        </div>
      )}
      {showSuccessMessage && (
        <div className="conversion-success">
          <div className="success-message">CONVERSION SUCCESSFUL</div>
          <div className="button">
            <button onClick={console.log("lol")}>Download File</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LoadingBar;
