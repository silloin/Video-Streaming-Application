import datetime

class User:
    @staticmethod
    def create(name, email, password_hash):
        return {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.datetime.utcnow()
        }

class Video:
    @staticmethod
    def create(title, description, youtube_id, thumbnail_url, is_active=True):
        return {
            "title": title,
            "description": description,
            "youtube_id": youtube_id,
            "thumbnail_url": thumbnail_url,
            "is_active": is_active,
            "created_at": datetime.datetime.utcnow()
        }
