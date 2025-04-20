from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association tables
track_artist = Table(
    'track_artist', Base.metadata,
    Column('track_id', String, ForeignKey('track.id')),
    Column('artist_id', String, ForeignKey('artist.id'))
)

album_artist = Table(
    'album_artist', Base.metadata,
    Column('album_id', String, ForeignKey('album.id')),
    Column('artist_id', String, ForeignKey('artist.id'))
)

playlist_track = Table(
    'playlist_track', Base.metadata,
    Column('playlist_id', String, ForeignKey('playlist.id')),
    Column('track_id', String, ForeignKey('track.id'))
)

artist_genre = Table(
    'artist_genre', Base.metadata,
    Column('artist_id', String, ForeignKey('artist.id')),
    Column('genre_name', String, ForeignKey('genre.name'))
)

class ArtistORM(Base):
    __tablename__ = 'artist'
    id = Column(String, primary_key=True)
    name = Column(String)
    image = Column(String)
    genres = relationship("GenreORM", secondary=artist_genre, back_populates="artists")
    albums = relationship("AlbumORM", secondary=album_artist, back_populates="artists")
    tracks = relationship("TrackORM", secondary=track_artist, back_populates="artists")

class GenreORM(Base):
    __tablename__ = 'genre'
    name = Column(String, primary_key=True)
    artists = relationship("ArtistORM", secondary=artist_genre, back_populates="genres")

class AlbumORM(Base):
    __tablename__ = 'album'
    id = Column(String, primary_key=True)
    title = Column(String)
    release_year = Column(String)
    image = Column(String)
    artists = relationship("ArtistORM", secondary=album_artist, back_populates="albums")
    tracks = relationship("TrackORM", back_populates="album")

class TrackORM(Base):
    __tablename__ = 'track'
    id = Column(String, primary_key=True)
    title = Column(String)
    duration = Column(Integer)
    url = Column(String)
    album_id = Column(String, ForeignKey('album.id'))
    album = relationship("AlbumORM", back_populates="tracks")
    artists = relationship("ArtistORM", secondary=track_artist, back_populates="tracks")
    playlists = relationship("PlaylistORM", secondary=playlist_track, back_populates="tracks")

class PlaylistORM(Base):
    __tablename__ = 'playlist'
    id = Column(String, primary_key=True)
    name = Column(String)
    user_id = Column(String, ForeignKey('user.id'))
    user = relationship("UserORM", back_populates="playlists")
    tracks = relationship("TrackORM", secondary=playlist_track, back_populates="playlists")

class UserORM(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    display_name = Column(String)
    photo = Column(String)
    uri = Column(String)
    playlists = relationship("PlaylistORM", back_populates="user", cascade="all, delete-orphan")