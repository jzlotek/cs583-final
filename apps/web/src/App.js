import React from 'react'
import ReactDOM from 'react-dom'

import Upload from './components/Upload'

import './style/App.css'

const UploadWrapper = () => (
  <div>
    <Upload />
  </div>
)

const AppWrapper = (children) => (
  <div className="App-Wrapper">
    <h1 className="App-Title">Learning to See in the Dark</h1>
    {children}
  </div>
)

const App = () => AppWrapper(UploadWrapper())

export default App
