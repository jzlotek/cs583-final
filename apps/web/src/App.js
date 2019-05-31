import React from 'react'
import ReactDOM from 'react-dom'

import { ToastContainer } from 'react-toastify'
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
  </React.Fragment>
)

const App = () => AppWrapper(UploadWrapper())

export default App
