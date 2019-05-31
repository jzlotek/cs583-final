import React from 'react'

import 'babel-polyfill'
import { toast } from 'react-toastify'

import UPLOAD_ICON from '../images/upload_icon.png'
import '../style/Upload.css'

class Upload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      results: [],
      toastId: 0,
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

  deleteZip(uuid) {
    var request = new XMLHttpRequest()
    request.open('DELETE', '/zip/' + uuid)
    request.send()
  }

  getZip(uuid, del) {
    let download = window.open('/zip/' + uuid, '_blank')

    download.onunload = () => {
      toast.update(10, {
        autoClose: 5000,
        render: 'Success, downloading now',
        type: toast.TYPE.SUCCESS,
        className: 'Upload-toast rotateY animated',
      })

      del(uuid)
    }
  }

  sendData(data, get, del) {
    toast('Loading...', {
      autoClose: false,
      className: 'Upload-toast',
      closeButton: false,
      position: toast.POSITION.BOTTOM_RIGHT,
      toastId: 10,
      type: toast.TYPE.INFO,
    })
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
            // Download results
            let response = JSON.parse(request.responseText)
            get(response.filename, del)
            break
          default:
            // Handle error
            toast('Server error, try again...', {
              autoClose: 10000,
              className: 'Upload-toast',
              closeButton: false,
              position: toast.POSITION.BOTTOM_RIGHT,
              toastId: 5,
              type: toast.TYPE.ERROR,
            })
            break
        }
      }
    }
    request.send(formData)
  }
  handleFiles(files) {
    let promises = []
    if (files.length <= 5) {
      this.sendData(files, this.getZip, this.deleteZip)
    } else {
      toast('Please upload 5 or less files at once...', {
        autoClose: 10000,
        className: 'Upload-toast',
        closeButton: false,
        position: toast.POSITION.BOTTOM_RIGHT,
        toastId: 5,
        type: toast.TYPE.ERROR,
      })
    }
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
          <span className="Upload-prompt">Upload JPGs or PNGs</span>
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
