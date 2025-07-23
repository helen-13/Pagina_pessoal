from app import app, db
from models import Course, Module, Lesson, User
from datetime import datetime

def init_courses():
    with app.app_context():
        # Criar cursos
        word_course = Course(
            title='Microsoft Word - Do Básico ao Avançado',
            description='Aprenda a usar o Microsoft Word de forma profissional, desde o básico até recursos avançados.',
            price=197.00,
            duration=20,
            level='Iniciante',
            image='word-course.jpg'
        )
        
        canva_course = Course(
            title='Canva - Design Gráfico para Iniciantes',
            description='Crie designs profissionais com o Canva, mesmo sem experiência em design gráfico.',
            price=147.00,
            duration=15,
            level='Iniciante',
            image='canva-course.jpg'
        )
        
        ai_course = Course(
            title='Inteligência Artificial para Negócios',
            description='Entenda como aplicar IA em seu negócio e aumentar sua produtividade.',
            price=297.00,
            duration=25,
            level='Intermediário',
            image='ai-course.jpg'
        )
        
        db.session.add_all([word_course, canva_course, ai_course])
        db.session.commit()
        
        # Módulos do curso de Word
        word_modules = [
            Module(
                title='Introdução ao Word',
                description='Conheça a interface e as ferramentas básicas do Word.',
                order=1,
                course_id=word_course.id
            ),
            Module(
                title='Formatação de Texto',
                description='Aprenda a formatar textos de forma profissional.',
                order=2,
                course_id=word_course.id
            ),
            Module(
                title='Tabelas e Gráficos',
                description='Crie e formate tabelas e gráficos no Word.',
                order=3,
                course_id=word_course.id
            )
        ]
        
        # Módulos do curso de Canva
        canva_modules = [
            Module(
                title='Conhecendo o Canva',
                description='Aprenda a navegar pela plataforma e usar as ferramentas básicas.',
                order=1,
                course_id=canva_course.id
            ),
            Module(
                title='Design de Posts',
                description='Crie posts profissionais para redes sociais.',
                order=2,
                course_id=canva_course.id
            ),
            Module(
                title='Apresentações',
                description='Desenvolva apresentações impactantes.',
                order=3,
                course_id=canva_course.id
            )
        ]
        
        # Módulos do curso de IA
        ai_modules = [
            Module(
                title='Fundamentos de IA',
                description='Entenda os conceitos básicos de Inteligência Artificial.',
                order=1,
                course_id=ai_course.id
            ),
            Module(
                title='ChatGPT e Outras IAs',
                description='Aprenda a usar ferramentas de IA generativa.',
                order=2,
                course_id=ai_course.id
            ),
            Module(
                title='Aplicações Práticas',
                description='Veja exemplos reais de uso de IA em negócios.',
                order=3,
                course_id=ai_course.id
            )
        ]
        
        db.session.add_all(word_modules + canva_modules + ai_modules)
        db.session.commit()
        
        # Aulas do curso de Word
        word_lessons = [
            Lesson(
                title='Interface do Word',
                content='<p>Nesta aula, você vai conhecer a interface do Word e suas principais ferramentas.</p>',
                video_url='https://www.youtube.com/embed/example1',
                duration=30,
                order=1,
                module_id=word_modules[0].id
            ),
            Lesson(
                title='Salvando Documentos',
                content='<p>Aprenda a salvar seus documentos em diferentes formatos.</p>',
                video_url='https://www.youtube.com/embed/example2',
                duration=20,
                order=2,
                module_id=word_modules[0].id
            )
        ]
        
        # Aulas do curso de Canva
        canva_lessons = [
            Lesson(
                title='Criando uma Conta',
                content='<p>Saiba como criar e configurar sua conta no Canva.</p>',
                video_url='https://www.youtube.com/embed/example3',
                duration=15,
                order=1,
                module_id=canva_modules[0].id
            ),
            Lesson(
                title='Templates',
                content='<p>Aprenda a usar e personalizar templates.</p>',
                video_url='https://www.youtube.com/embed/example4',
                duration=25,
                order=2,
                module_id=canva_modules[0].id
            )
        ]
        
        # Aulas do curso de IA
        ai_lessons = [
            Lesson(
                title='O que é IA?',
                content='<p>Entenda o conceito de Inteligência Artificial e suas aplicações.</p>',
                video_url='https://www.youtube.com/embed/example5',
                duration=40,
                order=1,
                module_id=ai_modules[0].id
            ),
            Lesson(
                title='Tipos de IA',
                content='<p>Conheça os diferentes tipos de IA e suas características.</p>',
                video_url='https://www.youtube.com/embed/example6',
                duration=35,
                order=2,
                module_id=ai_modules[0].id
            )
        ]
        
        db.session.add_all(word_lessons + canva_lessons + ai_lessons)
        db.session.commit()
        
        print('Cursos, módulos e aulas criados com sucesso!')


if __name__ == '__main__':
    init_courses() 