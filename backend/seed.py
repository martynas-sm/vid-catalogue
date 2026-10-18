# use with: uv run python seed.py

from database import SessionLocal, engine
from models import Annotation, Catalog, User, Video
from models.base import Base


def seed_users(db):
    users_data = [
        {
            "username": "adomas",
            "email": "adomas@example.com",
            "hashed_password": "hashed_secret_password",
            "role": "admin",
        },
        {
            "username": "martynas",
            "email": "martynas@example.com",
            "hashed_password": "hashed_secret_password",
            "role": "member",
        },
    ]
    users = [User(**u) for u in users_data]
    db.add_all(users)
    db.flush()
    return users


def seed_catalogs(db, user_id):
    catalogs_data = [
        {
            "name": "Linear Algebra",
            "description": "Essence of linear algebra, determinants, and transformations.",
            "is_public": True,
            "user_id": user_id,
        },
        {
            "name": "Web Dev",
            "description": "Web protocols, JavaScript, and backend frameworks.",
            "is_public": True,
            "user_id": user_id,
        },
        {
            "name": "System Design",
            "description": "Distributed systems and scalable architecture.",
            "is_public": True,
            "user_id": user_id,
        },
        {
            "name": "DevOps",
            "description": "Docker containers, CI/CD, and deployment.",
            "is_public": True,
            "user_id": user_id,
        },
        {
            "name": "Mobile Dev",
            "description": "Flutter and cross-platform app development.",
            "is_public": True,
            "user_id": user_id,
        },
    ]
    catalogs = [Catalog(**c) for c in catalogs_data]
    db.add_all(catalogs)
    db.flush()
    return catalogs


def seed_videos(db, catalogs):
    cat_by_name = {c.name: c.id for c in catalogs}
    videos_data = [
        {
            "catalog_id": cat_by_name["Linear Algebra"],
            "title": "The determinant | Chapter 6, Essence of linear algebra",
            "url": "https://youtu.be/Ip3X9LOh2dk",
            "duration": 620.0,
            "description": "The determinant measures how much areas and volumes scale during a transformation.",
        },
        {
            "catalog_id": cat_by_name["Linear Algebra"],
            "title": "Cross products | Chapter 10, Essence of linear algebra",
            "url": "https://youtu.be/eu6i7WJeinw",
            "duration": 540.0,
            "description": "Geometric intuition behind 2D and 3D cross products and their relation to determinants.",
        },
        {
            "catalog_id": cat_by_name["Linear Algebra"],
            "title": "Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra",
            "url": "https://youtu.be/PFDu9oVAE-g",
            "duration": 1030.0,
            "description": "Visual understanding of eigenvectors as vectors that remain on their span during linear transformations.",
        },
        {
            "catalog_id": cat_by_name["Web Dev"],
            "title": "Web Development In 2022 - A Practical Guide",
            "url": "https://youtu.be/EqzUcMzfV1w",
            "duration": 5500.0,
            "description": "Comprehensive technology roadmap covering frontend, backend, databases, and APIs.",
        },
        {
            "catalog_id": cat_by_name["Web Dev"],
            "title": "Full HTTP Networking Course – Fetch and REST APIs in JavaScript",
            "url": "https://youtu.be/2JYT5f2isg4",
            "duration": 18500.0,
            "description": "Deep dive into the HTTP protocol, DNS, URLs, headers, and building web crawlers.",
        },
        {
            "catalog_id": cat_by_name["Web Dev"],
            "title": "Spring Boot & Spring Data JPA – Complete Course",
            "url": "https://youtu.be/5rNk7m_zlAg",
            "duration": 27300.0,
            "description": "Complete guide to building RESTful backend APIs with Spring Boot, Dependency Injection, and JPA.",
        },
        {
            "catalog_id": cat_by_name["Web Dev"],
            "title": "Every React Concept Explained in 12 Minutes",
            "url": "https://youtu.be/wIyHSOugGGw",
            "duration": 720.0,
            "description": "Quick breakdown of components, JSX, props, hooks, and state management in React.",
        },
    ]
    videos = [Video(**v) for v in videos_data]
    db.add_all(videos)
    db.flush()
    return videos


