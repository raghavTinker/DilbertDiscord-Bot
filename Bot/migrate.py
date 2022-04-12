from database import SessionLocal, engine
import models
import json

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)


def importComics():
    # open comics.json
    with open('comics.json') as f:
        comics = json.load(f)

    # new comic
    for comic in comics:
        newComic = models.Comics(
            title=comic['title'],
            description=comic['description'],
            image=comic['image'],
            link=comic['link'],
            date=comic['date']
        )
        db.add(newComic)
    db.commit()
importComics()