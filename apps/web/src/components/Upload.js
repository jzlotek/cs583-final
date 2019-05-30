import React from 'react'
import '../style/Upload.css'
import 'babel-polyfill'

import UPLOAD_ICON from '../images/upload_icon.png'

class Upload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      results: [],
    }

    // Refs
    this.fileInputRef = React.createRef()

    // Bindings
    this.openFileDialog = this.openFileDialog.bind(this)
    this.onFilesAdded = this.onFilesAdded.bind(this)
    this.onDragOver = this.onDragOver.bind(this)
    this.onDragLeave = this.onDragLeave.bind(this)
    this.onDrop = this.onDrop.bind(this)
    this.handleFiles = this.handleFiles.bind(this)
    this.getBase64 = this.getBase64.bind(this)
    this.renderResult = this.renderResult.bind(this)
    this.sendData = this.sendData.bind(this)
  }

  sendData(data) {
    let formData = new FormData()
    let blob

    for (let f of data) {
      blob = new Blob([f], { type: f.type })
      formData.append(f.name, blob, f.name)
    }

    var request = new XMLHttpRequest()
    request.open('POST', '/photo')
    request.onreadystatechange = function() {
      console.log(request)
      if (request.readyState === 4) {
        switch (request.status) {
          case 200:
            console.log("success")
            // Display/Download results
            break
          default:
            // Handle error
            break
        }
      }
    }
  }

  handleFiles(files) {
    let promises = []

    this.sendData(files).then(res => console.log(res))

    //    for (let i = 0; i < files.length; i++) {
    //      promises.push(
    //        new Promise((res) => {
    //          this.getBase64(files[i], (result) => {
    //            res(result)
    //          })
    //        }),
    //      )
    //    }
    //
    //    Promise.all(promises).then((data) => {
    //      console.log(data)
    //      this.sendData(data)
    //    })
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

  renderResult(img) {
    return <img src={img} className="Result" />
  }

  render() {
    return (
      <div className="Upload-wrapper">
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
          <span className="Upload-prompt">Upload File(s)</span>
          <img className="Upload-icon" src={UPLOAD_ICON} />
        </div>
        <div className="Results">
          <span>{this.state.results[0] !== undefined ? 'Result(s)' : ''}</span>
          <div>
            {this.state.results.map((result) => this.renderResult(result))}
          </div>
        </div>
      </div>
    )
  }
}

export default Upload
