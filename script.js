function createStars() {
    const container = document.getElementById('stars-container');
    for (let i = 0; i < 120; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDelay = Math.random() * 5 + 's';
        star.style.animationDuration = 5 + Math.random() * 10 + 's';
        container.appendChild(star);
    }
}
document.addEventListener('DOMContentLoaded', createStars);

document.getElementById('interpret-btn').addEventListener('click', async () => {
    const dream = document.getElementById('dream-input').value;
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    if (!dream.trim()) {
        errorDiv.textContent = "❌ Veuillez décrire votre rêve.";
        resultDiv.innerHTML = "";
        return;
    }

    errorDiv.textContent = "";
    loadingDiv.style.display = "block";
    resultDiv.innerHTML = "";

    try {
        const response = await fetch('/interpret', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dream })
        });

        const data = await response.json();

        if (response.ok) {
            loadingDiv.style.display = "none";
            resultDiv.innerHTML = data.interpretation
                .replace(/\n/g, '<br>')
                .replace(/### (.*?)(?=<br>|$)/g, '<h4>$1</h4>');
        } else {
            loadingDiv.style.display = "none";
            errorDiv.textContent = "⚠️ " + data.error;
        }
    } catch (err) {
        loadingDiv.style.display = "none";
        errorDiv.textContent = "⚠️ Erreur de connexion. Veuillez réessayer.";
    }
});