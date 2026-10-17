import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import { CollegeApp } from './college/CollegeApp';
import './index.css';
import './college/college.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {window.location.pathname.startsWith('/scms') ? <CollegeApp /> : <App />}
  </React.StrictMode>,
);
