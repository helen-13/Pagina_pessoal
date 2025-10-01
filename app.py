from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify, abort
from markupsafe import escape
from forms import (
    RegistrationForm, LoginForm, EsqueciForm, EditarPerfilForm, AlterarSenhaForm,
    CourseForm, ModuleForm, LessonForm, MentoringSessionForm, RegistrationForm, ProfileForm, MentorshipForm
)
from models import db, User, Course, Module, Lesson, Purchase, Mentorship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import click

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Você não tem permissão para acessar esta página.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    courses = Course.query.filter_by(is_featured=True).all()
    purchases = []
    if current_user.is_authenticated:
        purchases = [p.course_id for p in current_user.purchases]
    return render_template('home.html', courses=courses, purchases=purchases)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'info')
    return redirect(url_for('home'))

@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = EsqueciForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Aqui você implementaria o envio de email
            flash('Se o email existir em nossa base, você receberá instruções para redefinir sua senha.', 'info')
        return redirect(url_for('login'))
    return render_template('esqueci_senha.html', form=form)

@app.route('/profile/<username>')
@login_required
def show_user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@app.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            form.profile_picture.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_picture = filename
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('show_user_profile', username=current_user.username))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    
    return render_template('editar_perfil.html', form=form)

@app.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        if current_user.check_password(form.senha_atual.data):
            current_user.set_password(form.nova_senha.data)
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('show_user_profile', username=current_user.username))
        flash('Senha atual incorreta', 'error')
    return render_template('alterar_senha.html', form=form)

@app.route('/admin')
@login_required
@admin_required
def admin():
    if not current_user.is_admin:
        abort(403)
    
    courses = Course.query.all()
    users = User.query.all()
    mentorias = Mentorship.query.all()
    return render_template('admin.html', courses=courses, users=users, mentorias=mentorias)

@app.route('/admin/toggle/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Você não pode alterar seu próprio status de administrador'})
    
    user.is_admin = not user.is_admin
    db.session.commit()
    return jsonify({'success': True})

@app.route('/cursos')
def cursos():
    courses = Course.query.all()
    purchases = []
    if current_user.is_authenticated:
        purchases = [p.course_id for p in current_user.purchases]
    return render_template('cursos.html', courses=courses, purchases=purchases)

@app.route('/curso/<int:course_id>')
def curso_detail(course_id):
    course = Course.query.get_or_404(course_id)
    purchase = None
    if current_user.is_authenticated:
        purchase = Purchase.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    return render_template('curso_detail.html', course=course, purchase=purchase)

@app.route('/comprar/<int:course_id>', methods=['POST'])
@login_required
def comprar_curso(course_id):
    course = Course.query.get_or_404(course_id)
    if Purchase.query.filter_by(user_id=current_user.id, course_id=course_id).first():
        flash('Você já possui este curso!', 'warning')
        return redirect(url_for('curso_detail', course_id=course_id))
    
    purchase = Purchase(user_id=current_user.id, course_id=course_id)
    db.session.add(purchase)
    db.session.commit()
    
    flash('Curso adquirido com sucesso!', 'success')
    return redirect(url_for('curso_detail', course_id=course_id))

@app.route('/meus-cursos')
@login_required
def meus_cursos():
    purchases = Purchase.query.filter_by(user_id=current_user.id).all()
    courses = [p.course for p in purchases]
    return render_template('meus_cursos.html', courses=courses)

@app.route('/aula/<int:course_id>/<int:lesson_id>')
@login_required
def aula_detail(course_id, lesson_id):
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Verificar se o usuário comprou o curso
    purchase = Purchase.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not purchase and not current_user.is_admin:
        flash('Você precisa comprar este curso para acessar as aulas.', 'warning')
        return redirect(url_for('curso_detail', course_id=course_id))
    
    # Encontrar a próxima e anterior aula
    current_module = lesson.module
    current_module_index = course.modules.index(current_module)
    current_lesson_index = current_module.lessons.index(lesson)
    
    next_lesson = None
    prev_lesson = None
    
    # Próxima aula
    if current_lesson_index < len(current_module.lessons) - 1:
        next_lesson = current_module.lessons[current_lesson_index + 1]
    elif current_module_index < len(course.modules) - 1:
        next_module = course.modules[current_module_index + 1]
        if next_module.lessons:
            next_lesson = next_module.lessons[0]
    
    # Aula anterior
    if current_lesson_index > 0:
        prev_lesson = current_module.lessons[current_lesson_index - 1]
    elif current_module_index > 0:
        prev_module = course.modules[current_module_index - 1]
        if prev_module.lessons:
            prev_lesson = prev_module.lessons[-1]
    
    return render_template('aula_detail.html', 
                         course=course, 
                         lesson=lesson, 
                         next_lesson=next_lesson, 
                         prev_lesson=prev_lesson)

