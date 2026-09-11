from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
PAGE='''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IONOS-8</title><style>body{margin:0;background:#02030a;color:#eef5ff;font:16px system-ui}main{max-width:900px;margin:auto;padding:12vh 24px;text-align:center}.orb{margin:auto;width:190px;height:190px;border-radius:50%;background:radial-gradient(circle,#fff,#75d8ff 15%,#145cff 40%,transparent 72%);box-shadow:0 0 100px #1685ff}h1{font-size:52px;letter-spacing:.1em}p{color:#9caad0}button{padding:12px 18px;border-radius:10px;border:0;font-weight:700}</style></head><body><main><div class="orb"></div><h1>IONOS-8</h1><p>Eigenständige IONOS-KI-/System-App</p><button onclick="fetch('/api/health').then(r=>r.json()).then(x=>alert(JSON.stringify(x)))">SYSTEM STATUS</button></main></body></html>'''
@app.get('/')
def index(): return render_template_string(PAGE)
@app.get('/api/health')
def health(): return jsonify(status='ok',app='IONOS-8',mode='standalone')
if __name__=='__main__': app.run(host='127.0.0.1',port=5008,debug=False)
