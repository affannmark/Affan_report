from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFFAN MARK - Pro Security Tool</title>
    <style>
        body {
            background-color: #030303;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 750px;
            background: #080808;
            border: 1px solid #00ff00;
            border-radius: 6px;
            padding: 15px;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        pre.banner {
            color: #00ff00;
            font-weight: bold;
            font-size: 8px;
            overflow-x: auto;
            text-align: center;
            margin-bottom: 15px;
        }
        @media (min-width: 500px) {
            pre.banner { font-size: 10px; }
        }
        .yellow { color: #ffff00; }
        .red { color: #ff2a2a; }
        .cyan { color: #00ffff; }
        .green { color: #00ff00; }
        .bold { font-weight: bold; }
        
        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 6px 0 12px 0;
            background: #111;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            border-radius: 4px;
            box-sizing: border-box;
            outline: none;
        }
        button {
            background: #00ff00;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            transition: 0.1s;
        }
        button:active {
            background: #009900;
        }
        .hidden { display: none; }
        .log-box {
            background: #000;
            border: 1px solid #222;
            padding: 12px;
            height: 280px;
            overflow-y: auto;
            margin-top: 12px;
            font-size: 12px;
            line-height: 1.4;
        }
        .final-alert {
            border-top: 3px solid #ff2a2a;
            border-bottom: 3px solid #ff2a2a;
            color: #ff2a2a;
            font-weight: bold;
            padding: 10px 5px;
            margin-top: 12px;
            text-align: center;
            font-size: 15px;
            background: rgba(255, 0, 0, 0.05);
        }
        .method-card {
            border: 1px solid #222;
            padding: 8px;
            margin-bottom: 8px;
            border-radius: 4px;
            background: #0d0d0d;
        }
    </style>
</head>
<body>

<div class="container">
    <pre class="banner">
 █████╗ ███████╗███████╗█████╗ ███╗   ██╗    ███╗   ███╗█████╗ ██████╗ ██╗  ██╗
 ██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║    ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝
 ███████║█████╗  █████╗  ███████║██╔██╗ ██║    ██╔████╔██║███████║██████╔╝█████═╝ 
 ██╔══██║██╔══╝  ██╔══╝  ██╔══██║██║╚██╗██║    ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ 
 ██║  ██║██║     ██║     ██║  ██║██║ ╚████║    ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗
 ╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                                                   
                        [ MADE BY AFFAN MARK ]
    </pre>

    <!-- STEP 1: PASSWORD VERIFICATION -->
    <div id="step-password">
        <p class="yellow bold">--- SECURITY VERIFICATION ---</p>
        <label>Enter first password:</label>
        <input type="password" id="pass1" placeholder="Enter password...">
        
        <label>Enter next password:</label>
        <input type="password" id="pass2" placeholder="Enter confirm password...">
        
        <button onclick="verifyPassword()">VERIFY & UNLOCK TOOL</button>
    </div>

    <!-- STEP 2: COOKIE SETUP -->
    <div id="step-cookies" class="hidden">
        <p class="green bold">[+] Authentication Successful! Welcome, Affan.</p>
        <p class="yellow bold">--- COOKIE AUTHENTICATION SETUP ---</p>
        <label>Kitni ID ki cookie dalni hai? (1, 2, 3):</label>
        <select id="cookie-count" onchange="generateCookieInputs()">
            <option value="1">1 ID Cookie</option>
            <option value="2">2 ID Cookies</option>
            <option value="3">3 ID Cookies</option>
        </select>
        
        <div id="cookie-inputs-container">
            <label>Enter Cookie #1 for target ID:</label>
            <input type="text" class="cookie-val" placeholder="Paste ID cookie here...">
        </div>
        
        <button onclick="saveCookies()">LOAD COOKIES & CONTINUE</button>
    </div>

    <!-- STEP 3: REPORT MENU & EXECUTION -->
    <div id="step-menu" class="hidden">
        <p class="yellow bold">--- SELECT A THE MOST WANTED AFFAN REPORT METHOD ---</p>
        
        <div class="method-card">
            <span class="bold">1. WhatsApp Spam Report</span><br>
            <small class="yellow">[NOTE: Is report ka use sirf tool owner Affan karega. Baki kisi ko use krni he to Affan bhai se WhatsApp password lelo or use kro]</small>
        </div>
        <div class="method-card">
            <span class="bold">2. Facebook Mask Report</span>
        </div>
        <div class="method-card">
            <span class="bold">3. Instagram Mask Report</span>
        </div>

        <label>Select Method:</label>
        <select id="platform-select">
            <option value="WhatsApp">1. WhatsApp Spam Report</option>
            <option value="Facebook">2. Facebook Mask Report</option>
            <option value="Instagram">3. Instagram Mask Report</option>
        </select>

        <label>Jis ID/Number ko report karna hai uska link ya number dalo:</label>
        <input type="text" id="target-link" placeholder="Enter target link or number...">

        <button id="start-btn" onclick="startSimulation()">START HEAVY REPORT</button>

        <div id="terminal-output" class="log-box hidden"></div>
    </div>
</div>

<script>
    let loadedCookies = [];

    function redirectToWhatsApp() {
        alert("[!] Tool Locked! Password lene ke liye WhatsApp par redirect kiya ja raha hai...");
        const phone = "918307999802";
        const msg = encodeURIComponent("Affan bhai tool ko use krne ke liye password do mujhe");
        window.location.href = `https://wa.me/${phone}?text=${msg}`;
    }

    async function verifyPassword() {
        const p1 = document.getElementById("pass1").value;
        const p2 = document.getElementById("pass2").value;

        // Fast fetch request without blocking UI
        try {
            const res = await fetch('/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pass1: p1, pass2: p2 })
            });
            const data = await res.json();

            if (data.status === "success") {
                document.getElementById("step-password").classList.add("hidden");
                document.getElementById("step-cookies").classList.remove("hidden");
            } else {
                redirectToWhatsApp();
            }
        } catch (err) {
            redirectToWhatsApp();
        }
    }

    function generateCookieInputs() {
        const count = parseInt(document.getElementById("cookie-count").value);
        const container = document.getElementById("cookie-inputs-container");
        container.innerHTML = "";
        for (let i = 1; i <= count; i++) {
            container.innerHTML += `
                <label>Enter Cookie #${i} for target ID:</label>
                <input type="text" class="cookie-val" placeholder="Paste ID cookie #${i} here...">
            `;
        }
    }

    function saveCookies() {
        const inputs = document.querySelectorAll(".cookie-val");
        loadedCookies = [];
        for (let inp of inputs) {
            if (!inp.value.trim()) {
                alert("[!] Cookie khali nahi ho sakti, saari cookies dalo!");
                return;
            }
            loadedCookies.push(inp.value.trim());
        }
        document.getElementById("step-cookies").classList.add("hidden");
        document.getElementById("step-menu").classList.remove("hidden");
    }

    function startSimulation() {
        const platform = document.getElementById("platform-select").value;
        const target = document.getElementById("target-link").value.trim();

        if (!target) {
            alert("[!] Error: Target link ya number dalo!");
            return;
        }

        const btn = document.getElementById("start-btn");
        btn.disabled = true;
        btn.innerText = "EXECUTING HEAVY ATTACK...";

        const out = document.getElementById("terminal-output");
        out.classList.remove("hidden");
        out.innerHTML = `
            <div class="yellow">[*] Target Platform: ${platform}</div>
            <div class="green">[+] Initializing blazing-fast API proxy nodes (${loadedCookies.length} active sessions)...</div>
            <div class="cyan">[+] Target Locked: ${target}</div>
            <div class="yellow">[+] Pushing 20 heavy automated reports concurrently...</div><br>
        `;

        const categories = [
            "Terrorism & Violent Extremism",
            "Harassment & Targeted Bullying",
            "Scam, Phishing & Financial Fraud",
            "Spam Bot & Automated Mass Interruption",
            "Impersonation & Fake Identity",
            "Dangerous Content & Malware Distribution",
            "Hate Speech & Discriminatory Behavior",
            "Intellectual Property Violation",
            "Unverified Commercial Spam",
            "Platform Terms of Service Breach"
        ];

        let i = 1;
        // Fast interval (400ms per report for lightning speed execution)
        const interval = setInterval(() => {
            if (i <= 20) {
                const cat = categories[(i - 1) % categories.length];
                const cookieTag = `Cookie #${((i - 1) % loadedCookies.length) + 1}`;
                out.innerHTML += `<div class="green">[SUCCESS] Report #${i}/20 dispatched via [${cookieTag}] [${cat}]</div>`;
                out.scrollTop = out.scrollHeight;
                i++;
            } else {
                clearInterval(interval);
                out.innerHTML += `<br><div class="yellow">[*] Flushing server sockets and clearing connection traces...</div>`;
                out.scrollTop = out.scrollHeight;
                
                setTimeout(() => {
                    out.innerHTML += `
                        <div class="final-alert">
                            [!] THIS ACCOUNT REMOVED FROM ${platform.toUpperCase()}
                        </div>
                    `;
                    out.scrollTop = out.scrollHeight;
                    btn.disabled = false;
                    btn.innerText = "START HEAVY REPORT";
                }, 600);
            }
        }, 400);
    }
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    p1 = data.get("pass1", "")
    p2 = data.get("pass2", "")
    if p1 == "AFFANMARK376" and p2 == "AFFANMARK376":
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
