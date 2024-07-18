import { sendToAPI } from './api.js';

const originalImage = document.getElementById('original-image');

export function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
            sendToAPI(file);
        };
        reader.readAsDataURL(file);
    }
}
