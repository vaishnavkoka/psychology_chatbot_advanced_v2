# Image Mutation Tool - Frontend Implementation Guide

## 🎨 React Component Architecture

```
App
├── Layout (Header, Navigation, Footer)
├── Pages
│   ├── HomePage
│   ├── MutationPage
│   │   ├── ImageUpload
│   │   ├── MutationSelector
│   │   │   ├── MutationTabs (Continuous/Discrete)
│   │   │   ├── ParameterControls
│   │   │   │   ├── SliderControl (for continuous)
│   │   │   │   └── SelectControl (for discrete)
│   │   │   └── MutationPresets
│   │   ├── PreviewWindow
│   │   │   ├── BeforeAfterSlider
│   │   │   └── ImageComparison
│   │   └── ResultsPanel
│   │       ├── DownloadManager
│   │       ├── ManifestViewer
│   │       └── StatisticsCard
│   ├── BatchPage
│   └── DocumentationPage
├── Services
│   ├── api.js (API calls)
│   ├── mutationService.js
│   └── storageService.js
└── Hooks
    ├── useImageUpload.js
    ├── useMutation.js
    └── usePreview.js
```

---

## 📦 Component Examples

### **1. Main App Component** (`App.jsx`)

```jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Pages
import HomePage from './pages/HomePage';
import MutationPage from './pages/MutationPage';
import BatchPage from './pages/BatchPage';
import DocumentationPage from './pages/DocumentationPage';

// Layout
import Header from './components/Header';
import Navigation from './components/Navigation';
import Footer from './components/Footer';

function App() {
  const [jobId, setJobId] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  return (
    <Router>
      <div className="app">
        <Header />
        <Navigation />
        
        <main className="main-content">
          <Routes>
            <Route 
              path="/" 
              element={<HomePage />} 
            />
            <Route 
              path="/mutate" 
              element={
                <MutationPage 
                  jobId={jobId}
                  setJobId={setJobId}
                  uploadedFiles={uploadedFiles}
                  setUploadedFiles={setUploadedFiles}
                />
              } 
            />
            <Route 
              path="/batch" 
              element={<BatchPage />} 
            />
            <Route 
              path="/docs" 
              element={<DocumentationPage />} 
            />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
```

### **2. Image Upload Component** (`components/ImageUpload.jsx`)

```jsx
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadImages } from '../services/api';
import './ImageUpload.css';

const ImageUpload = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles) => {
    setUploading(true);
    setUploadError(null);
    
    try {
      // Create FormData for multipart upload
      const formData = new FormData();
      acceptedFiles.forEach((file) => {
        formData.append('files', file);
      });

      // Upload files
      const response = await uploadImages(formData, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setUploadProgress(percentCompleted);
      });

      onUploadSuccess(response.data);
      setUploadProgress(0);
    } catch (error) {
      setUploadError(error.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.tiff', '.bmp', '.webp']
    },
    multiple: true,
    disabled: uploading
  });

  return (
    <div className="image-upload">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <div className="upload-progress">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <p>Uploading... {uploadProgress}%</p>
          </div>
        ) : (
          <div className="upload-content">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <h3>Drag images here or click to select</h3>
            <p>Supported: JPG, PNG, GIF, TIFF, BMP, WebP</p>
            <p className="file-size">Max 50MB per image</p>
          </div>
        )}
      </div>

      {uploadError && (
        <div className="error-message">
          <span>❌ {uploadError}</span>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
```

### **3. Mutation Selector Component** (`components/MutationSelector.jsx`)

