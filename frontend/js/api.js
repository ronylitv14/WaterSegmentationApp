const segmentedImage = document.getElementById('segmented-image');
const loading = document.getElementById('loading');

const API_URL = process.env.API_URL;

export async function sendToAPI(file) {
    loading.style.display = 'block';
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            segmentedImage.src = URL.createObjectURL(blob);
        } else {
            const errorData = await response.json();
            console.error('API request failed:', errorData);
            alert('Failed to process the image. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        loading.style.display = 'none';
    }
}
