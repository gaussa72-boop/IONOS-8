from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# SECURITY HARDENING
_SEC_RATE_LIMIT={}
from time import monotonic
@app.before_request
def _sec_before():
    if request.content_length and request.content_length>1048576:return jsonify(error="Request too large."),413
    if request.path.startswith("/.git/") or request.path.startswith("/.env"):return jsonify(error="Not Found."),404
    ip=request.remote_addr or "unknown";now=monotonic();b=_SEC_RATE_LIMIT.setdefault(ip,[]);b[:]=[t for t in b if now-t<60];limit=30 if request.method in {"POST","PUT","PATCH","DELETE"} else 120
    if len(b)>=limit:return jsonify(error="Too many requests. Please try again later."),429
    b.append(now)
@app.after_request
def _sec_headers(response):
    response.headers.setdefault("X-Content-Type-Options","nosniff");response.headers.setdefault("X-Frame-Options","DENY");response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin");response.headers.setdefault("Permissions-Policy","camera=(), microphone=(), geolocation=()");response.headers.setdefault("Strict-Transport-Security","max-age=31536000; includeSubDomains");response.headers.pop("Server",None);return response
PAGE='''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IONOS-8 · AI Workspace</title>
<style>
:root{color-scheme:dark;--bg:#080a12;--panel:#111522;--line:rgba(255,255,255,.1);--cyan:#80e8ef;--muted:#9aa5bb}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% -15%,#1b2850 0,transparent 55%),var(--bg);color:#eef3ff;font:15px system-ui,-apple-system,sans-serif}
header{height:68px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 22px;background:rgba(8,10,18,.8);backdrop-filter:blur(16px)}
.brand{display:flex;gap:12px;align-items:center;font-weight:750;letter-spacing:.08em}.orb{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle,#fff,#80e8ef 22%,#3158db 65%,transparent 72%);box-shadow:0 0 24px #3158db}
.status{font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:7px 12px}
main{max-width:920px;margin:0 auto;padding:34px 18px 28px;min-height:calc(100vh - 68px);display:flex;flex-direction:column}
h1{font-size:clamp(26px,5vw,42px);margin:12px 0 6px}.sub{color:var(--muted);margin:0 0 24px}
#messages{flex:1;min-height:260px;max-height:62vh;overflow:auto;display:flex;flex-direction:column;gap:14px;padding:16px 0}
.msg{max-width:88%;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55;padding:13px 16px;border:1px solid var(--line);border-radius:16px;background:var(--panel)}
.msg.user{align-self:flex-end;background:#182441;border-color:#2d416e}.msg.assistant{align-self:flex-start}
.composer{border:1px solid var(--line);border-radius:18px;background:rgba(17,21,34,.92);padding:12px;display:flex;gap:10px;align-items:flex-end;box-shadow:0 18px 60px #0006}
textarea{flex:1;resize:vertical;min-height:54px;max-height:180px;background:transparent;color:#fff;border:0;outline:0;font:inherit;padding:10px}
button{border:0;border-radius:12px;padding:12px 18px;background:linear-gradient(135deg,#5d7be7,#2aa8b7);color:#06101c;font-weight:750;cursor:pointer}button:disabled{opacity:.55;cursor:wait}
.note{font-size:12px;color:var(--muted);margin:10px 4px}.model{color:var(--cyan);font-size:12px}
@media(max-width:600px){header{padding:0 14px}main{padding:22px 12px}.msg{max-width:96%}.composer{gap:5px;padding:8px}button{padding:11px 13px}}
</style></head>
<body><header><div class="brand"><span class="orb"></span><span>IONOS-8</span><span class="model">AI WORKSPACE</span></div><div id="status" class="status">System wird geprüft …</div></header>
<main><h1>Womit kann ich helfen?</h1><p class="sub">Dein KI-Arbeitsbereich für Fragen, Analyse und Programmierung.</p>
<div id="messages" aria-live="polite"><div class="msg assistant">Hallo! Ich bin dein IONOS-8-Assistent. Schreib mir, woran wir arbeiten sollen.</div></div>
<form id="chatForm" class="composer"><textarea id="message" placeholder="Nachricht an IONOS-8 …" required></textarea><button id="send" type="submit">Senden</button></form>
<p class="note">Die KI benötigt einen gültigen OPENAI_API_KEY in den Render Environment Variables. API-Schlüssel werden nicht im Browser gespeichert.</p></main>
<script>
const messages=document.getElementById('messages'),statusEl=document.getElementById('status'),form=document.getElementById('chatForm'),input=document.getElementById('message'),send=document.getElementById('send');
function addMessage(role,text){const node=document.createElement('div');node.className='msg '+role;node.textContent=text;messages.appendChild(node);messages.scrollTop=messages.scrollHeight}
async function checkStatus(){try{const r=await fetch('/api/health',{cache:'no-store'});const x=await r.json();statusEl.textContent=x.ai_configured?'● KI verbunden · '+x.model:'○ API-Key fehlt';statusEl.style.color=x.ai_configured?'#8de5b1':'#f2c27a'}catch(e){statusEl.textContent='Status nicht verfügbar'}}
form.addEventListener('submit',async e=>{e.preventDefault();const message=input.value.trim();if(!message)return;addMessage('user',message);input.value='';send.disabled=true;send.textContent='…';try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});const data=await r.json();if(!r.ok)throw new Error(data.error||('HTTP '+r.status));addMessage('assistant',data.reply||'Keine Antwort erhalten.')}catch(err){addMessage('assistant','Fehler: '+err.message)}finally{send.disabled=false;send.textContent='Senden';input.focus()}});
input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.requestSubmit()}});
checkStatus();
</script><script src="https://ultima-membership-api.onrender.com/support-widget.js" defer></script></body></html>'''
@app.get('/')
def index(): return render_template_string(PAGE)
@app.get('/api/health')
def health(): return jsonify(status='ok',app='IONOS-8',mode='openai-chat',ai_configured=bool(os.getenv('OPENAI_API_KEY','').strip()),model=os.getenv('OPENAI_MODEL','gpt-4o-mini'))

