import React from 'react';
import { BrowserRouter as Router, Switch, Route, Routes} from 'react-router-dom';
import HomePage from './Home';
import AdminPage from './Admin';

const App = () => {
  return (
    <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/admin" element={<AdminPage />} />

    </Routes>
  );
};

export default App;