def seed_annotations(db, videos):
    vid_by_title = {v.title: v.id for v in videos}
    annotations_data = [
        {
            "video_id": vid_by_title[
                "The determinant | Chapter 6, Essence of linear algebra"
            ],
            "text": "Understanding determinants as scaling factors",
            "from_dur": 0.0,
            "to_dur": 159.0,
        },
        {
            "video_id": vid_by_title[
                "The determinant | Chapter 6, Essence of linear algebra"
            ],
            "text": "Interpreting 2D determinants and area scaling",
            "from_dur": 159.0,
            "to_dur": 222.0,
        },
        {
            "video_id": vid_by_title[
                "The determinant | Chapter 6, Essence of linear algebra"
            ],
            "text": "Negative determinants and orientation flipping",
            "from_dur": 222.0,
            "to_dur": 333.0,
        },
        {
            "video_id": vid_by_title[
                "The determinant | Chapter 6, Essence of linear algebra"
            ],
            "text": "Determinants in 3D: volume scaling",
            "from_dur": 333.0,
            "to_dur": 451.0,
        },
        {
            "video_id": vid_by_title[
                "Cross products | Chapter 10, Essence of linear algebra"
            ],
            "text": "2D cross products & parallelogram area",
            "from_dur": 0.0,
            "to_dur": 140.0,
        },
        {
            "video_id": vid_by_title[
                "Cross products | Chapter 10, Essence of linear algebra"
            ],
            "text": "Connecting cross products to determinants",
            "from_dur": 140.0,
            "to_dur": 298.0,
        },
        {
            "video_id": vid_by_title[
                "Cross products | Chapter 10, Essence of linear algebra"
            ],
            "text": "3D cross product geometry & right-hand rule",
            "from_dur": 298.0,
            "to_dur": 405.0,
        },
        {
            "video_id": vid_by_title[
                "Cross products | Chapter 10, Essence of linear algebra"
            ],
            "text": "3D computation trick via matrix determinant",
            "from_dur": 405.0,
            "to_dur": 540.0,
        },
        {
            "video_id": vid_by_title[
                "Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra"
            ],
            "text": "Introduction to eigenvectors and span",
            "from_dur": 0.0,
            "to_dur": 80.0,
        },
        {
            "video_id": vid_by_title[
                "Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra"
            ],
            "text": "Geometric interpretation of vectors staying on their span",
            "from_dur": 80.0,
            "to_dur": 179.0,
        },
        {
            "video_id": vid_by_title[
                "Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra"
            ],
            "text": "Eigenvalues defined as scaling factors",
            "from_dur": 179.0,
            "to_dur": 315.0,
        },
        {
            "video_id": vid_by_title[
                "Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra"
            ],
            "text": "Computing eigenvectors and characteristic polynomial",
            "from_dur": 315.0,
            "to_dur": 456.0,
        },
        {
            "video_id": vid_by_title["Web Development In 2022 - A Practical Guide"],
            "text": "Web developer career paths and core HTML/CSS tools",
            "from_dur": 234.0,
            "to_dur": 1103.0,
        },
        {
            "video_id": vid_by_title["Web Development In 2022 - A Practical Guide"],
            "text": "JavaScript fundamentals and language features",
            "from_dur": 1103.0,
            "to_dur": 1885.0,
        },
        {
            "video_id": vid_by_title["Web Development In 2022 - A Practical Guide"],
            "text": "Frontend frameworks overview (React, Vue, Angular)",
            "from_dur": 1885.0,
            "to_dur": 3111.0,
        },
        {
            "video_id": vid_by_title["Web Development In 2022 - A Practical Guide"],
            "text": "Backend web frameworks, databases, and REST APIs",
            "from_dur": 3400.0,
            "to_dur": 4230.0,
        },
        {
            "video_id": vid_by_title[
                "Full HTTP Networking Course – Fetch and REST APIs in JavaScript"
            ],
            "text": "Ch 1 - Why HTTP and protocol fundamentals",
            "from_dur": 212.0,
            "to_dur": 1651.0,
        },
        {
            "video_id": vid_by_title[
                "Full HTTP Networking Course – Fetch and REST APIs in JavaScript"
            ],
            "text": "Ch 2 - DNS lookup and domain resolution",
            "from_dur": 1651.0,
            "to_dur": 2891.0,
        },
        {
            "video_id": vid_by_title[
                "Full HTTP Networking Course – Fetch and REST APIs in JavaScript"
            ],
            "text": "Ch 3 - URIs, URLs, and path anatomy",
            "from_dur": 2891.0,
            "to_dur": 4581.0,
        },
        {
            "video_id": vid_by_title[
                "Full HTTP Networking Course – Fetch and REST APIs in JavaScript"
            ],
            "text": "Ch 8 - HTTP Methods and REST conventions",
            "from_dur": 9669.0,
            "to_dur": 11800.0,
        },
        {
            "video_id": vid_by_title["Spring Boot & Spring Data JPA – Complete Course"],
            "text": "Spring Boot fundamentals and bean management",
            "from_dur": 64.0,
            "to_dur": 4273.0,
        },
        {
            "video_id": vid_by_title["Spring Boot & Spring Data JPA – Complete Course"],
            "text": "Dependency Injection (DI) and inversion of control",
            "from_dur": 4273.0,
            "to_dur": 7031.0,
        },
        {
            "video_id": vid_by_title["Spring Boot & Spring Data JPA – Complete Course"],
            "text": "Spring REST controllers and endpoint mapping",
            "from_dur": 7031.0,
            "to_dur": 12008.0,
        },
        {
            "video_id": vid_by_title["Spring Boot & Spring Data JPA – Complete Course"],
            "text": "Spring Data JPA repositories and entity relations",
            "from_dur": 12008.0,
            "to_dur": 17298.0,
        },
        {
            "video_id": vid_by_title["Every React Concept Explained in 12 Minutes"],
            "text": "Components and JSX syntax basics",
            "from_dur": 11.0,
            "to_dur": 109.0,
        },
        {
            "video_id": vid_by_title["Every React Concept Explained in 12 Minutes"],
            "text": "Props, Children, and component composition",
            "from_dur": 109.0,
            "to_dur": 305.0,
        },
        {
            "video_id": vid_by_title["Every React Concept Explained in 12 Minutes"],
            "text": "State management and re-rendering flow",
            "from_dur": 305.0,
            "to_dur": 391.0,
        },
        {
            "video_id": vid_by_title["Every React Concept Explained in 12 Minutes"],
            "text": "Hooks and useEffect lifecycle handling",
            "from_dur": 391.0,
            "to_dur": 502.0,
        },
    ]
    annotations = [Annotation(**a) for a in annotations_data]
    db.add_all(annotations)
    db.flush()
    return annotations


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        users = seed_users(db)
        catalogs = seed_catalogs(db, users[0].id)
        videos = seed_videos(db, catalogs)
        seed_annotations(db, videos)
        db.commit()


if __name__ == "__main__":
    main()
