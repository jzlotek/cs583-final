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
    this.onDragOver = this.onDragOver.bind(this)
    this.onDragLeave = this.onDragLeave.bind(this)
    this.onDrop = this.onDrop.bind(this)
    this.handleFiles = this.handleFiles.bind(this)
    this.getBase64 = this.getBase64.bind(this)
  }

  handleFiles(files) {
    let promises = []

    for (let i = 0; i < files.length; i++) {
      promises.push(
        new Promise((res) => {
          this.getBase64(files[i], (result) => {
            res(result)
          })
        }),
      )
    }

    Promise.all(promises).then((data) => {
      console.log(data)
    })
  }

  onFilesAdded(e) {
    if (this.props.disabled) return
    const files = e.target.files

    this.handleFiles(files)
  }

  onDragLeave() {
    this.setState({ hightlight: false })
  }

  onDrop(e) {
    e.preventDefault()

    if (this.props.disabled) return

    const files = e.dataTransfer.files

    this.handleFiles(files)

    this.setState({ hightlight: false })
  }

  onDragOver(e) {
    e.preventDefault()

    if (this.props.disabled) return

    this.setState({ hightlight: true })
  }

  openFileDialog() {
    if (this.props.disabled) return
    this.fileInputRef.current.click()
  }

  getBase64(file, cb) {
    let reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = function() {
      cb(reader.result)
    }
    reader.onerror = function(error) {
      console.log('Error: ', error)
    }
  }

  render() {
    return (
      <div>
        <div
          className={`Upload ${this.state.hightlight ? 'Highlight' : ''}`}
          onDragOver={this.onDragOver}
          onDragLeave={this.onDragLeave}
          onDrop={this.onDrop}
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
        <div>
          <span>Result</span>
        </div>
      </div>
    )
  }
}

export default Upload
