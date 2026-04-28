import { UploadCloud, FileText, X } from "lucide-react";

function UploadBox({ file, setFile }) {
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const removeFile = () => {
    setFile(null);
  };

  return (
    <div className="card">
      <h2>Upload Prescription</h2>
      <p className="muted">Supports PDF, JPG, JPEG, and PNG prescriptions.</p>

      {!file ? (
        <label className="upload-box">
          <UploadCloud size={42} />
          <span>Click to upload prescription</span>
          <small>PDF, PNG, JPG, JPEG</small>
          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileChange}
            hidden
          />
        </label>
      ) : (
        <div className="selected-file">
          <div>
            <FileText size={22} />
            <span>{file.name}</span>
          </div>

          <button onClick={removeFile} className="icon-btn">
            <X size={18} />
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadBox;
