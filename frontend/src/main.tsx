import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './pages/App/App.tsx'
import {GlobalStyle} from "./styles/global.ts";

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
      <GlobalStyle></GlobalStyle>
  </React.StrictMode>,
)
