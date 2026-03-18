// AutoShare - YouTube to Instagram & TikTok
// Configuration and API Integration

const CONFIG = {
    CREAO_ENDPOINT: 'https://api.creao.ai/v1/miniapp/wdJ9GXUpU4/run',
    DEMO_MODE: false,
};

// Form elements
const form = document.getElementById('videoForm');
const submitBtn = document.getElementById('submitBtn');
const loading = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const resultContent = document.getElementById('resultContent');
const errorDiv = document.getElementById('error');

// Form submission handler
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Reset UI
    loading.style.display = 'none';
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    submitBtn.disabled = false;
    
    // Get form values
    const videoUrl = document.getElementById('videoUrl').value.trim();
    const outputFormat = document.getElementById('outputFormat').value;
    
    // Validation
    if (!videoUrl) {
        showError('Lütfen bir YouTube video URL\'si girin.');
        return;
    }
    
    if (!outputFormat) {
        showError('Lütfen bir çıktı formatı seçin.');
        return;
    }
    
    // Validate YouTube URL
    if (!isValidYouTubeUrl(videoUrl)) {
        showError('Geçerli bir YouTube URL\'si girin. Örnek: https://www.youtube.com/watch?v=xxxxx');
        return;
    }
    
    // Show loading
    submitBtn.disabled = true;
    loading.style.display = 'block';
    
    if (DEMO_MODE) {
        // Demo mode - simulate API call
        setTimeout(() => {
            loading.style.display = 'none';
            submitBtn.disabled = false;
            showResult(`Demo Sonuç:\n\nVideo URL: ${videoUrl}\nFormat: ${outputFormat}\n\nBu bir demo yanıtıdır. Gerçek API entegrasyonu için DEMO_MODE'u false yapın.`);
        }, 2000);
    } else {
        // Real API call
        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    videoUrl: videoUrl,
                    outputFormat: outputFormat
                })
            });
            
            loading.style.display = 'none';
            submitBtn.disabled = false;
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`API Hatası (${response.status}): ${errorText}`);
            }
            
            const data = await response.json();
            
            // Display result
            if (data.result) {
                showResult(data.result);
            } else if (data.message) {
                showResult(data.message);
            } else {
                showResult(JSON.stringify(data, null, 2));
            }
            
        } catch (error) {
            loading.style.display = 'none';
            submitBtn.disabled = false;
            showError(`Hata: ${error.message}`);
            console.error('API Error:', error);
        }
    }
});

// Helper function to validate YouTube URL
function isValidYouTubeUrl(url) {
    const patterns = [
        /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=[\w-]+/,
        /^(https?:\/\/)?(www\.)?youtu\.be\/[\w-]+/,
        /^(https?:\/\/)?(www\.)?youtube\.com\/embed\/[\w-]+/
    ];
    return patterns.some(pattern => pattern.test(url));
}

// Helper function to show error
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Helper function to show result
function showResult(content) {
    resultContent.textContent = content;
    resultDiv.style.display = 'block';
}
