from app import app, db, Venue
from datetime import datetime
import json

test_venues = [
    {
        'name': 'Panorama',
        'description': 'Ресторан с панорамным видом на город. Европейская и азиатская кухня.',
        'venue_type': 'restaurant',
        'latitude': 55.7558,
        'longitude': 37.6173,
        'images': json.dumps([
            'images/panoram1-img.webp',
            'images/panorama2-img.webp',
            'images/panorma3-img.webp'
        ]),
        'current_visitors': 12
    },
    {
        'name': 'Сыроварня',
        'description': 'Ресторан итальянской кухни с собственным производством сыров.',
        'venue_type': 'restaurant',
        'latitude': 55.7532,
        'longitude': 37.6225,
        'images': json.dumps([
            'images/syrovarnya1.webp',
            'images/syrovarnya2.webp',
            'images/syrovarnya3.webp'
        ]),
        'current_visitors': 8
    },
    {
        'name': 'Бар "Стрелка"',
        'description': 'Модный бар с авторскими коктейлями и живой музыкой.',
        'venue_type': 'bar',
        'latitude': 55.7414,
        'longitude': 37.6290,
        'images': json.dumps([
            'images/strelka1.webp',
            'images/strelka2.webp',
            'images/strelka3.webp'
        ]),
        'current_visitors': 15
    },
    {
        'name': 'Клуб "Бессонница"',
        'description': 'Ночной клуб с электронной музыкой и световым шоу.',
        'venue_type': 'club',
        'latitude': 55.7601,
        'longitude': 37.6333,
        'images': json.dumps([
            'images/insomnia1.webp',
            'images/insomnia2.webp',
            'images/insomnia3.webp'
        ]),
        'current_visitors': 45
    }
]

def add_test_venues():
    with app.app_context():
        # Удаляем все существующие заведения
        Venue.query.delete()
        
        # Добавляем тестовые заведения
        for venue_data in test_venues:
            venue = Venue(**venue_data)
            db.session.add(venue)
        
        db.session.commit()
        print("Тестовые заведения успешно добавлены!")

if __name__ == '__main__':
    add_test_venues() 