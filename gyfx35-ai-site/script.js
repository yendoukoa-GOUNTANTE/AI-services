// script.js - GYFX35 AI Site Interaction

document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const apiQuery = document.getElementById('api-query');
    const apiResult = document.getElementById('api-result');

    if (sendBtn) {
        sendBtn.addEventListener('click', () => {
            const query = apiQuery.value.trim();

            if (!query) {
                apiResult.innerHTML = '<p style="color: #ef4444;">Veuillez entrer une requête.</p>';
                return;
            }

            // Simulate API Loading
            apiResult.innerHTML = '<p class="loading">Exécution de Flash API en cours...</p>';
            sendBtn.disabled = true;

            setTimeout(() => {
                // Mock Response
                const mockResponse = {
                    status: "success",
                    timestamp: new Date().toISOString(),
                    model: "Flash-API-v1",
                    result: `Analyse terminée pour : "${query}"\n\n[FLASH-API] : Nous avons détecté plusieurs opportunités d'optimisation IA pour votre projet. Notre agent d'ingénierie logicielle peut commencer l'implémentation immédiatement.`
                };

                // Security: Create pre element and set textContent to avoid XSS
                apiResult.innerHTML = '<p style="color: #10b981; margin-bottom: 0.5rem;">> Request successful</p>';
                const pre = document.createElement('pre');
                pre.style.whiteSpace = 'pre-wrap';
                pre.textContent = JSON.stringify(mockResponse, null, 2);
                apiResult.appendChild(pre);

                sendBtn.disabled = false;
            }, 1500);
        });
    }

    // Mobile Menu Toggle (Simple placeholder)
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.addEventListener('click', () => {
            alert('Menu mobile bientôt disponible !');
        });
    }
});