```jsx
import React, { useState, useEffect } from 'react';
import { fetchMutations } from '../services/api';
import ParameterControls from './ParameterControls';
import MutationPresets from './MutationPresets';
import './MutationSelector.css';

const MutationSelector = ({ onMutationSelect, imageFiles }) => {
  const [mutations, setMutations] = useState({});
  const [selectedTab, setSelectedTab] = useState('continuous'); // continuous/discrete
  const [selectedMutation, setSelectedMutation] = useState(null);
  const [parameters, setParameters] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch mutations on mount
  useEffect(() => {
    const loadMutations = async () => {
      try {
        const response = await fetchMutations();
        setMutations(response.data);
        // Auto-select first continuous mutation
        const continuous = response.data.continuous;
        if (continuous && Object.keys(continuous).length > 0) {
          const firstMutation = Object.keys(continuous)[0];
          setSelectedMutation(firstMutation);
          initializeParameters(continuous[firstMutation]);
        }
      } catch (err) {
        setError('Failed to load mutations');
      } finally {
        setLoading(false);
      }
    };

    loadMutations();
  }, []);

  const initializeParameters = (mutation) => {
    const params = {};
    mutation.parameters.forEach((param) => {
      params[param.name] = param.default_value;
    });
    setParameters(params);
  };

  const handleMutationChange = (mutationName) => {
    setSelectedMutation(mutationName);
    const mutation = mutations[selectedTab][mutationName];
    initializeParameters(mutation);
  };

  const handleParameterChange = (paramName, value) => {
    setParameters({
      ...parameters,
      [paramName]: value
    });
  };

  const handleApply = () => {
    if (!selectedMutation) return;

    onMutationSelect({
      mutation: selectedMutation,
      parameters: parameters,
      tab: selectedTab
    });
  };

  if (loading) return <div className="loading">Loading mutations...</div>;
  if (error) return <div className="error">{error}</div>;

  const availableMutations = mutations[selectedTab] || {};
  const currentMutation = selectedMutation ? availableMutations[selectedMutation] : null;

  return (
    <div className="mutation-selector">
      <div className="tabs">
        <button 
          className={`tab ${selectedTab === 'continuous' ? 'active' : ''}`}
          onClick={() => {
            setSelectedTab('continuous');
            handleMutationChange(Object.keys(mutations.continuous)[0]);
          }}
        >
          📊 Continuous Mutations
        </button>
        <button 
          className={`tab ${selectedTab === 'discrete' ? 'active' : ''}`}
          onClick={() => {
            setSelectedTab('discrete');
            handleMutationChange(Object.keys(mutations.discrete)[0]);
          }}
        >
          🎯 Discrete Mutations
        </button>
      </div>

      <div className="mutation-list">
        <label>Select Mutation:</label>
        <select 
          value={selectedMutation || ''} 
          onChange={(e) => handleMutationChange(e.target.value)}
        >
          {Object.entries(availableMutations).map(([name, mutation]) => (
            <option key={name} value={name}>
              {name.charAt(0).toUpperCase() + name.slice(1)} - {mutation.description}
            </option>
          ))}
        </select>
      </div>

      {currentMutation && (
        <>
          <div className="mutation-description">
            <p>{currentMutation.description}</p>
          </div>

          <ParameterControls 
            parameters={currentMutation.parameters}
            values={parameters}
            onChange={handleParameterChange}
          />

          <MutationPresets 
            mutation={selectedMutation}
            onPresetSelect={(preset) => setParameters(preset)}
          />

          <button 
            className="apply-mutation-btn"
            onClick={handleApply}
            disabled={!imageFiles || imageFiles.length === 0}
          >
            Apply Mutation
          </button>
        </>
      )}
    </div>
  );
};

export default MutationSelector;
```

### **4. Parameter Controls Component** (`components/ParameterControls.jsx`)

