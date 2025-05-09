---
layout: default
title: Document Upload
---

<div class="upload-container">
    <h1>Document Upload</h1>
    <p>Drag and drop your documents here or click to select files</p>
    
    <div class="drop-zone" id="dropZone">
        <p>Drop files here</p>
        <input type="file" id="fileInput" multiple style="display: none;">
        <button onclick="document.getElementById('fileInput').click()">Select Files</button>
    </div>

    <div class="file-list" id="fileList"></div>
</div>

<style>
    .upload-container {
        max-width: 800px;
        margin: 0 auto;
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .drop-zone {
        border: 2px dashed #ccc;
        border-radius: 4px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        background-color: #fafafa;
        transition: all 0.3s ease;
    }
    
    .drop-zone.dragover {
        background-color: #e3f2fd;
        border-color: var(--accent-color);
    }
    
    .file-list {
        margin-top: 2rem;
    }
    
    .file-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid #eee;
    }
    
    .file-item:last-child {
        border-bottom: none;
    }
    
    .status {
        color: #666;
        font-size: 0.9em;
    }
    
    .success {
        color: #4caf50;
    }
    
    .error {
        color: #f44336;
    }
    
    button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    button:hover {
        background-color: var(--accent-hover);
    }
</style>

<script>
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('dragover');
    }

    function unhighlight(e) {
        dropZone.classList.remove('dragover');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files: files } });
    }

    function handleFiles(e) {
        const files = [...e.target.files];
        files.forEach(uploadFile);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Create file item in the list
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span>${file.name}</span>
            <span class="status">Uploading...</span>
        `;
        fileList.appendChild(fileItem);

        // Send file to server
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const status = fileItem.querySelector('.status');
            if (data.success) {
                status.textContent = 'Uploaded successfully';
                status.classList.add('success');
            } else {
                status.textContent = 'Upload failed';
                status.classList.add('error');
            }
        })
        .catch(error => {
            const status = fileItem.querySelector('.status');
            status.textContent = 'Upload failed';
            status.classList.add('error');
            console.error('Error:', error);
        });
    }
</script> 