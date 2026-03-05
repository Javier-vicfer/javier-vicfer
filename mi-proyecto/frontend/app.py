import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
# ¡NUEVO! Importamos las herramientas de seguridad
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')
app.secret_key = 'clave_secreta_123'

# --- RUTAS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_FOLDER = os.path.join(BASE_DIR, 'backend')
USERS_FILE = os.path.join(BACKEND_FOLDER, 'usuarios.json')
MESSAGES_FILE = os.path.join(BACKEND_FOLDER, 'mensajes.json')

def inicializar_archivos():
    if not os.path.exists(BACKEND_FOLDER):
        os.makedirs(BACKEND_FOLDER)
    for archivo in [USERS_FILE, MESSAGES_FILE]:
        if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump([], f)

def cargar_datos(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def guardar_datos(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# --- RUTAS DE LA WEB ---

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    mensajes = cargar_datos(MESSAGES_FILE)
    return render_template('index.html', usuario=session['user'], mensajes=mensajes)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        
        if not u or not p:
            flash("Rellena todos los campos")
            return redirect(url_for('registro'))

        usuarios = cargar_datos(USERS_FILE)
        
        if any(user['username'] == u for user in usuarios):
            flash("El usuario ya existe")
            return redirect(url_for('registro'))
        
        # ¡AQUÍ ESTÁ LA MAGIA! Transformamos la contraseña en un hash ilegible
        password_hasheada = generate_password_hash(p)
        
        # Guardamos el hash, NUNCA la contraseña real
        usuarios.append({"username": u, "password": password_hasheada})
        guardar_datos(USERS_FILE, usuarios)
        flash("¡Registro con éxito! Ahora inicia sesión.")
        return redirect(url_for('login'))
        
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        usuarios = cargar_datos(USERS_FILE)
        
        # Buscamos al usuario por su nombre
        usuario_encontrado = next((user for user in usuarios if user['username'] == u), None)
        
        # ¡NUEVO! Comparamos la contraseña escrita con el hash guardado
        if usuario_encontrado and check_password_hash(usuario_encontrado['password'], p):
            session['user'] = u
            return redirect(url_for('index'))
        
        flash("Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/publicar', methods=['POST'])
def publicar():
    if 'user' in session:
        txt = request.form.get('mensaje')
        if txt:
            mensajes = cargar_datos(MESSAGES_FILE)
            mensajes.append({"usuario": session['user'], "texto": txt})
            guardar_datos(MESSAGES_FILE, mensajes)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    inicializar_archivos()
    app.run(debug=True)