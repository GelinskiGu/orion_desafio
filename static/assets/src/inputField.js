function handleFileChange(event) {
    const fileInput = event.target;
    const fileNameElement = document.getElementById('selected-file-name');
    fileNameElement.textContent = fileInput.files[0]?.name || '';
};