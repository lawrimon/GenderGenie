import React, { useEffect, useState } from 'react';

export function AdminPage() {
  const [feedbackData, setFeedbackData] = useState([]);
  const [genderSuggestionsData, setGenderSuggestionsData] = useState([]);
  const feedbackCollectionName = 'Feedback'; // Replace with the actual collection name
  const genderSuggestionsCollectionName = 'GenderSuggestions'; // Replace with the actual collection name

  useEffect(() => {
    fetch(`http://192.168.0.135:8000/collection/${feedbackCollectionName}`)
      .then(response => response.json())
      .then(data => setFeedbackData(data.data))
      .catch(error => console.error('Error fetching feedback data:', error));

    fetch(`http://192.168.0.135:8000/collection/${genderSuggestionsCollectionName}`)
      .then(response => response.json())
      .then(data => setGenderSuggestionsData(data.data))
      .catch(error => console.error('Error fetching gender suggestions data:', error));
  }, []);

  const handleApproveClick = (index, collectionName) => {
    const item = collectionName === feedbackCollectionName ? feedbackData[index] : genderSuggestionsData[index];
    const value = item.word || item.text;

    fetch(`http://192.168.0.135:8000/${collectionName}/approve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'word': value })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Item approved:', data);
        // Refresh the data
        if (collectionName === feedbackCollectionName) {
          refreshFeedbackData();
        } else if (collectionName === genderSuggestionsCollectionName) {
          refreshGenderSuggestionsData();
        }
      })
      .catch(error => console.error('Error approving item:', error));
  };

  const handleDeleteClick = (index, collectionName) => {
    const item = collectionName === feedbackCollectionName ? feedbackData[index] : genderSuggestionsData[index];
    const value = item.word || item.text;

    fetch(`http://192.168.0.135:8000/${collectionName}/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'word': value })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Item deleted:', data);
        // Refresh the data
        if (collectionName === feedbackCollectionName) {
          refreshFeedbackData();
        } else if (collectionName === genderSuggestionsCollectionName) {
          refreshGenderSuggestionsData();
        }
      })
      .catch(error => console.error('Error deleting item:', error));
  };

  const refreshFeedbackData = () => {
    fetch(`http://192.168.0.135:8000/collection/${feedbackCollectionName}`)
      .then(response => response.json())
      .then(data => setFeedbackData(data.data))
      .catch(error => console.error('Error refreshing feedback data:', error));
  };

  const refreshGenderSuggestionsData = () => {
    fetch(`http://192.168.0.135:8000/collection/${genderSuggestionsCollectionName}`)
      .then(response => response.json())
      .then(data => setGenderSuggestionsData(data.data))
      .catch(error => console.error('Error refreshing gender suggestions data:', error));
  };

  return (
    <div>
      <h1>Admin Page</h1>
      <p>Welcome to the Admin Page. This is a protected area.</p>

      <h2>Collection: {feedbackCollectionName}</h2>

      <h3>Feedback Data:</h3>
      <table>
        <thead>
          <tr>
            <th>Value</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {feedbackData.map((item, index) => (
            <tr key={index}>
              <td>{item.word || item.text}</td>
              <td>
                <button onClick={() => handleDeleteClick(index, feedbackCollectionName)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Collection: {genderSuggestionsCollectionName}</h2>

      <h3>Gender Suggestions Data:</h3>
      <table>
        <thead>
          <tr>
            <th>Value</th>
            <th>Approve</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {genderSuggestionsData.map((item, index) => (
            <tr key={index}>
              <td>{item.word || item.text}</td>
              <td>
                <button onClick={() => handleApproveClick(index, genderSuggestionsCollectionName)}>Approve</button>
              </td>
              <td>
                <button onClick={() => handleDeleteClick(index, genderSuggestionsCollectionName)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPage;
