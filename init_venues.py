from app import db, Venue
import json

# Создаем все таблицы
db.create_all()

# Список ресторанов
restaurants = [
    {
        "name": "KITCHEN",
        "description": "Уральская кухня, панорамный вид на Исеть. Бренд-шеф — Сергей Мирошников.",
        "venue_type": "restaurant",
        "latitude": 56.8361,
        "longitude": 60.6123
    },
    {
        "name": "Gosti",
        "description": "Грузинское бистро с живой музыкой.",
        "venue_type": "restaurant",
        "latitude": 56.8385,
        "longitude": 60.6052
    },
    {
        "name": "Choclo",
        "description": "Перуанская кухня, уютный интерьер.",
        "venue_type": "restaurant",
        "latitude": 56.8379,
        "longitude": 60.6031
    },
    {
        "name": "Breadway",
        "description": "Разнообразное меню с акцентом на европейскую кухню.",
        "venue_type": "restaurant",
        "latitude": 56.8350,
        "longitude": 60.5978
    },
    {
        "name": "Panorama",
        "description": "Ресторан в БЦ «Высоцкий» с видом на Ижевский пруд.",
        "venue_type": "restaurant",
        "latitude": 56.8432,
        "longitude": 60.6531
    },
    {
        "name": "Сыроварня",
        "description": "Итальянская кухня, уютная атмосфера.",
        "venue_type": "restaurant",
        "latitude": 56.8324,
        "longitude": 60.6120
    },
    {
        "name": "The BARBARA",
        "description": "Модный ресторан с европейской и морской кухней.",
        "venue_type": "restaurant",
        "latitude": 56.8376,
        "longitude": 60.5973
    },
    {
        "name": "Гуливани",
        "description": "Аутентичная грузинская кухня, живая музыка.",
        "venue_type": "restaurant",
        "latitude": 56.8145,
        "longitude": 60.6257
    },
    {
        "name": "Троекуров",
        "description": "Русская дворянская кухня в особняке XIX века.",
        "venue_type": "restaurant",
        "latitude": 56.8301,
        "longitude": 60.6148
    },
    {
        "name": "Стейк-Хаус",
        "description": "Стейки и мясные блюда в здании гостиницы «Исеть».",
        "venue_type": "restaurant",
        "latitude": 56.8382,
        "longitude": 60.5984
    },
    {
        "name": "Gavi",
        "description": "Итальянская кухня и винная карта.",
        "venue_type": "restaurant",
        "latitude": 56.8357,
        "longitude": 60.6079
    },
    {
        "name": "Гады, Крабы и Вино",
        "description": "Морская кухня и авторские блюда.",
        "venue_type": "restaurant",
        "latitude": 56.8296,
        "longitude": 60.6105
    },
    {
        "name": "Friends",
        "description": "Международная кухня, атмосфера дружеских встреч.",
        "venue_type": "restaurant",
        "latitude": 56.8364,
        "longitude": 60.6120
    },
    {
        "name": "Своя компания",
        "description": "Уютное место с разнообразным меню.",
        "venue_type": "restaurant",
        "latitude": 56.8342,
        "longitude": 60.6067
    },
    {
        "name": "Engels",
        "description": "Завтраки и кофейная культура.",
        "venue_type": "restaurant",
        "latitude": 56.8335,
        "longitude": 60.6051
    }
]

# Список баров
bars = [
    {
        "name": "Alibi",
        "description": "Бар с европейской кухней и вечерними мероприятиями.",
        "venue_type": "bar",
        "latitude": 56.8320,
        "longitude": 60.6083
    },
    {
        "name": "Sekta",
        "description": "Винный бар с органическими винами.",
        "venue_type": "bar",
        "latitude": 56.8430,
        "longitude": 60.5982
    },
    {
        "name": "Marlerino Lounge",
        "description": "Кальян-бар с авторскими напитками.",
        "venue_type": "bar",
        "latitude": 56.8371,
        "longitude": 60.6024
    },
    {
        "name": "Руки вверх бар",
        "description": "Танцевальный бар с живой музыкой.",
        "venue_type": "bar",
        "latitude": 56.8358,
        "longitude": 60.6115
    },
    {
        "name": "The Rosy Jane Pub & Whisky Bar",
        "description": "Английский паб с коллекцией виски.",
        "venue_type": "bar",
        "latitude": 56.8380,
        "longitude": 60.6001
    },
    {
        "name": "Ben Hall",
        "description": "Бар в стиле старой Англии.",
        "venue_type": "bar",
        "latitude": 56.8412,
        "longitude": 60.5953
    },
    {
        "name": "НСБ by КАМ",
        "description": "Бар с меняющейся коктейльной картой.",
        "venue_type": "bar",
        "latitude": 56.8365,
        "longitude": 60.6048
    },
    {
        "name": "Коллектив",
        "description": "Авторские коктейли и уютная атмосфера.",
        "venue_type": "bar",
        "latitude": 56.8367,
        "longitude": 60.6132
    },
    {
        "name": "Негодяи",
        "description": "Бар с вечерними вечеринками.",
        "venue_type": "bar",
        "latitude": 56.8389,
        "longitude": 60.5976
    },
    {
        "name": "MeyerStreet",
        "description": "Израильская кухня и веганские блюда.",
        "venue_type": "bar",
        "latitude": 56.8339,
        "longitude": 60.6055
    },
    {
        "name": "Байки",
        "description": "Уютный бар для романтических встреч.",
        "venue_type": "bar",
        "latitude": 56.8421,
        "longitude": 60.5942
    },
    {
        "name": "Museum",
        "description": "Кальян-бар с атмосферой релакса.",
        "venue_type": "bar",
        "latitude": 56.8273,
        "longitude": 60.6180
    },
    {
        "name": "Luna",
        "description": "Лаундж-бар с азиатской кухней.",
        "venue_type": "bar",
        "latitude": 56.8359,
        "longitude": 60.6117
    },
    {
        "name": "Ёпрст бар",
        "description": "Танцевальная музыка и вечеринки.",
        "venue_type": "bar",
        "latitude": 56.8150,
        "longitude": 60.6342
    },
    {
        "name": "Nebar",
        "description": "Легендарный клуб с двумя танцполами.",
        "venue_type": "bar",
        "latitude": 56.8358,
        "longitude": 60.6115
    }
]

# Добавляем все заведения в базу данных
for venue_data in restaurants + bars:
    venue = Venue(
        name=venue_data["name"],
        description=venue_data["description"],
        venue_type=venue_data["venue_type"],
        latitude=venue_data["latitude"],
        longitude=venue_data["longitude"],
        images="[]",  # Пустой список изображений по умолчанию
        current_visitors=0
    )
    db.session.add(venue)

try:
    db.session.commit()
    print("Все заведения успешно добавлены в базу данных!")
except Exception as e:
    db.session.rollback()
    print(f"Произошла ошибка при добавлении заведений: {str(e)}") 