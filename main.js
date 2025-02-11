document.addEventListener('DOMContentLoaded', function() {
    const urlForm = document.getElementById('urlForm');
    const resultDiv = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrl');
    const copyButton = document.getElementById('copyButton');
    const visitCountSpan = document.getElementById('visitCount');

    urlForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(urlForm);
        
        try {
            const response = await fetch('/shorten', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                shortUrlInput.value = data.short_url;
                visitCountSpan.textContent = data.visits;
                resultDiv.classList.remove('d-none');
            } else {
                alert(data.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while shortening the URL');
        }
    });

    copyButton.addEventListener('click', function() {
        shortUrlInput.select();
        document.execCommand('copy');
        
        // Change button text temporarily
        const originalText = copyButton.innerHTML;
        copyButton.innerHTML = '<i class="bi bi-check"></i> Copied!';
        setTimeout(() => {
            copyButton.innerHTML = originalText;
        }, 2000);
    });
});
