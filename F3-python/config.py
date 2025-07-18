class Config:
    JWT_SECRET_KEY = 'super-secret'
    JWT_TTL = 3600
    MONGO_URI = "mongodb://localhost:27017/"
    MONGO_DB_NAME = "fedicom3"
    SQLITE_DB_PATH = "fedicom3.db"
