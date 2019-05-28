import React from 'react'
import '../style/Upload.css'
import 'babel-polyfill'

class Upload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  render() {
    return (
      <div className="Upload">
        <span className="Title">Upload Files</span>
      </div>
    )
  }
}

export default Upload
