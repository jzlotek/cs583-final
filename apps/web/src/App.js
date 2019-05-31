import React from 'react'
import ReactDOM from 'react-dom'

import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import Upload from './components/Upload'

import './style/App.css'

const UploadWrapper = () => (
  <React.Fragment>
    <Upload />
  </React.Fragment>
)

const AppWrapper = (children) => (
  <React.Fragment>
    <ToastContainer />
    <h1 className="App-Title">Learning to See in the Dark</h1>
    <a
      className="App-ref"
      href="https://arxiv.org/abs/1805.01934"
      rel="noopener noreferrer"
      target="_blank"
    >
      Based on the research of Chen Chen, Qifeng Chen, Jia Xu, and Vladlen
      Koltun.
    </a>
    {children}
    <div className="App-about">
      <h1>About</h1>
      <p>
        This is our final project for CS583 at Drexel University. The source
        code for this project
      </p>
      <a
        className="App-repo"
        href="https://github.com/jzlotek/cs583-final"
        target="_blank"
        rel="noopener noreferrer"
      >
        can be found here
      </a>
      <a
        className="App-dev"
        href="https://github.com/josephthomashines"
        target="_blank"
        rel="noopener noreferrer"
      >
        <h2>Joseph Hines</h2>
        <span>Frontend Design and Development + Neural Net Optimizations</span>
      </a>
      <a
        className="App-dev"
        href="https://github.com/jzlotek"
        target="_blank"
        rel="noopener noreferrer"
      >
        <h2>John Zlotek</h2>
        <span>Backend Design and Development + Neural Net Optimizations</span>
      </a>
    </div>
  </React.Fragment>
)

const App = () => AppWrapper(UploadWrapper())

toast('Make sure to allow pop-ups from this page', {
  autoClose: 8000,
  className: 'Upload-toast',
})

export default App
