from datetime import datetime, timedelta, date
import random
from faker import Faker
from models import Flight, Event  # 导入模型
from database import db, init_db  # 导入数据库实例

fake = Faker()

AIRPORTS = [
    {'code': 'AKL', 'name': 'Auckland Airport'},
    {'code': 'WLG', 'name': 'Wellington Airport'},
    {'code': 'CHC', 'name': 'Christchurch Airport'},
    {'code': 'ZQN', 'name': 'Queenstown Airport'},
    {'code': 'DUD', 'name': 'Dunedin Airport'},
]

# 添加一个函数来生成假的航班数据
def add_fake_flights(num_flights):
    airlines = ['Air New Zealand', 'Jetstar', 'Qantas', 'Virgin Australia']
    today = date.today()
    one_month_later = today + timedelta(days=30)
    
    for _ in range(num_flights):
        departure_airport = random.choice(AIRPORTS)
        arrival_airport = random.choice([a for a in AIRPORTS if a != departure_airport])
        
        departure_date = fake.date_between(start_date=today, end_date=one_month_later)
        departure_time = fake.time_object()
        flight_duration = timedelta(hours=random.randint(1, 5))
        departure_datetime = datetime.combine(departure_date, departure_time)
        arrival_datetime = departure_datetime + flight_duration
        
        flight = Flight(
            flight_number=f"{random.choice(['NZ', 'JQ', 'QF', 'VA'])}{random.randint(100, 999)}",
            departure_airport=departure_airport['code'],
            arrival_airport=arrival_airport['code'],
            departure_date=departure_date,
            departure_time=departure_time,
            arrival_date=arrival_datetime.date(),
            arrival_time=arrival_datetime.time(),
            airline=random.choice(airlines),
            economy_price=round(random.uniform(50, 500), 2),
            business_price=round(random.uniform(200, 1500), 2),
            available_economy_seats=random.randint(0, 200),
            available_business_seats=random.randint(0, 50)
        )
        db.session.add(flight)
    db.session.commit()

def add_fake_events(num_events):
    for _ in range(num_events):
        event = Event(
            title=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=3),
            address=fake.address(),
            price=round(random.uniform(10, 200), 2),
            date=fake.date_time_between(start_date='now', end_date='+1y'),
            image_url=fake.image_url(),
            details=fake.text()
        )
        db.session.add(event)
    db.session.commit()

def populate_database(app):
    init_db(app)
    with app.app_context():
        db.create_all()  # 确保所有表都已创建
        events_count = Event.query.count()
        if events_count < 100:
            add_fake_events(100 - events_count)
        
        flights_count = Flight.query.count()
        if flights_count < 1000:
            add_fake_flights(1000 - flights_count)
        