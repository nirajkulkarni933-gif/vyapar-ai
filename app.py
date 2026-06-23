from flask import Flask, request, jsonify, render_template_string
from google import genai

from flask import Flask

app = Flask(__name__)
import os
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VyaparAI - AI Captions for Your Business</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            background: #0a0a1a;
            color: white;
            overflow-x: hidden;
        }

        /* Animated background */
        .bg-animation {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            background: radial-gradient(ellipse at 20% 50%, #1a0533 0%, transparent 60%),
                        radial-gradient(ellipse at 80% 20%, #0d2b4e 0%, transparent 60%),
                        radial-gradient(ellipse at 50% 80%, #1a1a0a 0%, transparent 60%),
                        #0a0a1a;
        }

        .floating-orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(60px);
            animation: float 8s infinite ease-in-out;
            z-index: 0;
        }
        .orb1 { width: 300px; height: 300px; background: rgba(120, 40, 255, 0.15); top: 10%; left: 10%; animation-delay: 0s; }
        .orb2 { width: 400px; height: 400px; background: rgba(0, 150, 255, 0.1); top: 50%; right: 5%; animation-delay: 3s; }
        .orb3 { width: 250px; height: 250px; background: rgba(255, 100, 50, 0.08); bottom: 10%; left: 30%; animation-delay: 6s; }

        @keyframes float {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-30px) scale(1.05); }
        }

        /* Main content */
        .container {
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        /* Logo */
        .logo {
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.4);
            margin-bottom: 40px;
        }

        /* Hero */
        .hero-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(120,40,255,0.3), rgba(0,150,255,0.3));
            border: 1px solid rgba(120,40,255,0.4);
            border-radius: 50px;
            padding: 6px 20px;
            font-size: 13px;
            color: rgba(255,255,255,0.8);
            margin-bottom: 24px;
            backdrop-filter: blur(10px);
        }

        h1 {
            font-size: clamp(36px, 6vw, 64px);
            font-weight: 800;
            line-height: 1.1;
            text-align: center;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            font-size: 18px;
            color: rgba(255,255,255,0.5);
            text-align: center;
            margin-bottom: 50px;
            font-weight: 300;
        }

        /* 3D Card */
        .card {
            width: 100%;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 40px;
            backdrop-filter: blur(20px);
            transform-style: preserve-3d;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
        }

        .card:hover {
            transform: translateY(-5px) rotateX(2deg);
            box-shadow: 0 40px 70px rgba(0,0,0,0.6), 0 0 40px rgba(120,40,255,0.1), inset 0 1px 0 rgba(255,255,255,0.15);
        }

        .input-label {
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.4);
            margin-bottom: 12px;
            display: block;
        }

        .input-wrapper {
            position: relative;
            margin-bottom: 16px;
        }

        .input-icon {
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 20px;
        }

        input[type="text"] {
            width: 100%;
            padding: 18px 18px 18px 52px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px;
            color: white;
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
            outline: none;
        }

        input[type="text"]:focus {
            border-color: rgba(120,40,255,0.6);
            background: rgba(120,40,255,0.08);
            box-shadow: 0 0 0 3px rgba(120,40,255,0.15), 0 0 20px rgba(120,40,255,0.1);
        }

        input::placeholder { color: rgba(255,255,255,0.25); }

        /* Language selector */
        .lang-row {
            display: flex;
            gap: 10px;
            margin-bottom: 24px;
        }

        .lang-btn {
            flex: 1;
            padding: 10px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            color: rgba(255,255,255,0.5);
            font-size: 13px;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .lang-btn.active, .lang-btn:hover {
            background: rgba(120,40,255,0.2);
            border-color: rgba(120,40,255,0.5);
            color: white;
        }

        /* Generate button */
        .btn-generate {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #7828ff, #3b82f6);
            border: none;
            border-radius: 14px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            letter-spacing: 0.5px;
        }

        .btn-generate::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
            transition: left 0.5s ease;
        }

        .btn-generate:hover::before { left: 100%; }

        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(120,40,255,0.4);
        }

        .btn-generate:active { transform: translateY(0px); }

        /* Output */
        .output-section {
            margin-top: 30px;
            display: none;
        }

        .output-section.visible { display: block; }

        .output-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }

        .output-title {
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.4);
        }

        .output-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 24px;
            white-space: pre-wrap;
            line-height: 1.8;
            color: rgba(255,255,255,0.85);
            font-size: 15px;
            min-height: 100px;
        }

        .copy-btn {
            margin-top: 12px;
            padding: 10px 24px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: rgba(255,255,255,0.6);
            font-size: 13px;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .copy-btn:hover {
            background: rgba(255,255,255,0.1);
            color: white;
        }

        /* Loading animation */
        .loading {
            display: flex;
            align-items: center;
            gap: 8px;
            color: rgba(255,255,255,0.5);
            font-size: 14px;
        }

        .dots span {
            display: inline-block;
            width: 6px; height: 6px;
            background: #7828ff;
            border-radius: 50%;
            animation: bounce 1.2s infinite;
        }
        .dots span:nth-child(2) { animation-delay: 0.2s; background: #5b9fff; }
        .dots span:nth-child(3) { animation-delay: 0.4s; background: #60a5fa; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1.2); opacity: 1; }
        }

        /* Stats */
        .stats {
            display: flex;
            gap: 30px;
            margin-top: 40px;
            justify-content: center;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            font-size: 12px;
            color: rgba(255,255,255,0.35);
            letter-spacing: 1px;
        }

        /* Grid particles */
        .grid-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 50px 50px;
            z-index: 0;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    <div class="grid-overlay"></div>
    <div class="floating-orb orb1"></div>
    <div class="floating-orb orb2"></div>
    <div class="floating-orb orb3"></div>

    <div class="container">
        <div class="logo">⚡ Vyapar AI</div>

        <div class="hero-badge">✨ Powered by AI</div>

        <h1>Captions that sell,<br>in your language</h1>
        <p class="subtitle">Generate powerful social media captions in Marathi, Hindi & English — instantly</p>

        <div class="card" id="mainCard">
            <label class="input-label">Your Business Name</label>
            <div class="input-wrapper">
                <span class="input-icon">🏪</span>
                <input type="text" id="business" placeholder="e.g. your store name," />
            </div>

            <label class="input-label" style="margin-top:8px;">Language</label>
            <div class="lang-row">
                <div class="lang-btn active" onclick="selectLang(this, 'Marathi, Hindi and English')">🇮🇳 All 3</div>
                <div class="lang-btn" onclick="selectLang(this, 'Marathi only')">मराठी</div>
                <div class="lang-btn" onclick="selectLang(this, 'Hindi only')">हिंदी</div>
                <div class="lang-btn" onclick="selectLang(this, 'English only')">English</div>
            </div>

            <button class="btn-generate" onclick="generate()">
                ✨ Generate Captions
            </button>

            <div class="output-section" id="outputSection">
                <div class="output-header">
                    <div class="output-title">Generated Captions</div>
                </div>
                <div class="output-box" id="output"></div>
                <button class="copy-btn" onclick="copyText()">📋 Copy All</button>
            </div>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">3</div>
                <div class="stat-label">LANGUAGES</div>
            </div>
            <div class="stat">
                <div class="stat-number">5s</div>
                <div class="stat-label">GENERATION</div>
            </div>
            <div class="stat">
                <div class="stat-number">∞</div>
                <div class="stat-label">CAPTIONS</div>
            </div>
        </div>
    </div>

    <script>
        let selectedLang = 'Marathi, Hindi and English,';

        function selectLang(el, lang) {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            el.classList.add('active');
            selectedLang = lang;
        }

        async function generate() {
            const business = document.getElementById('business').value.trim();
            if (!business) {
                document.getElementById('business').focus();
                return;
            }

            const outputSection = document.getElementById('outputSection');
            const output = document.getElementById('output');
            const btn = document.querySelector('.btn-generate');

            outputSection.classList.add('visible');
            output.innerHTML = '<div class="loading">AI is creating your captions <div class="dots"><span></span><span></span><span></span></div></div>';
            btn.disabled = true;
            btn.textContent = 'Generating...';

            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({business, lang: selectedLang})
                });
                const data = await res.json();
                output.innerText = data.captions;
            } catch(e) {
                output.innerText = 'Error generating captions. Please try again.';
            }

            btn.disabled = false;
            btn.textContent = '✨ Generate Captions';
        }

        function copyText() {
            const text = document.getElementById('output').innerText;
            navigator.clipboard.writeText(text);
            const btn = document.querySelector('.copy-btn');
            btn.textContent = '✅ Copied!';
            setTimeout(() => btn.textContent = '📋 Copy All', 2000);
        }

        // 3D card tilt effect
        const card = document.getElementById('mainCard');
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = `perspective(1000px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) translateY(-5px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });

        // Enter key support
        document.getElementById('business').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') generate();
        });
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        business = request.json.get("business")
        lang = request.json.get("lang", "Marathi, Hindi and English")
        print(f"Generating for: {business}")
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=f"Generate 3 captions for '{business}' in {lang}"
        )
        print("Success!")
        return jsonify({"captions": response.text})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"captions": str(e)})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)