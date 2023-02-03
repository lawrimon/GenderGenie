import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [text, setText] = useState('');
  const [highlightWords, setHighlightWords] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [keyvalues, setKeyValues] = useState([]);

  const [selectedKeyword, setSelectedKeyword] = useState('');
const [selectedValue, setSelectedValue] = useState('');

const handleHighlightClick = (keyword, value) => {
  setSelectedKeyword(keyword);
  setSelectedValue(value);
  setShowPopup(true);
};

  const handleTextChange = (event) => {
    setText(event.target.value);
    console.log(text,"ist event change")
  };

  const handleSubmit = () => {
    fetch('http://192.168.0.135:8000/postText', {
      method: 'POST',
      body: JSON.stringify({"text":text}),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
          console.log(data.message)
          if (data.message ==='[]'){
            console.log("Im IF")
            setText("Sie haben alles gender-neutral verfasst! :)")
            return
          }
          let keywords = extractKeywords(data.message);
          let keyvalues = extractValues(data.message);
          console.log(keyvalues);
          setHighlightWords(keywords);
          setKeyValues(keyvalues);
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

  function extractValues(daten){
    let keyValuePairs = []
    daten.forEach(obj => {
        Object.entries(obj).forEach(entry => {
            keyValuePairs.push({key: entry[0],value: "  " + entry[1]})
        });
    });
    return keyValuePairs
  };

  
  const handleClick = () => {
    setShowPopup(true);
  };
  
  
  const highlight = (text, words, handleClick) => {
    let result = [text];
    words.forEach(word => {
      result = result.flatMap(item => {
        if (typeof item === "string") {
          const startIndex = item.indexOf(word.key);
          if (startIndex >= 0) {
            const endIndex = startIndex + word.key.length;
            return [
              item.slice(0, startIndex),
              <span key={word.key} style={{color: 'red', cursor: 'pointer'}} onClick={() => handleClick(word.key, word.value)}>
                {word.key}
              </span>,
              item.slice(endIndex)
            ];
          } else {
            return [item];
          }
        } else {
          return [item];
        }
      });
    });
    return result;
  };
  

  
  const handleUpload = (event) => {
    // prevent default behavior of form submission
    event.preventDefault();
  
    // access the first file in the input field
    const file = event.target.files[0];
  
    // create a new instance of FileReader
    const reader = new FileReader();
  
    // handle the load event after reading the file
    reader.onload = (e) => {
      // set the contents of the file as the text value
      setText(e.target.result);
      // call the handleSubmit function
      handleSubmit();
    };
  
    // start reading the file as text
    reader.readAsText(file);
  };

  
  const uploadSubmit = (event) => {
    // call the handleSubmit function
    handleSubmit(event);
  }
  
  
  
  

  return (
    <div className="App">
      <header className="App-header">
        <h1>-Gender-API-</h1>
        <div>
        <textarea 
       className='big-text-field'
        type="text"
        rows={10}
         onChange={handleTextChange} value={text} 
       />
<div style = {{padding: '20px'}}><button style ={{
  width:'60px', 
  height:'40px',
  borderradius: '10px',
  backgroundcolor: '#007bff',
  color: 'white',
  fontsize: '16px',
  border: 'none',
  cursor: 'pointer',
  }}
  onClick={handleSubmit}>Submit</button> </div>
 <input
      type="file"
      accept=".txt"
      style={{left: '60%', padding: '20px'}}
      onChange={handleUpload}
    />
        <div style={{ display: 'flex' , padding: '20px', backgroundColor: 'gray', backgroundClip: 'padding-box' }}>
        <div style = {{padding: '20px'}} >
  {highlight(text, keyvalues, handleHighlightClick)}
</div>
 {showPopup && (
  <div style={{ 
    position: 'relative', 
    color: 'black', 
    backgroundColor: 'white', 
    padding: '15px', 
    width: '120%', 
    left: '0',
    height: '250px',
    top: '0', 
    overflow: 'scroll',
    whitespace: 'prewrap',
    wordwrap: 'breakword'
  }}>
    <div >      
      <b>{selectedKeyword}:</b> {selectedValue}
    </div>
  </div>  
)}


</div>






        </div>
      </header>
    </div>
  );
};

export default App;
