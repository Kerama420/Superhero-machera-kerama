from config import create_app, db
from models import Hero, Power

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    heroes = [
        Hero(name="Bruce Wayne", super_name="Batman"),
        Hero(name="Clark Kent", super_name="Superman"),
        Hero(name="Diana Prince", super_name="Wonder Woman")
    ]

    powers = [
        Power(name="Super Strength", description="Gives the wielder super-human strengths"),
        Power(name="Flight", description="Gives the wielder the ability to fly"),
        Power(name="Invisibility", description="Makes the wielder invisible to the naked eye")
    ]

    db.session.add_all(heroes + powers)
    db.session.commit()

    print("🌱 Database seeded!")
