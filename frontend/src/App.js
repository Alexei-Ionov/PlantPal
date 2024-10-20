import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import Profile from './pages/profile';
import NavBar from './components/Navbar';
import Login from './pages/login';
import SignUp from './pages/signup';

import MyPlants from './pages/myPlants';
import { AuthProvider } from './components/AuthContext';
function App() {
  return (
    <AuthProvider>
      <Router>
        <div>
          <NavBar/>
          <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/profile" element={<Profile/>}/>
            <Route path="/login" element={<Login/>}/>
            <Route path="/signup" element={<SignUp/>}/>
            <Route path="/my_plants" element={<MyPlants/>}/>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;