```jsx
import React from 'react';
import './ParameterControls.css';

const ParameterControls = ({ parameters, values, onChange }) => {
  return (
    <div className="parameter-controls">
      <h3>Parameters</h3>
      
      {parameters.map((param) => (
        <div key={param.name} className="control-group">
          <label htmlFor={param.name}>
            {param.name.charAt(0).toUpperCase() + param.name.slice(1)}
            {param.description && <span className="description-tooltip">?</span>}
          </label>
          
          {param.type === 'float' || param.type === 'int' ? (
            // Slider for continuous values
            <div className="slider-control">
              <input
                id={param.name}
                type="range"
                min={param.min}
                max={param.max}
                step={param.type === 'float' ? 0.1 : 1}
                value={values[param.name] || param.default_value}
                onChange={(e) => {
                  const value = param.type === 'float' 
                    ? parseFloat(e.target.value)
                    : parseInt(e.target.value);
                  onChange(param.name, value);
                }}
              />
              <div className="slider-display">
                <span className="value">{values[param.name] || param.default_value}</span>
                <span className="range">
                  [{param.min} - {param.max}]
                </span>
              </div>
            </div>
          ) : param.type === 'choice' ? (
            // Dropdown for choices
            <select
              id={param.name}
              value={values[param.name] || param.default_value}
              onChange={(e) => {
                const value = isNaN(e.target.value) 
                  ? e.target.value 
                  : parseInt(e.target.value);
                onChange(param.name, value);
              }}
            >
              {param.choices.map((choice) => (
                <option key={choice} value={choice}>
                  {choice}
                </option>
              ))}
            </select>
          ) : param.type === 'bool' ? (
            // Toggle for boolean
            <input
              id={param.name}
              type="checkbox"
              checked={values[param.name] || param.default_value}
              onChange={(e) => onChange(param.name, e.target.checked)}
            />
          ) : null}
          
          {param.description && (
            <small className="param-description">{param.description}</small>
          )}
        </div>
      ))}
    </div>
  );
};

export default ParameterControls;
```

### **5. Before-After Slider Component** (`components/BeforeAfterSlider.jsx`)

```jsx
import React, { useState, useRef } from 'react';
import './BeforeAfterSlider.css';

const BeforeAfterSlider = ({ beforeImage, afterImage, beforeLabel = 'Original', afterLabel = 'Mutated' }) => {
  const [sliderPosition, setSliderPosition] = useState(50);
  const containerRef = useRef(null);

  const handleMouseMove = (e) => {
    if (!containerRef.current) return;
    
    const rect = containerRef.current.getBoundingClientRect();
    const newPosition = ((e.clientX - rect.left) / rect.width) * 100;
    setSliderPosition(Math.min(100, Math.max(0, newPosition)));
  };

  return (
    <div 
      className="before-after-slider"
      ref={containerRef}
      onMouseMove={handleMouseMove}
    >
      {/* Before Image */}
      <div className="before-image">
        <img src={beforeImage} alt={beforeLabel} />
        <label className="image-label before">{beforeLabel}</label>
      </div>

      {/* After Image (with clipping) */}
      <div 
        className="after-image"
        style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
      >
        <img src={afterImage} alt={afterLabel} />
        <label className="image-label after">{afterLabel}</label>
      </div>

      {/* Divider */}
      <div 
        className="divider"
        style={{ left: `${sliderPosition}%` }}
      >
        <div className="divider-handle">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 3L3 9v6l6 6h2V3H9zM15 3v18h2l6-6V9l-6-6h-2z" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default BeforeAfterSlider;
```

### **6. Results Panel Component** (`components/ResultsPanel.jsx`)

