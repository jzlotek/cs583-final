import React from 'react'
import ReactDOM from 'react-dom'

import Dropzone from './Dropzone'

import './style/App.css'

const DropzoneWrapper = () => (
  <div>
    <Dropzone onFilesAdded={console.log} />
  </div>
)

const AppWrapper = (children) => (
  <div className="App-Wrapper">
    <h1 className="App-Title">Learning to See in the Dark</h1>
    {children}
  </div>
)

const App = () => AppWrapper(DropzoneWrapper())

export default App
