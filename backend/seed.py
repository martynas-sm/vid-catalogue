# use with: uv run python seed.py

from database import SessionLocal, engine
from models import Annotation, Catalog, User, Video
from models.base import Base


def seed_users(db):
    users_data = [
        {
            "username": "user1",
            "email": "u1@example.com",
            "hashed_password": "pass",
            "role": "admin",
        },
    ]
    users = [User(**u) for u in users_data]
    db.add_all(users)
    db.flush()
    return users


def seed_catalogs(db, user_id):
    catalogs_data = [
        {
            "name": "Catalog 1",
            "description": "Desc 1",
            "is_public": True,
            "user_id": user_id,
        },
    ]
    catalogs = [Catalog(**c) for c in catalogs_data]
    db.add_all(catalogs)
    db.flush()
    return catalogs


def seed_videos(db, catalog_id):
    videos_data = [
        {
            "catalog_id": catalog_id,
            "title": "Video 1",
            "url": "https://youtube.com/watch?v=1",
            "duration": 100.0,
            "transcript": "Transcript 1",
        },
    ]
    videos = [Video(**v) for v in videos_data]
    db.add_all(videos)
    db.flush()
    return videos


def seed_annotations(db, video_id):
    annotations_data = [
        {
            "video_id": video_id,
            "text": "Note 1",
            "from_dur": 0.0,
            "to_dur": 10.0,
        },
    ]
    annotations = [Annotation(**a) for a in annotations_data]
    db.add_all(annotations)
    db.flush()
    return annotations


def main():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        users = seed_users(db)
        catalogs = seed_catalogs(db, users[0].id)
        videos = seed_videos(db, catalogs[0].id)
        seed_annotations(db, videos[0].id)
        db.commit()


if __name__ == "__main__":
    main()
