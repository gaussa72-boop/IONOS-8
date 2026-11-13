from flask import Flask, request, jsonify, render_template_string

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
PAGE='''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IONOS-8</title><style>body{margin:0;background:#02030a;color:#eef5ff;font:16px system-ui}main{max-width:900px;margin:auto;padding:12vh 24px;text-align:center}.orb{margin:auto;width:190px;height:190px;border-radius:50%;background:radial-gradient(circle,#fff,#75d8ff 15%,#145cff 40%,transparent 72%);box-shadow:0 0 100px #1685ff}h1{font-size:52px;letter-spacing:.1em}p{color:#9caad0}button{padding:12px 18px;border-radius:10px;border:0;font-weight:700}/* ULTIMA COMPLETE 2026 */
:root{color-scheme:dark;--u-line:rgba(255,255,255,.13);--u-glass:rgba(15,20,32,.72);--u-cyan:#7de9ef;--u-gold:#d9b66f}
html{scroll-behavior:smooth}body{overflow-x:hidden!important;background-image:radial-gradient(ellipse at 15% 0%,rgba(86,100,180,.2),transparent 40%),radial-gradient(ellipse at 90% 10%,rgba(31,180,187,.12),transparent 35%)}
header,.site-header,.announcement,.searchbar,.cart-drawer,.product-card,.modal,.panel{backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}
button,.btn,.cart-btn,a{transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease}
button:hover,.btn:hover,.cart-btn:hover{transform:translateY(-1px)}
input,textarea,select{max-width:100%;outline:none}input:focus,textarea:focus,select:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--u-cyan)!important;outline-offset:3px}
img{max-width:100%;height:auto}
@media(max-width:760px){.site-header{padding-left:14px!important;padding-right:14px!important}.nav{gap:12px}.product-grid,.products-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.hero h1,h1{overflow-wrap:anywhere}}
@media(max-width:440px){.product-grid,.products-grid{grid-template-columns:1fr!important}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation-duration:.01ms!important;transition-duration:.01ms!important}}
</style></head><body><main><div class="orb"></div><h1>IONOS-8</h1><p>Eigenständige IONOS-KI-/System-App</p><button id="statusButton" type="button" onclick="checkStatus()">SYSTEM STATUS</button><p id="statusMessage" role="status" aria-live="polite" style="min-height:1.5em;margin-top:18px;color:#9caad0">System bereit · IONOS-8 online</p></main><script>async function checkStatus(){const out=document.getElementById('statusMessage'),btn=document.getElementById('statusButton');btn.disabled=true;out.textContent='Systemstatus wird geprüft …';try{const r=await fetch('/api/health',{headers:{'Accept':'application/json'},cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);const x=await r.json();out.textContent='● System online · '+(x.app||'IONOS-8')+' · Status: '+(x.status||'OK');out.style.color='#7de3b0'}catch(e){out.textContent='Systemstatus derzeit nicht abrufbar. Bitte in wenigen Sekunden erneut versuchen.';out.style.color='#ffb4a8'}finally{btn.disabled=false}}(function(){const M=[["openai/gpt-5.6-luna","OpenAI · GPT-5.6 Luna"],["anthropic/claude-sonnet-5","Anthropic · Claude Sonnet 5"],["google/gemini-3.8-flash","Google · Gemini 3.8 Flash"],["x-ai/grok-4.7","xAI · Grok 4.7"],["deepseek/deepseek-v4.1-flash","DeepSeek · V4.1 Flash"],["z-ai/glm-5.3-flashx","Z.ai · GLM 5.3 FlashX"],["qwen/qwen3.7-plus-20260602","Qwen · Qwen3.7 Plus"],["moonshotai/kimi-k3","Moonshot · Kimi K3"],["minimax/minimax-m3","MiniMax · M3"],["mistralai/mistral-small-2603","Mistral · Small 4"]];const s=document.createElement('select');s.id='ai-model-select';s.setAttribute('aria-label','KI-Modell wählen');s.style.cssText='position:fixed;top:14px;right:14px;z-index:9999;background:#15131f;color:#fff;border:1px solid #8b5cf6;border-radius:999px;padding:7px 10px;font:inherit;max-width:230px';M.forEach(([v,t])=>{const o=document.createElement('option');o.value=v;o.textContent=t;s.appendChild(o)});const x=localStorage.getItem('ai_model');if(x&&M.some(m=>m[0]===x))s.value=x;s.onchange=()=>localStorage.setItem('ai_model',s.value);document.body.appendChild(s)})()</script></body></html>'''
@app.get('/')
def index(): return render_template_string(PAGE)
@app.get('/api/health')
def health(): return jsonify(status='ok',app='IONOS-8',mode='standalone')

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