@app.post('/api/chat')
def ai_chat():
    data=request.get_json(silent=True) or {}
    message=str(data.get('message') or '').strip()
    if not message:return jsonify(error='Bitte gib eine Nachricht ein.'),400
    if len(message)>12000:return jsonify(error='Nachricht ist zu lang (max. 12.000 Zeichen).'),413
    api_key=os.getenv('OPENAI_API_KEY','').strip()
    if not api_key:return jsonify(error='OPENAI_API_KEY fehlt in den Render Environment Variables.'),503
    model=os.getenv('OPENAI_MODEL','gpt-4o-mini').strip()
    try:
        response=requests.post('https://api.openai.com/v1/responses',
            headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'},
            json={'model':model,'instructions':'Du bist IONOS-8, ein hilfreicher deutschsprachiger KI-Assistent für Analyse, Recherche, Programmierung und Projektarbeit. Antworte klar und erfinde keine Fakten oder ausgeführten Aktionen.','input':message},
            timeout=60)
        if not response.ok:
            app.logger.warning('OpenAI returned HTTP %s: %s',response.status_code,response.text[:500])
            return jsonify(error='OpenAI-Anfrage fehlgeschlagen. Prüfe API-Key, Modellfreigabe und Guthaben.'),502
        payload=response.json()
        answer=payload.get('output_text')
        if not answer:
            parts=[]
            for item in payload.get('output',[]):
                for block in item.get('content',[]):
                    if block.get('type')=='output_text' and block.get('text'):parts.append(block['text'])
            answer='\\n'.join(parts)
        if not answer:return jsonify(error='Das KI-Modell hat keine Textantwort zurückgegeben.'),502
        return jsonify(ok=True,reply=answer,model=model),200
    except requests.RequestException:
        app.logger.exception('IONOS-8 OpenAI request failed')
        return jsonify(error='OpenAI ist momentan nicht erreichbar.'),502

@app.get('/favicon.ico')
def favicon():
    return '', 204

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify(status='error', message='Dieser API-Endpunkt ist nicht eingerichtet.'), 404
    return render_template_string(PAGE), 200

@app.errorhandler(500)
def internal_error(error):
    app.logger.exception('Unhandled IONOS-8 server error')
    if request.path.startswith('/api/'):
        return jsonify(status='error', message='Interner Fehler. Bitte später erneut versuchen.'), 500
    return render_template_string(PAGE), 200
if __name__=='__main__': app.run(host='127.0.0.1',port=5008,debug=False)