```jsx
import React, { useState } from 'react';
import { downloadFile, downloadZip } from '../services/api';
import ManifestViewer from './ManifestViewer';
import './ResultsPanel.css';

const ResultsPanel = ({ jobId, mutations, results, manifest }) => {
  const [selectedResults, setSelectedResults] = useState(new Set());
  const [downloading, setDownloading] = useState(false);

  const handleSelectResult = (filename) => {
    const newSelected = new Set(selectedResults);
    if (newSelected.has(filename)) {
      newSelected.delete(filename);
    } else {
      newSelected.add(filename);
    }
    setSelectedResults(newSelected);
  };

  const handleDownloadSelected = async () => {
    setDownloading(true);
    try {
      const filenames = Array.from(selectedResults);
      await downloadZip(jobId, filenames);
    } catch (error) {
      alert('Download failed: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  const handleDownloadAll = async () => {
    setDownloading(true);
    try {
      const filenames = results.map(r => r.output_filename);
      await downloadZip(jobId, filenames);
    } catch (error) {
      alert('Download failed: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="results-panel">
      <div className="results-header">
        <h3>🎨 Mutation Results</h3>
        <div className="results-stats">
          <span>{results.length} images mutated</span>
          <span>{selectedResults.size} selected</span>
        </div>
      </div>

      <div className="results-list">
        {results.map((result, idx) => (
          <div key={idx} className="result-item">
            <input
              type="checkbox"
              checked={selectedResults.has(result.output_filename)}
              onChange={() => handleSelectResult(result.output_filename)}
            />
            <div className="result-info">
              <p className="filename">{result.output_filename}</p>
              <p className="detail">
                {result.output_filename} 
                {result.execution_time_ms && ` • ${result.execution_time_ms}ms`}
              </p>
            </div>
            <button 
              className="download-btn"
              onClick={() => downloadFile(jobId, result.output_filename)}
              disabled={downloading}
            >
              ⬇️ Download
            </button>
          </div>
        ))}
      </div>

      <div className="results-actions">
        {selectedResults.size > 0 && (
          <button 
            className="batch-download-btn"
            onClick={handleDownloadSelected}
            disabled={downloading}
          >
            ⬇️ Download {selectedResults.size} Selected
          </button>
        )}
        <button 
          className="download-all-btn"
          onClick={handleDownloadAll}
          disabled={downloading}
        >
          ⬇️ Download All ({results.length})
        </button>
        <button className="export-manifest-btn">
          📋 Export Manifest (JSON)
        </button>
      </div>

      {manifest && <ManifestViewer manifest={manifest} />}
    </div>
  );
};

export default ResultsPanel;
```

---

## 🎯 CSS Styling Example (`ImageUpload.css`)

```css
.image-upload {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.dropzone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #fafafa;
}

.dropzone.active {
  border-color: #2563eb;
  background-color: #eff6ff;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.dropzone.uploading {
  opacity: 0.7;
  cursor: not-allowed;
}

.upload-content {
  color: #666;
}

.upload-content svg {
  margin-bottom: 16px;
  color: #2563eb;
}

.upload-content h3 {
  margin: 8px 0;
  color: #333;
  font-size: 16px;
}

.upload-content p {
  margin: 4px 0;
  font-size: 14px;
  color: #666;
}

.upload-content .file-size {
  font-size: 12px;
  color: #999;
}

.upload-progress {
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
  background-size: 200% 100%;
  animation: progress-animation 1s ease-in-out;
}

@keyframes progress-animation {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: 0 0;
  }
}

.error-message {
  margin-top: 16px;
  padding: 12px;
  background-color: #fee2e2;
  border-left: 4px solid #dc2626;
  border-radius: 4px;
  color: #991b1b;
  font-size: 14px;
}
```

---

## 🔌 API Service (`services/api.js`)

```javascript
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 600000, // 10 minutes for long operations
});

// Upload images
export const uploadImages = (formData, onProgress) => {
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: onProgress,
  });
};

// Fetch available mutations
export const fetchMutations = () => {
  return api.get('/mutations');
};

// Apply mutation
export const applyMutation = (jobId, mutation, parameters, imagePaths) => {
  return api.post('/mutate', {
    job_id: jobId,
    mutation,
    parameters,
    image_paths: imagePaths,
  });
};

// Download file
export const downloadFile = async (jobId, filename) => {
  const response = await api.get(`/download/${jobId}/${filename}`, {
    responseType: 'blob',
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.parentElement.removeChild(link);
};

// Download multiple files as ZIP
export const downloadZip = async (jobId, filenames) => {
  const response = await api.post(`/download-zip/${jobId}`, {
    files: filenames,
  }, {
    responseType: 'blob',
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `mutations_${jobId}.zip`);
  document.body.appendChild(link);
  link.click();
  link.parentElement.removeChild(link);
};

export default api;
```

---

## 🚀 Installation & Running

```bash
# 1. Install dependencies
npm install

# 2. Create .env file
REACT_APP_API_URL=http://localhost:5000/api

# 3. Start development server
npm start

# 4. Build for production
npm run build
```

This frontend implementation provides a professional, user-friendly interface for the mutation tool!

