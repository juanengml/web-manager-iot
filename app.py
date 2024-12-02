from flask import Flask, jsonify, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Chave para gerenciar sessões

# Simulação de banco de dados
users = [{"id": 1, "username": "admin", "password": "admin"}]  # Usuário administrador pré-criado
endpoints = []  # Lista para armazenar endpoints

# Função para verificar se o usuário está logado
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Página inicial (redireciona para login se não autenticado)
@app.route('/')
@login_required
def index():
    return redirect(url_for('crud_endpoints'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('crud_endpoints'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Gestão de usuários
@app.route('/crud_usuarios', methods=['GET', 'POST'])
@login_required
def crud_usuarios():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if any(u['username'] == username for u in users):
            return render_template('crud_usuarios.html', users=users, error="User already exists")
        new_user = {"id": len(users) + 1, "username": username, "password": password}
        users.append(new_user)
    return render_template('crud_usuarios.html', users=users)

# CRUD de endpoints
@app.route('/crud_endpoints', methods=['GET', 'POST'])
@login_required
def crud_endpoints():
    if request.method == 'POST':
        name = request.form['name']
        link = request.form['link']
        if any(e['name'] == name for e in endpoints):
            return render_template('crud_endpoints.html', endpoints=endpoints, error="Endpoint already exists")
        new_endpoint = {"id": len(endpoints) + 1, "name": name, "link": link, "status": "off"}
        endpoints.append(new_endpoint)
    return render_template('crud_endpoints.html', endpoints=endpoints)

@app.route('/delete_endpoint/<int:endpoint_id>')
@login_required
def delete_endpoint(endpoint_id):
    global endpoints
    endpoints = [e for e in endpoints if e['id'] != endpoint_id]
    return redirect(url_for('crud_endpoints'))

@app.route('/toggle_endpoint/<int:endpoint_id>')
@login_required
def toggle_endpoint(endpoint_id):
    for endpoint in endpoints:
        if endpoint['id'] == endpoint_id:
            endpoint['status'] = "on" if endpoint['status'] == "off" else "off"
            break
    return redirect(url_for('crud_endpoints'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
