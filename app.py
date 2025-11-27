from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import pytz 
import firebase_admin
from firebase_admin import credentials, db 
import json
import base64
import os
from werkzeug.utils import secure_filename

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura'

# ----------------------------------------------------
# CONFIGURAÇÃO E CONEXÃO FIREBASE (Realtime Database)
# ----------------------------------------------------
DB_ROOT = None
CONEXAO_OK = False
try:
    cred = credentials.Certificate("ttk2k-642d6-firebase-adminsdk-fbsvc-e3c9e51e2b.json")
    FIREBASE_URL = 'https://ttk2k-642d6-default-rtdb.firebaseio.com'
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL
    })

    DB_ROOT = db.reference()
    CONEXAO_OK = True
    print("✓ Conexão Firebase estabelecida com sucesso!")

except Exception as e:
    print(f"✗ ERRO DE CONEXÃO FIREBASE: {e}")
    print("Verifique o arquivo de credenciais e a URL.")

# --- MAPAS DE DADOS ---
EMOCOES_DEFAULT = {
    'feliz': '😊',
    'triste': '😢',
    'ansioso': '😰',
    'calmo': '😌',
    'motivado': '🔥',
    'cansado': '😴',
    'frustrado': '😠',
    'grato': '🙏'
}

HABILIDADES_DEFAULT = {
    'programacao': {'nome': 'Programação', 'icone': '💻'},
    'criatividade': {'nome': 'Criatividade', 'icone': '🎨'},
    'comunicacao': {'nome': 'Comunicação', 'icone': '🗣️'},
    'lideranca': {'nome': 'Liderança', 'icone': '👑'},
    'fitness': {'nome': 'Fitness', 'icone': '💪'},
    'meditacao': {'nome': 'Meditação', 'icone': '🧘'},
    'leitura': {'nome': 'Leitura', 'icone': '📚'},
    'musica': {'nome': 'Música', 'icone': '🎵'},
    'culinaria': {'nome': 'Culinária', 'icone': '👨‍🍳'},
    'desenho': {'nome': 'Desenho', 'icone': '✏️'}
}


def get_user_list_ref(user_id):
    """Retorna referência para listas do usuário (emocoes, habilidades, config, etc)"""
    return DB_ROOT.child('listas').child(user_id)

def load_user_lists(user_id):
    """Carrega emoções e habilidades do Firebase se existirem, senão usa defaults."""
    try:
        listas_ref = get_user_list_ref(user_id)
        emocoes = listas_ref.child('emocoes').get() or EMOCOES_DEFAULT
        habilidades = listas_ref.child('habilidades').get() or HABILIDADES_DEFAULT
        return emocoes, habilidades
    except Exception:
        return EMOCOES_DEFAULT, HABILIDADES_DEFAULT

# --- DECORATORS E FUNÇÕES AUXILIARES ---