@app.route('/mentorias', methods=['GET', 'POST'])
@login_required
def mentorias():
    from datetime import datetime
    form = MentoringSessionForm()
    if form.validate_on_submit():
        session = Mentorship(
            user_id=current_user.id,
            scheduled_date=form.date.data,
            notes=form.notes.data,
            status='pending',
            created_at=datetime.utcnow()
        )
        db.session.add(session)
        db.session.commit()
        flash('Mentoria agendada com sucesso!', 'success')
        return redirect(url_for('mentorias'))

    sessions = Mentorship.query.filter_by(user_id=current_user.id).order_by(Mentorship.scheduled_date.desc()).all()
    now = datetime.now()
    return render_template('agendar_mentoria.html', form=form, sessions=sessions, now=now)

# Rotas administrativas
@app.route('/admin/cursos')
@login_required
@admin_required
def admin_cursos():
    courses = Course.query.all()
    return render_template('admin/cursos.html', courses=courses)

@app.route('/admin/curso/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_curso():
    if not current_user.is_admin:
        abort(403)
    
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            level=form.level.data,
            duration=form.duration.data,
            is_featured=form.is_featured.data
        )
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            course.image = filename
        
        db.session.add(course)
        db.session.commit()
        flash('Curso criado com sucesso!', 'success')
        return redirect(url_for('admin_cursos'))
    
    return render_template('admin/novo_curso.html', form=form)

@app.route('/admin/curso/<int:course_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_curso(course_id):
    if not current_user.is_admin:
        abort(403)
    
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.price = form.price.data
        course.level = form.level.data
        course.duration = form.duration.data
        course.is_featured = form.is_featured.data
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            course.image = filename
        
        db.session.commit()
        flash('Curso atualizado com sucesso!', 'success')
        return redirect(url_for('admin_cursos'))
    
    return render_template('admin/editar_curso.html', form=form, course=course)

@app.route('/admin/curso/<int:course_id>/deletar', methods=['POST'])
@login_required
@admin_required
def deletar_curso(course_id):
    if not current_user.is_admin:
        abort(403)
    
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Curso deletado com sucesso!', 'success')
    return redirect(url_for('admin_cursos'))

@app.route('/admin/curso/<int:course_id>/modulo/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_modulo(course_id):
    if not current_user.is_admin:
        abort(403)
    
    course = Course.query.get_or_404(course_id)
    form = ModuleForm()
    
    if form.validate_on_submit():
        module = Module(
            title=form.title.data,
            description=form.description.data,
            course_id=course_id
        )
        db.session.add(module)
        db.session.commit()
        flash('Módulo criado com sucesso!', 'success')
        return redirect(url_for('editar_curso', course_id=course_id))
    
    return render_template('admin/novo_modulo.html', form=form, course=course)

@app.route('/admin/modulo/<int:module_id>/aula/nova', methods=['GET', 'POST'])
@login_required
@admin_required
def nova_aula(module_id):
    if not current_user.is_admin:
        abort(403)
    
    module = Module.query.get_or_404(module_id)
    form = LessonForm()
    
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            content=form.content.data,
            video_url=form.video_url.data,
            module_id=module_id
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Aula criada com sucesso!', 'success')
        return redirect(url_for('editar_curso', course_id=module.course_id))
    
    return render_template('admin/nova_aula.html', form=form, module=module)

@app.route('/admin/modulo/<int:module_id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_modulo(module_id):
    module = Module.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/aula/<int:lesson_id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_aula(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/aula/<int:lesson_id>/completar', methods=['POST'])
@login_required
def completar_aula(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course_id
    ).first()
    
    if not purchase:
        return jsonify({'success': False, 'error': 'Curso não comprado'})
    
    lesson.completed = True
    db.session.commit()
    return jsonify({'success': True})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CLI: cria superusuário (admin)
@app.cli.command('createsuperuser')
@click.option('--username', prompt=True, help='Nome de usuário (único)')
@click.option('--email', prompt=True, help='Email do usuário (único)')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Senha do usuário')
def create_super_user(username, email, password):
    """Cria um usuário administrador com is_admin=True."""
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        click.echo('Usuário com este username ou email já existe.')
        return
    user = User(username=username, email=email, is_admin=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo('Superusuário criado com sucesso!')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)