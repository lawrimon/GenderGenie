import React, { useState } from 'react';
import './App.css';
import genderLogo from './gender_logo.png';
import LoadingBar from './Loading';



const App = () => {
  const [showContainer, setShowContainer] = useState(false);

  const [text, setText] = useState('');
  const [highlightWords, setHighlightWords] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [keyvalues, setKeyValues] = useState([]);

  const [selectedKeyword, setSelectedKeyword] = useState('');
  const [selectedValue, setSelectedValue] = useState('');

  const [firstInput, setFirstInput] = useState('');
  const [secondInput, setSecondInput] = useState('');

  const suggestionTextfield = () => {
    console.log('First Input:', firstInput);
    console.log('Second Input:', secondInput);
    let suggestion = { firstInput: secondInput }

    fetch('http://141.31.86.15:8000/postSuggestion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(suggestion)
    })
      .then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:', error));
  };

  const handleHighlightClick = (keyword, value) => {
    setSelectedKeyword(keyword);
    setSelectedValue(value);
    setShowPopup(true);
  };

  const handleTextChange = (event) => {
    setText(event.target.value);
    console.log(text, "ist event change")
  };

  const handleSubmit = () => {
    setShowContainer(true);
    fetch('http://192.168.0.135:8000//postText', {
      method: 'POST',
      body: JSON.stringify({ "text": text }),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          console.log(data.message)
          if (data.message === '[]') {
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

  const downloadTxtFile = () => {
    const element = document.createElement("a");
    const file = new Blob([text], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = "Output.txt";
    document.body.appendChild(element);
    element.click();
  }

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

  function extractValues(daten) {
    let keyValuePairs = []
    daten.forEach(obj => {
      Object.entries(obj).forEach(entry => {
        keyValuePairs.push({ key: entry[0], value: "  " + entry[1] })
      });
    });
    return keyValuePairs
  };


  const handleClick = () => {
    setShowPopup(true);
  };

  const handleWordClick = word => {
    console.log(word)
    setText(prevText => prevText.replace(selectedKeyword, word))
    //setText(prevText => prevText.replace(selectedKeyword,  (<span key={word} style={{color: 'blue', cursor: 'pointer'}}>
    //{word}
    //</span>).toString()));
    //setSelectedKeyword(word);
    console.log(text)
    //highlight_keyword(text, word, handleWordClick, "green")
    //const newText = highlight_keyword(text, word)
    //setText(newText);
    //console.log(newText)
    let result = highlight(text, [word], handleHighlightClick)
    console.log(result)
    //setText(text,newText)
    // IN text replace selected word with word!!!
    // Hier Logik einbauen um die Wörter im Text zu ersetzen
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
              <span key={word.key} style={{ color: 'red', cursor: 'pointer' }} onClick={() => handleClick(word.key, word.value)}>
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

  const highlight_keyword = (text, word) => {
    console.log("this text,", text)

    word = word.replace(/\s+/g, '');
    console.log("this word,", word)
    console.log("this wordkey,", word.key)
    let result = [text];
    result = result.flatMap(item => {
      let itemo = item.replace(/\s+/g, '');

      if (typeof itemo === "string") {
        const startIndex = itemo.indexOf(word);
        console.log(startIndex)
        if (startIndex >= 0) {
          const endIndex = startIndex + word.length;
          console.log("im if")
          return [
            itemo.slice(0, startIndex),
            <span key={word} style={{ color: 'green', cursor: 'pointer' }}>
              {word}
            </span>,
            itemo.slice(endIndex)
          ];
        } else {
          return [item];
        }
      } else {
        return [item];
      }
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
        <img src={genderLogo} alt="Image"   style={{ 
          marginTop: '20px', 
          marginBottom: '80px', 
          width: '40%', 
          height: 'auto',
          borderRadius: '10px',
          filter: 'contrast(80%)',
          boxShadow: '0 0 10px rgba(0, 0, 0, 0.2)',
          backgroundColor: '#f2f2f2'
        }} 
      />
        <div>
          <textarea
            className='big-text-field'
            type="text"
            rows={10}
            onChange={handleTextChange} value={text}
          />

          <div>
            <button className="apple-btn" onClick={downloadTxtFile}>Download</button>
            <button className="apple-btn" onClick={handleSubmit}>Submit</button>
            <label for="file-input" className="apple-btn" >Select .txt file</label>
            <input type="file" id="file-input" accept=".txt" onChange={handleUpload} />
          </div>

          {showContainer && <div className='container'>
            <div className='Apple-style-div'>
              {highlight(text, keyvalues, handleHighlightClick)}
            </div>

            {showPopup && (
              <div className='Popup'>
                <div >
                  <b>{selectedKeyword}</b>:{selectedValue.split(",").map((word, index) => (
                    <span key={index} onClick={() => handleWordClick(word)}>
                      {word + ","}
                    </span>
                  ))}
                </div>
              </div>
            )}



          </div> }

          <h2> Suggestion Box</h2>
          <div className="suggestion-box">
            <div className="input-wrapper">
              <input type="text" placeholder="Ungegendertes Wort" value={firstInput} onChange={(e) => setFirstInput(e.target.value)} />
            </div>
            <div className="input-wrapper">
              <input type="text" placeholder="Alternative" value={secondInput} onChange={(e) => setSecondInput(e.target.value)} />
            </div>
            <div className="button-wrapper">
              <button onClick={suggestionTextfield}>Submit</button>
            </div>
          </div>
          <h2>Instant conversion box</h2>
        <LoadingBar />
      </div>
      </header>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50px', backgroundColor: '#f2f2f2', padding: "10px" }}>
        <p style={{ margin: 0, fontSize: '12px' }}>
          Ⓒ GenderInator 2023<br /> Keine Verwendung für kommerzielle Zwecke. <br /> Datensatz erhalten durch https://geschicktgendern.de
        </p>
      </div>
    </div>
  );
};

export default App;
