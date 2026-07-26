import { useState } from "react";
import "../styles/upload.css";

function DocumentUpload() {

    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    return (

        <div className="page">

            <div className="left-panel">

                <h1>
                    DocIntel
                
                </h1>

                <p className="subtitle">
                    Securely upload, analyze and compare
                    document versions using AI.
                </p>

                <div className="features">

                    <div className="feature">
                        📄 PDF, DOCX & TXT Support
                    </div>

                    <div className="feature">
                        ☁ Cloud Storage Integration
                    </div>

                    <div className="feature">
                        🤖 AI Document Analysis
                    </div>

                    <div className="feature">
                        🔍 Intelligent Version Comparison
                    </div>

                </div>

            </div>

            <div className="upload-card">

                <span className="badge">
                    DOCUMENT UPLOAD
                </span>

                <h2>Upload your document</h2>

                <p className="description">
                    Select a document to begin intelligent processing.
                </p>

                <label className="upload-box">

                    <input
                        type="file"
                        onChange={handleFileChange}
                    />

                    <div className="upload-icon">
                        ⬆
                    </div>

                    <h3>
                        Drag & Drop
                    </h3>

                    <p>
                        or click to browse files
                    </p>

                </label>

                <div className="info-row">

                    <span>Supported</span>

                    <span>PDF • DOCX • TXT</span>

                </div>

                <div className="info-row">

                    <span>Maximum Size</span>

                    <span>30 MB</span>

                </div>

                <button className="upload-button">

                    Upload Document

                </button>

                <div className="status">

                    {selectedFile
                        ? selectedFile.name
                        : "No file selected"}

                </div>

            </div>

        </div>

    );

}

export default DocumentUpload;