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
    this.getZip = this.getZip.bind(this)
    this.deleteZip = this.deleteZip.bind(this)
  }

  deleteZip(uuid) {}

  getZip(uuid, del) {
    window.open('/zip/' + uuid, '_blank')

    //    var request = new XMLHttpRequest()
    //    request.open('GET', '/zip/' + uuid)
    //    request.onreadystatechange = function() {
    //      if (request.readyState === 4) {
    //        switch (request.status) {
    //          case 200:
    //            console.log('success')
    //            // Delete from server
    //            break
    //          default:
    //            console.log('fail')
    //            // Handle error
    //            break
    //        }
    //      }
    //    }
    //    request.send()
  }

  sendData(data, get, del) {
    let formData = new FormData()
    let blob

    for (let f of data) {
      blob = new Blob([f], { type: f.type })
      formData.append(f.name, blob, f.name)
    }

    var request = new XMLHttpRequest()
    request.open('POST', '/photo')
    request.onreadystatechange = function() {
      if (request.readyState === 4) {
        switch (request.status) {
          case 200:
            let response = JSON.parse(request.responseText)
            console.log(response.filename)
            get(response.filename, del)
            // Display/Download results
            break
          default:
            console.log('fail')
            // Handle error
            break
        }
      }
    }
    request.send(formData)
  }

  handleFiles(files) {
    let promises = []

    this.sendData(files, this.getZip, this.deleteZip)
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
