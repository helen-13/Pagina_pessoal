from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime, timedelta, timezone, date, time, tzinfo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

class ProfileForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Biografia', validators=[Optional(), Length(max=500)])
    profile_picture = FileField('Foto de Perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens são permitidas!')
    ])
    password = PasswordField('Nova Senha', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[EqualTo('password')])
    submit = SubmitField('Atualizar Perfil')

class CourseForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    price = FloatField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    level = SelectField('Nível', choices=[
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado')
    ], validators=[DataRequired()])
    duration = IntegerField('Duração (horas)', validators=[DataRequired(), NumberRange(min=1)])
    image = FileField('Imagem do Curso', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens são permitidas!')
    ])
    is_featured = BooleanField('Destacar na Página Inicial')
    submit = SubmitField('Salvar Curso')

class ModuleForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição', validators=[Optional()])
    submit = SubmitField('Salvar Módulo')

class LessonForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Conteúdo', validators=[DataRequired()])
    video_url = StringField('URL do Vídeo', validators=[Optional()])
    submit = SubmitField('Salvar Aula')

class MentorshipForm(FlaskForm):
    subject = StringField('Assunto', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Solicitar Mentoria')

class EsqueciForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Recuperar Senha')

class EditarPerfilForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Biografia')
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png'], 'Apenas imagens!')])
    submit = SubmitField('Atualizar Perfil')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            from models import User
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        if email.data != self.original_email:
            from models import User
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este email já está em uso.')

class AlterarSenhaForm(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('confirmar_senha', message='As senhas devem ser iguais')
    ])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired()])
    submit = SubmitField('Alterar Senha')

class MentoringSessionForm(FlaskForm):
    date = DateTimeField('Data e Hora', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    duration = SelectField('Duração', choices=[
        (30, '30 minutos'),
        (60, '1 hora'),
        (90, '1 hora e 30 minutos'),
        (120, '2 horas')
    ], validators=[DataRequired()])
    notes = TextAreaField('Observações')
    submit = SubmitField('Agendar Mentoria')

    def validate_date(self, date):
        if date.data < datetime.now():
            raise ValidationError('A data deve ser futura.')
        if date.data > datetime.now() + timedelta(days=30):
            raise ValidationError('A data deve estar dentro dos próximos 30 dias.')


