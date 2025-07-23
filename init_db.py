from app import app, db
from models import User

def init_db():
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existe um usuário admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Criar usuário admin
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Usuário admin criado com sucesso!')
        else:
            print('Usuário admin já existe!')

if __name__ == '__main__':
    init_db() 



    