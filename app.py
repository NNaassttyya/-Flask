from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask import jsonify
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Добавляем секретный ключ для сессий
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


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    venue_type = db.Column(db.String(50), nullable=False)  # restaurant, bar, club
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    images = db.Column(db.Text)  # JSON строка с путями к изображениям
    current_visitors = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


class MapPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship('Post', backref=db.backref('map_points', lazy=True))


# Функция-декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


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

        # Проверяем, существует ли пользователь
        existing_user = Post.query.filter_by(login=login).first()
        if existing_user:
            # Если пользователь существует и пароль совпадает - выполняем вход
            if existing_user.password == password:
                session['user_id'] = existing_user.id
                return redirect(url_for('map'))
            else:
                return 'Неверный пароль'
        
        # Если пользователь не существует - регистрируем
        post = Post(login=login, email=email, password=password)

        try:
            db.session.add(post)
            db.session.commit()
            # После успешной регистрации сразу выполняем вход
            session['user_id'] = post.id
            return redirect(url_for('map'))
        except:
            return 'При регистрации произошла ошибка'
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
@login_required
def map():
    """Страница с картой заведений
    ---
    tags:
      - Основные страницы
    responses:
      200:
        description: HTML страницы с картой
    """
    return render_template('map.html', current_user_id=session.get('user_id'))


@app.route('/add_point', methods=['POST'])
@login_required
def add_point():
    """Добавление новой точки на карту
    ---
    tags:
      - Карта
    """
    try:
        data = request.json
        new_point = MapPoint(
            user_id=session['user_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            description=data['description'],
            end_time=datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M'),
            created_at=datetime.now()
        )
        db.session.add(new_point)
        db.session.commit()
        return jsonify({'success': True, 'point_id': new_point.id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/get_points', methods=['GET'])
@login_required
def get_points():
    """Получение всех активных точек на карте
    ---
    tags:
      - Карта
    """
    current_time = datetime.now()
    points = MapPoint.query.filter(MapPoint.end_time >= current_time).all()
    points_data = [{
        'id': point.id,
        'latitude': point.latitude,
        'longitude': point.longitude,
        'description': point.description,
        'end_time': point.end_time.strftime('%Y-%m-%dT%H:%M'),
        'user_login': point.user.login,
        'user_id': point.user_id
    } for point in points]
    return jsonify(points_data)

@app.route('/delete_point/<int:point_id>', methods=['DELETE'])
@login_required
def delete_point(point_id):
    """Удаление точки с карты
    ---
    tags:
      - Карта
    """
    point = MapPoint.query.get_or_404(point_id)
    if point.user_id != session['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(point)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/get_venues', methods=['GET'])
def get_venues():
    """Получение списка заведений
    ---
    tags:
      - Заведения
    """
    venue_type = request.args.get('type')  # restaurant, bar, club
    query = Venue.query
    
    if venue_type:
        query = query.filter_by(venue_type=venue_type)
    
    venues = query.all()
    venues_data = [{
        'id': venue.id,
        'name': venue.name,
        'description': venue.description,
        'venue_type': venue.venue_type,
        'latitude': venue.latitude,
        'longitude': venue.longitude,
        'images': venue.images,
        'current_visitors': venue.current_visitors
    } for venue in venues]
    
    return jsonify(venues_data)

@app.route('/add_visitor', methods=['POST'])
@login_required
def add_visitor():
    """Отметиться в заведении
    ---
    tags:
      - Заведения
    """
    try:
        data = request.json
        venue_id = data['venue_id']
        description = data.get('description', '')
        end_time = data['end_time']
        
        venue = Venue.query.get_or_404(venue_id)
        venue.current_visitors += 1
        
        new_point = MapPoint(
            user_id=session['user_id'],
            latitude=venue.latitude,
            longitude=venue.longitude,
            description=description,
            end_time=datetime.strptime(end_time, '%Y-%m-%dT%H:%M'),
            created_at=datetime.now()
        )
        
        db.session.add(new_point)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'point_id': new_point.id,
            'current_visitors': venue.current_visitors
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/remove_visitor/<int:point_id>', methods=['DELETE'])
@login_required
def remove_visitor(point_id):
    """Удалить отметку о присутствии в заведении
    ---
    tags:
      - Заведения
    """
    point = MapPoint.query.get_or_404(point_id)
    if point.user_id != session['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        # Находим ближайшее заведение к точке
        venue = Venue.query.filter(
            db.func.abs(Venue.latitude - point.latitude) < 0.0001,
            db.func.abs(Venue.longitude - point.longitude) < 0.0001
        ).first()
        
        if venue and venue.current_visitors > 0:
            venue.current_visitors -= 1
        
        db.session.delete(point)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'current_visitors': venue.current_visitors if venue else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
