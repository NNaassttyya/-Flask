from flask import Flask, render_template, request, redirect
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
db = SQLAlchemy(app)

from flask_mail import Mail, Message

# Конфигурация почты
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cityvibe859@gmail.com'
app.config['MAIL_PASSWORD'] = 'NK6-j6s-sDS-akk'
app.config['MAIL_DEFAULT_SENDER'] = 'cityvibe859@gmail.com'

mail = Mail(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)


#  SWAGGER

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # Все правила включаются
            "model_filter": lambda tag: True,  # Все модели включаются
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"  # URL для доступа к Swagger UI
}

Swagger(app, config=swagger_config, template={
    "info": {
        "title": "API",
        "description": "",
        "version": "1.0.0",
        "contact": {
            "email": "support@example.com"
        }
    },
    "tags": [
        {
            "name": "Основные страницы",
            "description": "Главные страницы сайта"
        }
    ]
})


# 2. МОДИФИКАЦИЯ СУЩЕСТВУЮЩИХ РОУТОВ
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        login = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        post = Post(login=login, email=email, password=password)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')

        except:
            return 'При регистации произошла ошибка'


    else:
        return render_template('index.html')
    """Главная страница
    ---
    tags:
      - Основные страницы
    responses:
      200:
        description: HTML главной страницы
    """
    return render_template('index.html')


@app.route('/support', methods=['GET', 'POST'])
def support():
    """Страница поддержки
    ---
    tags:
      - Основные страницы
    responses:
      200:
        description: HTML страницы поддержки
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')

        try:
            msg = Message(
                subject=f"Сообщение от {name} через форму поддержки",
                recipients=['cityvibe859@gmail.com'],
                body=f"""
                Имя: {name}
                Email: {email}
                Сообщение:
                {message_text}
                """
            )
            mail.send(msg)
            return jsonify({'success': True})
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    return render_template('support.html')


@app.route('/map')
def map():
    """Страница с картой заведений
    ---
    tags:
      - Основные страницы
    responses:
      200:
        description: HTML страницы с картой
    """
    return render_template('map.html')





if __name__ == '__main__':
    app.run(debug=True)
