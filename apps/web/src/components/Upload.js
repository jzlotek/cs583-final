import React from 'react'
import '../style/Upload.css'
import 'babel-polyfill'

class Upload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
    this.fileInputRef = React.createRef()

    this.openFileDialog = this.openFileDialog.bind(this)
    this.onFilesAdded = this.onFilesAdded.bind(this)
  }

  onFilesAdded(evt) {
    if (this.props.disabled) return
    const files = evt.target.files
    // pass files to function to make POST
    console.log(files)
  }

  openFileDialog() {
    if (this.props.disabled) return
    this.fileInputRef.current.click()
  }

  render() {
    return (
      <div
        className="Upload"
        onClick={this.openFileDialog}
        style={{ cursor: this.props.disabled ? 'default' : 'pointer' }}
      >
        <input
          ref={this.fileInputRef}
          className="FileInput"
          type="file"
          multiple
          onChange={this.onFilesAdded}
        />
        <span className="Title">Upload Files</span>
      </div>
    )
  }
}

export default Upload