def verificar_conexao(f):
    def wrapper(*args, **kwargs):
        if not CONEXAO_OK:
            flash("Erro de conexão com o banco de dados. Tente novamente mais tarde.", 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def get_user_diario_ref(user_id):
    """Retorna a referência do diário do usuário"""
    return DB_ROOT.child('diarios').child(user_id)

def get_hoje():
    """Retorna a data de hoje no formato YYYY-MM-DD"""
    return datetime.now().strftime('%Y-%m-%d')

def formatar_data_br(data_str):
    """Converte YYYY-MM-DD para DD/MM/YYYY"""
    try:
        dt = datetime.strptime(data_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return data_str

def obter_dia_semana(data_str):
    """Retorna dia da semana em português"""
    dias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
    try:
        dt = datetime.strptime(data_str, '%Y-%m-%d')
        return dias[dt.weekday()]
    except:
        return ""

# Filtros customizados do Jinja2
app.jinja_env.filters['formatar_data_br'] = formatar_data_br
app.jinja_env.filters['obter_dia_semana'] = obter_dia_semana

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        if not CONEXAO_OK:
            flash("Erro de conexão: Não foi possível salvar o cadastro.", 'danger')
            return redirect(url_for('cadastro'))

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_confirma = request.form.get('senha_confirma', '')

        if senha != senha_confirma:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('cadastro'))

        usuarios_ref = DB_ROOT.child('usuarios')
        usuarios = usuarios_ref.order_by_child('email').equal_to(email).get()

        if usuarios:
            flash('E-mail já cadastrado.', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario = {
            'nome': nome,
            'email': email,
            'senha_hash': generate_password_hash(senha),
            'data_registro': int(datetime.now().timestamp() * 1000),
            'foto_perfil_url': f"https://placehold.co/40x40/3b82f6/ffffff?text={nome[0].upper()}"
        }

        usuarios_ref.push(novo_usuario)
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not CONEXAO_OK:
            flash("Erro de conexão: Não foi possível realizar o login.", 'danger')
            return redirect(url_for('login'))

        email = request.form['email']
        senha = request.form['senha']

        usuarios_ref = DB_ROOT.child('usuarios')
        resultado = usuarios_ref.order_by_child('email').equal_to(email).get()

        if resultado:
            user_id, user_data = list(resultado.items())[0]

            if check_password_hash(user_data['senha_hash'], senha):
                session['logged_in'] = True
                session['user_id'] = user_id
                session['user_nome'] = user_data['nome']
                session['user_foto'] = user_data.get('foto_perfil_url', 'https://placehold.co/40x40/3b82f6/ffffff?text=U')
                flash(f'Bem-vindo, {user_data["nome"]}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('E-mail ou senha inválidos.', 'danger')
        else:
            flash('E-mail ou senha inválidos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# --- ROTAS PRINCIPAIS DO DIÁRIO ---

@app.route('/')
@login_required
@verificar_conexao
def index():
    """Página inicial com últimas entradas do diário"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id)
    diario_data = diario_ref.get() or {}

    # Ordena as datas em ordem decrescente
    datas_ordenadas = sorted(diario_data.keys(), reverse=True)

    # Última entrada
    ultimo = None
    if datas_ordenadas:
        ultima_data = datas_ordenadas[0]
        ultimo = {
            'date': ultima_data,
            'data': diario_data[ultima_data]
        }

    # Últimas 8 entradas
    dias = []
    for data_str in datas_ordenadas[:8]:
        dias.append({
            'date': data_str,
            'data': diario_data[data_str]
        })

    return render_template('index.html', ultimo=ultimo, dias=dias)

@app.route('/diario/hoje')
@login_required
@verificar_conexao
def diario_hoje():
    """Abre/cria a entrada do diário de hoje"""
    hoje = get_hoje()
    return redirect(url_for('diario', dia=hoje))

@app.route('/diario/<dia>', methods=['GET', 'POST'])
@login_required
@verificar_conexao
def diario(dia):
    """Página de edição do diário"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id)

    if request.method == 'POST':
        # Recebe os dados do formulário
        data_entrada = {
            'rotina': request.form.get('rotina', ''),
            'journal': request.form.get('journal', ''),
            'emocoes': request.form.getlist('emocoes'),
            'habilidades': request.form.getlist('habilidades'),
            'checklist': [],
            'photo_url': request.form.get('photo_url', ''),
            'timestamp': int(datetime.now().timestamp() * 1000)
        }

        # Processa o checklist
        tarefas = request.form.getlist('tarefa_texto')
        for tarefa in tarefas:
            if tarefa.strip():
                data_entrada['checklist'].append({
                    'texto': tarefa,
                    'feito': False
                })

        # Salva no Firebase
        diario_ref.child(dia).set(data_entrada)
        flash('Entrada do diário salva com sucesso!', 'success')
        return redirect(url_for('diario', dia=dia))

    # GET - Carrega dados existentes
    entrada = diario_ref.child(dia).get()
    
    if entrada:
        entrada_data = entrada
    else:
        entrada_data = {
            'rotina': '',
            'journal': '',
            'emocoes': [],
            'habilidades': [],
            'checklist': [],
            'photo_url': ''
        }

    # carrega listas do usuário (emocoes e habilidades)
    emocoes, habilidades = load_user_lists(user_id)

    return render_template('diario.html',
                          dia=dia,
                          entrada=entrada_data,
                          emocoes=emocoes,
                          habilidades=habilidades)

@app.route('/diario/<dia>/checklist/toggle/<int:index>')
@login_required
@verificar_conexao
def toggle_checklist(dia, index):
    """Toggle do status de conclusão de uma tarefa"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id).child(dia)
    entrada = diario_ref.get()

    if entrada and 'checklist' in entrada:
        checklist = entrada['checklist']
        if 0 <= index < len(checklist):
            checklist[index]['feito'] = not checklist[index]['feito']
            diario_ref.update({'checklist': checklist})
            flash('Tarefa atualizada!', 'info')

    return redirect(url_for('diario', dia=dia))

@app.route('/historico')
@login_required
@verificar_conexao
def historico():
    """Página com histórico de todos os dias"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id)
    diario_data = diario_ref.get() or {}

    # Ordena por data (mais recente primeiro)
    datas_ordenadas = sorted(diario_data.keys(), reverse=True)

    historico_items = []
    for data_str in datas_ordenadas:
        historico_items.append({
            'date': data_str,
            'data': diario_data[data_str]
        })

    return render_template('historico.html', historico_items=historico_items)

@app.route('/analise')
@login_required
@verificar_conexao
def analise():
    """Página de análise com estatísticas"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id)
    diario_data = diario_ref.get() or {}

    # Carrega listas do usuário (emocoes e habilidades)
    emocoes, habilidades = load_user_lists(user_id)

    # Análise de emoções
    emocoes_count = {}
    for emocao in (emocoes.keys() if isinstance(emocoes, dict) else []):
        emocoes_count[emocao] = 0

    # Análise de habilidades
    habilidades_count = {}
    for hab_key in (habilidades.keys() if isinstance(habilidades, dict) else []):
        habilidades_count[hab_key] = 0

    total_dias = len(diario_data)
    total_tarefas = 0
    tarefas_concluidas = 0

    for data_str, entrada in diario_data.items():
        # Conta emoções
        for emocao in entrada.get('emocoes', []):
            if emocao in emocoes_count:
                emocoes_count[emocao] += 1

        # Conta habilidades
        for hab in entrada.get('habilidades', []):
            if hab in habilidades_count:
                habilidades_count[hab] += 1

        # Conta checklist
        for item in entrada.get('checklist', []):
            total_tarefas += 1
            if item.get('feito'):
                tarefas_concluidas += 1

    # Filtra emoções e habilidades com contagem > 0
    emocoes_count = {k: v for k, v in emocoes_count.items() if v > 0}
    habilidades_count = {k: v for k, v in habilidades_count.items() if v > 0}

    taxa_conclusao = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0

    return render_template('analise.html',
                          total_dias=total_dias,
                          total_tarefas=total_tarefas,
                          tarefas_concluidas=tarefas_concluidas,
                          taxa_conclusao=taxa_conclusao,
                          emocoes_count=emocoes_count,
                          habilidades_count=habilidades_count,
                          emocoes=emocoes,
                          habilidades=habilidades)


# --- API: CRUD para Emoções e Habilidades (por usuário) ---
@app.route('/api/listas', methods=['GET'])
@login_required
@verificar_conexao
def api_listas_get():
    user_id = session['user_id']
    emocoes, habilidades = load_user_lists(user_id)
    return jsonify({'emocoes': emocoes, 'habilidades': habilidades})


@app.route('/api/emocoes', methods=['POST'])
@login_required
@verificar_conexao
def api_emocoes_create():
    user_id = session['user_id']
    payload = request.get_json() or {}
    emoji = payload.get('emoji')
    key = payload.get('key')
    if not emoji:
        return jsonify({'error': 'emoji é obrigatório'}), 400
    listas_ref = get_user_list_ref(user_id).child('emocoes')
    if key:
        listas_ref.child(key).set(emoji)
        return jsonify({'key': key, 'emoji': emoji})
    else:
        new_ref = listas_ref.push(emoji)
        return jsonify({'key': new_ref.key, 'emoji': emoji})


@app.route('/api/emocoes/<string:key>', methods=['PUT'])
@login_required
@verificar_conexao
def api_emocoes_update(key):
    user_id = session['user_id']
    payload = request.get_json() or {}
    emoji = payload.get('emoji')
    if emoji is None:
        return jsonify({'error': 'emoji é obrigatório'}), 400
    listas_ref = get_user_list_ref(user_id).child('emocoes')
    listas_ref.child(key).set(emoji)
    return jsonify({'key': key, 'emoji': emoji})


@app.route('/api/emocoes/<string:key>', methods=['DELETE'])
@login_required
@verificar_conexao
def api_emocoes_delete(key):
    user_id = session['user_id']
    listas_ref = get_user_list_ref(user_id).child('emocoes')
    listas_ref.child(key).delete()
    return jsonify({'deleted': key})


@app.route('/api/habilidades', methods=['POST'])
@login_required
@verificar_conexao
def api_habilidades_create():
    user_id = session['user_id']
    payload = request.get_json() or {}
    nome = payload.get('nome')
    icone = payload.get('icone', '')
    key = payload.get('key')
    if not nome:
        return jsonify({'error': 'nome é obrigatório'}), 400
    listas_ref = get_user_list_ref(user_id).child('habilidades')
    data = {'nome': nome, 'icone': icone}
    if key:
        listas_ref.child(key).set(data)
        return jsonify({'key': key, 'habilidade': data})
    else:
        new_ref = listas_ref.push(data)
        return jsonify({'key': new_ref.key, 'habilidade': data})


@app.route('/api/habilidades/<string:key>', methods=['PUT'])
@login_required
@verificar_conexao
def api_habilidades_update(key):
    user_id = session['user_id']
    payload = request.get_json() or {}
    nome = payload.get('nome')
    icone = payload.get('icone', '')
    if not nome:
        return jsonify({'error': 'nome é obrigatório'}), 400
    listas_ref = get_user_list_ref(user_id).child('habilidades')
    data = {'nome': nome, 'icone': icone}
    listas_ref.child(key).set(data)
    return jsonify({'key': key, 'habilidade': data})


@app.route('/api/habilidades/<string:key>', methods=['DELETE'])
@login_required
@verificar_conexao
def api_habilidades_delete(key):
    user_id = session['user_id']
    listas_ref = get_user_list_ref(user_id).child('habilidades')
    listas_ref.child(key).delete()
    return jsonify({'deleted': key})

@app.route('/deletar-diario/<dia>', methods=['POST'])
@login_required
@verificar_conexao
def deletar_diario(dia):
    """Deleta uma entrada do diário"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id)
    diario_ref.child(dia).delete()
    flash(f'Entrada de {dia} deletada com sucesso.', 'info')
    return redirect(url_for('historico'))


# --- CONFIGURAÇÃO DE UPLOAD ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- ENDPOINTS DE PERFIL DO USUÁRIO ---
@app.route('/perfil')
@login_required
@verificar_conexao
def perfil():
    """Página de perfil do usuário"""
    user_id = session['user_id']
    usuarios_ref = DB_ROOT.child('usuarios')
    usuario_data = usuarios_ref.child(user_id).get()
    
    if usuario_data:
        user_info = usuario_data
        badges_ref = DB_ROOT.child('badges').child(user_id)
        badges_data = badges_ref.get() or {}
    else:
        user_info = {}
        badges_data = {}
    
    return render_template('perfil.html', usuario=user_info, badges=badges_data)


# --- ENDPOINTS DE UPLOAD DE FOTO ---
@app.route('/api/upload-foto', methods=['POST'])
@login_required
@verificar_conexao
def upload_foto():
    """Upload de foto para o diário (base64 ou file)"""
    user_id = session['user_id']
    
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename and allowed_file(file.filename):
            file_data = file.read()
            if len(file_data) <= MAX_FILE_SIZE:
                b64 = base64.b64encode(file_data).decode('utf-8')
                mime_type = f"image/{file.filename.rsplit('.', 1)[1].lower()}"
                photo_url = f"data:{mime_type};base64,{b64}"
                
                galeria_ref = DB_ROOT.child('galeria').child(user_id)
                photo_id = datetime.now().strftime('%Y%m%d%H%M%S')
                galeria_ref.child(photo_id).set({
                    'url': photo_url,
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'filename': secure_filename(file.filename)
                })
                return jsonify({'success': True, 'photo_url': photo_url, 'photo_id': photo_id})
            else:
                return jsonify({'error': 'Arquivo muito grande (máx 5MB)'}), 400
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
    
    photo_url = request.json.get('photo_url', '') if request.json else ''
    if photo_url:
        galeria_ref = DB_ROOT.child('galeria').child(user_id)
        photo_id = datetime.now().strftime('%Y%m%d%H%M%S')
        galeria_ref.child(photo_id).set({
            'url': photo_url,
            'timestamp': int(datetime.now().timestamp() * 1000),
            'filename': 'url_externa'
        })
        return jsonify({'success': True, 'photo_url': photo_url, 'photo_id': photo_id})
    
    return jsonify({'error': 'Nenhuma foto fornecida'}), 400


@app.route('/api/galeria')
@login_required
@verificar_conexao
def api_galeria():
    """Lista de fotos da galeria do usuário"""
    user_id = session['user_id']
    galeria_ref = DB_ROOT.child('galeria').child(user_id)
    fotos = galeria_ref.get() or {}
    
    fotos_list = []
    for photo_id, photo_data in fotos.items():
        fotos_list.append({
            'id': photo_id,
            'url': photo_data.get('url'),
            'timestamp': photo_data.get('timestamp'),
            'filename': photo_data.get('filename', 'foto')
        })
    
    return jsonify({'fotos': sorted(fotos_list, key=lambda x: x['timestamp'], reverse=True)})


# --- ENDPOINTS DE ACHIEVEMENTS ---
@app.route('/achievements')
@login_required
@verificar_conexao
def achievements():
    """Página de achievements e badges"""
    user_id = session['user_id']
    badges_ref = DB_ROOT.child('badges').child(user_id)
    user_badges = badges_ref.get() or {}
    
    all_badges = {
        'primeira_entrada': {'nome': 'Primeira Entrada', 'descricao': 'Crie sua primeira entrada', 'icone': '📝'},
        'sete_dias': {'nome': '7 Dias Seguidos', 'descricao': 'Registre 7 dias consecutivos', 'icone': '🔥'},
        'trinta_dias': {'nome': 'Mês Completo', 'descricao': 'Registre 30 dias no mês', 'icone': '🎯'},
        'cem_entradas': {'nome': '100 Entradas', 'descricao': 'Crie 100 entradas', 'icone': '💯'},
        'explorador': {'nome': 'Explorador', 'descricao': 'Use 5 habilidades diferentes', 'icone': '🗺️'},
        'sentimentos': {'nome': 'Conhecedor de Emoções', 'descricao': 'Registre todas as 8 emoções', 'icone': '💎'},
    }
    
    return render_template('achievements.html', all_badges=all_badges, user_badges=user_badges)


# --- ENDPOINTS DE CONFIGURAÇÕES ---
@app.route('/configuracoes')
@login_required
@verificar_conexao
def configuracoes():
    """Página de configurações do usuário"""
    user_id = session['user_id']
    config_ref = DB_ROOT.child('listas').child(user_id).child('config')
    config_data = config_ref.get() or {}
    
    return render_template('configuracoes.html', config=config_data)


@app.route('/api/config', methods=['POST'])
@login_required
@verificar_conexao
def api_config_update():
    """Atualiza configurações do usuário"""
    user_id = session['user_id']
    config_data = request.get_json() or {}
    
    config_ref = DB_ROOT.child('listas').child(user_id).child('config')
    for key, value in config_data.items():
        config_ref.child(key).set(value)
    
    return jsonify({'success': True})


# --- ENDPOINTS DE BUSCA E FILTRO ---
@app.route('/busca')
@login_required
@verificar_conexao
def busca():
    """Página de busca e filtros avançados"""
    user_id = session['user_id']
    query = request.args.get('q', '')
    emocao_filter = request.args.get('emocao', '')
    habilidade_filter = request.args.get('habilidade', '')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')
    
    diario_ref = get_user_diario_ref(user_id)
    diario_data = diario_ref.get() or {}
    
    resultados = []
    for data_str, entrada in diario_data.items():
        match = True
        
        if query:
            search_text = (entrada.get('journal', '') + ' ' + entrada.get('rotina', '')).lower()
            if query.lower() not in search_text:
                match = False
        
        if emocao_filter and emocao_filter not in entrada.get('emocoes', []):
            match = False
        
        if habilidade_filter and habilidade_filter not in entrada.get('habilidades', []):
            match = False
        
        if data_inicio and data_str < data_inicio:
            match = False
        
        if data_fim and data_str > data_fim:
            match = False
        
        if match:
            resultados.append({'date': data_str, 'data': entrada})
    
    emocoes, habilidades = load_user_lists(user_id)
    
    return render_template('busca.html', 
                          resultados=resultados, 
                          query=query,
                          emocoes=emocoes,
                          habilidades=habilidades,
                          emocao_filter=emocao_filter,
                          habilidade_filter=habilidade_filter,
                          data_inicio=data_inicio,
                          data_fim=data_fim)


# --- ENDPOINTS DE GALERIA ---
@app.route('/galeria')
@login_required
@verificar_conexao
def galeria():
    """Página de galeria de fotos"""
    user_id = session['user_id']
    galeria_ref = DB_ROOT.child('galeria').child(user_id)
    fotos = galeria_ref.get() or {}
    
    return render_template('galeria.html', fotos=fotos)


# --- ENDPOINTS DE COMUNIDADE ---
@app.route('/comunidade')
@login_required
@verificar_conexao
def comunidade():
    """Página de comunidade e feed social"""
    posts_ref = DB_ROOT.child('posts')
    posts = posts_ref.get() or {}
    
    posts_list = []
    for post_id, post_data in posts.items():
        posts_list.append({
            'id': post_id,
            'author': post_data.get('author', 'Usuário'),
            'content': post_data.get('content', ''),
            'timestamp': post_data.get('timestamp', ''),
            'likes': post_data.get('likes', 0),
            'comments': post_data.get('comments', [])
        })
    
    posts_list = sorted(posts_list, key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('comunidade.html', posts=posts_list)


# --- ENDPOINTS DE NOTIFICAÇÕES ---
@app.route('/notificacoes')
@login_required
@verificar_conexao
def notificacoes():
    """Página de notificações"""
    user_id = session['user_id']
    notif_ref = DB_ROOT.child('notificacoes').child(user_id)
    notificacoes_data = notif_ref.get() or {}
    
    notificacoes_list = []
    for notif_id, notif_data in notificacoes_data.items():
        notificacoes_list.append({
            'id': notif_id,
            'tipo': notif_data.get('tipo', 'sistema'),
            'titulo': notif_data.get('titulo', ''),
            'descricao': notif_data.get('descricao', ''),
            'lida': notif_data.get('lida', False),
            'timestamp': notif_data.get('timestamp', '')
        })
    
    notificacoes_list = sorted(notificacoes_list, key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('notificacoes.html', notificacoes=notificacoes_list)


# --- ENDPOINTS DE CALENDÁRIO ---
@app.route('/calendario')
@login_required
@verificar_conexao
def calendario():
    """Página de calendário com heatmap de atividades"""
    user_id = session['user_id']
    diario_ref = get_user_diario_ref(user_id)
    diario_data = diario_ref.get() or {}
    
    # Calcular estatísticas
    total_entradas = len(diario_data)
    
    # Encontrar sequência atual
    hoje = get_hoje()
    sequencia = 0
    # get_hoje() retorna YYYY-MM-DD, então usamos esse formato aqui
    try:
        data_check = datetime.strptime(hoje, '%Y-%m-%d')
    except Exception:
        # fallback para formatos já exibidos no banco (DD/MM/YYYY)
        try:
            data_check = datetime.strptime(hoje, '%d/%m/%Y')
        except Exception:
            data_check = datetime.now()

    while True:
        # usamos chave YYYY-MM-DD para procurar entradas no diário
        data_str = data_check.strftime('%Y-%m-%d')
        if data_str in diario_data and diario_data[data_str].get('journal'):
            sequencia += 1
            data_check -= timedelta(days=1)
        else:
            break
    
    emocoes, habilidades = load_user_lists(user_id)
    
    return render_template('calendario.html', 
                          total_entradas=total_entradas,
                          sequencia_atual=sequencia,
                          diario_data=diario_data,
                          emocoes=emocoes,
                          habilidades=habilidades)


if __name__ == '__main__':
    app.run(debug=True)
