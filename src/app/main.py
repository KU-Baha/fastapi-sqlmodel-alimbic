from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db import get_session
from app.models import Song, SongCreate, SongBase  # noqa

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [
        Song(
            id=song.id,
            name=song.name,
            artist=song.artist
        )
        for song in songs
    ]


@app.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(
        name=song.name,
        artist=song.artist
    )
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
