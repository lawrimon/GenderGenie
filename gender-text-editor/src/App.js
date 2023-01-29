import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [text, setText] = useState('');
  const [highlightWords, setHighlightWords] = useState([]);
  const [showPopup, setShowPopup] = useState(false);

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const handleSubmit = () => {
    fetch('http://192.168.178.96:8000/postText', {
      method: 'POST',
      body: JSON.stringify({"text":text}),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
          console.log(data.message)
          let keywords = extractKeywords(data.message);
          setHighlightWords(keywords);
      }
  })
    .catch(error => {
      console.error(error);
    });
  };

  function extractKeywords(daten) {
    console.log("in extract")
    console.log(daten)
    let keywords = []
    daten.forEach(obj => {
        Object.keys(obj).forEach(key => {
            keywords.push(key)
        });
    });
    return keywords
  };

  const handleClick = () => {
    setShowPopup(true);
  };
  
  
  const highlight = (text, words) => {
    let highlightedText = text;
    words.forEach((word) => {
      highlightedText = highlightedText.replace(
        new RegExp(`(${word})`, 'gi'),
        `<span style='color:red; cursor:pointer;' }>$1</span>`
      );
    });
    return highlightedText;
  };
  
  
  

  return (
    <div className="App">
      <header className="App-header">
        <div>
        <textarea 
       className='big-text-field'
        type="text"
        rows={10}
         onChange={handleTextChange} value={text} />
      <button onClick={handleSubmit}>Submit</button>
      <div
  dangerouslySetInnerHTML={{
    __html: highlight(text, highlightWords),
  }}
  onClick={handleClick}
/>

        {showPopup && (
        <div style={{ position: 'absolute', color: 'black', backgroundColor: 'white', padding: '10px' }}>
          Dies ist ein Popup
        </div>
      )}
        </div>
      </header>
    </div>
  );
};

export default App;
