import {handleFile} from './fileHandler.js';
import "../css/style.css";

const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', () => {
    handleFile(fileInput.files[0]);
});
