import asyncio
import argparse
import random
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, Base, engine
from app.models import (
    User,
    Source,
    Quote,
    Tag,
    Bookmark,
    BookmarkFolder,
    Book,
    Movie,
    Drama,
    Producer,
)
from app.models.quote_tag import quote_tags
from app.schemas import (
    UserCreate,
    SourceCreate,
    QuoteCreate,
    TagCreate,
    BookmarkFolderCreate,
    BookmarkCreate,
    BookCreate,
    MovieCreate,
    DramaCreate,
    ProducerCreate,
)
from app.core.auth import hash_password


async def wipe_database(db: AsyncSession):
    """Drops and recreates all tables in the database."""
    print("Wiping database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database wiped.")


async def seed_data(db: AsyncSession):
    """Populates the database with a rich set of dummy data."""
    # --- Create Users ---
    users_in = [
        UserCreate(
            email=f"user{i}@example.com", username=f"user{i}", password="password123"
        )
        for i in range(1, 21)
    ]  # 20 users
    users = [
        User(
            email=u.email,
            username=u.username,
            hashed_password=hash_password(u.password),
        )
        for u in users_in
    ]
    db.add_all(users)
    await db.flush()
    user_ids = [user.id for user in users]
    await db.commit()
    print(f"Created {len(users)} users.")

    # --- Create Producers (for Dramas) ---
    producer_names = [
        "HBO",
        "Netflix",
        "Amazon Prime",
        "Disney+",
        "Apple TV+",
        "BBC",
        "ITV",
        "Channel 4",
        "AMC",
        "FX",
    ]
    producers_in = [
        ProducerCreate(name=name, pd_type="broadcast") for name in producer_names
    ]
    producers = [Producer(**p.model_dump()) for p in producers_in]
    db.add_all(producers)
    await db.flush()
    producer_ids = [p.id for p in producers]
    await db.commit()
    print(f"Created {len(producers)} producers.")

    # --- Create Detailed Sources and Generic Sources ---
    all_sources = []

    # Books
    books = []
    for i in range(1, 11):  # 10 books
        book = Book(
            title=f"Book Title {i}", author=f"Author {i}", isbn=f"978-123456789{i:02d}"
        )
        books.append(book)
    db.add_all(books)
    await db.flush()
    for book in books:
        all_sources.append(
            Source(
                title=book.title,
                source_type="book",
                creator=book.author,
                details_id=book.id,
            )
        )

    # Movies
    movies = []
    for i in range(1, 11):  # 10 movies
        movie = Movie(
            title=f"Movie Title {i}",
            director=f"Director {i}",
            release_date=f"20{10 + i % 10}-01-01",
        )  # Corrected date generation
        movies.append(movie)
    db.add_all(movies)
    await db.flush()
    for movie in movies:
        all_sources.append(
            Source(
                title=movie.title,
                source_type="movie",
                creator=movie.director,
                details_id=movie.id,
            )
        )

    # Dramas
    dramas = []
    for i in range(1, 11):  # 10 dramas
        drama = Drama(
            title=f"Drama Title {i}",
            producer_id=random.choice(producer_ids),
            release_date=f"20{10 + i % 10}-01-01",
        )  # Corrected date generation
        dramas.append(drama)
    db.add_all(dramas)
    await db.flush()
    for drama in dramas:
        all_sources.append(
            Source(
                title=drama.title,
                source_type="tv",
                creator=f"Creator {drama.id}",
                details_id=drama.id,
            )
        )

    db.add_all(all_sources)
    await db.flush()

    book_source_ids = [s.id for s in all_sources if s.source_type == "book"]
    movie_source_ids = [s.id for s in all_sources if s.source_type == "movie"]
    drama_source_ids = [s.id for s in all_sources if s.source_type == "tv"]

    await db.commit()
    print(f"Created {len(all_sources)} sources with details.")

    # --- Create Tags ---
    tag_names = [
        "sci-fi",
        "fantasy",
        "dystopian",
        "action",
        "drama",
        "crime",
        "comedy",
        "thriller",
        "romance",
        "horror",
        "adventure",
        "mystery",
        "biography",
        "history",
        "philosophy",
        "self-help",
        "science",
        "technology",
        "art",
        "music",
    ]
    tags_in = [TagCreate(name=name) for name in tag_names]
    tags = [Tag(**t.model_dump()) for t in tags_in]
    db.add_all(tags)
    await db.flush()
    tag_ids = [tag.id for tag in tags]
    await db.commit()
    print(f"Created {len(tags)} tags.")

    # --- Create Quotes ---
    quotes_in = []
    # Create 20 quotes from books
    for i in range(20):
        quotes_in.append(
            QuoteCreate(
                user_id=random.choice(user_ids),
                source_id=random.choice(book_source_ids),
                content=f"This is a sample quote from a book, number {i+1}.",
            )
        )
    # Create 20 quotes from movies
    for i in range(20):
        quotes_in.append(
            QuoteCreate(
                user_id=random.choice(user_ids),
                source_id=random.choice(movie_source_ids),
                content=f"This is a sample quote from a movie, number {i+1}.",
            )
        )
    # Create 10 quotes from dramas
    for i in range(10):
        quotes_in.append(
            QuoteCreate(
                user_id=random.choice(user_ids),
                source_id=random.choice(drama_source_ids),
                content=f"This is a sample quote from a drama, number {i+1}.",
            )
        )

    quotes = [Quote(**q.model_dump()) for q in quotes_in]
    db.add_all(quotes)
    await db.flush()
    quote_ids = [quote.id for quote in quotes]
    await db.commit()
    print(f"Created {len(quotes)} quotes.")

    # --- Associate Tags with Quotes (Many-to-Many) ---
    associations = []
    for quote_id in quote_ids:
        num_tags = random.randint(1, 3)  # Each quote gets 1 to 3 tags
        selected_tag_ids = random.sample(tag_ids, num_tags)
        for tag_id in selected_tag_ids:
            associations.append({"quote_id": quote_id, "tag_id": tag_id})
    await db.execute(quote_tags.insert().values(associations))
    await db.commit()
    print("Created quote-tag associations.")

    # --- Create Bookmark Folders ---
    folders_in = []
    for i in range(10):  # 10 folders
        folders_in.append(
            BookmarkFolderCreate(name=f"Folder {i+1}", user_id=random.choice(user_ids))
        )
    folders = [BookmarkFolder(**f.model_dump()) for f in folders_in]
    db.add_all(folders)
    await db.flush()
    folder_ids = [folder.id for folder in folders]
    await db.commit()
    print(f"Created {len(folders)} bookmark folders.")

    # --- Create Bookmarks (Many-to-Many) ---
    bookmarks_in = []
    for i in range(20):  # 20 bookmarks
        user_id = random.choice(user_ids)
        quote_id = random.choice(quote_ids)
        folder_id = (
            random.choice(folder_ids) if random.random() > 0.3 else None
        )  # Some bookmarks without folders
        bookmarks_in.append(
            BookmarkCreate(user_id=user_id, quote_id=quote_id, folder_id=folder_id)
        )
    bookmarks = [Bookmark(**b.model_dump()) for b in bookmarks_in]
    db.add_all(bookmarks)
    await db.commit()
    print(f"Created {len(bookmarks)} bookmarks.")


async def main():
    parser = argparse.ArgumentParser(description="Database seeding and wiping utility.")
    parser.add_argument(
        "--wipe", action="store_true", help="Wipe all data from the database."
    )
    parser.add_argument(
        "--seed", action="store_true", help="Seed the database with dummy data."
    )
    args = parser.parse_args()

    async with AsyncSessionLocal() as db:
        if args.wipe:
            print("WARNING: This will permanently delete all data in the database.")
            confirm = input("Type 'yes' to continue: ")
            if confirm.lower() == "yes":
                await wipe_database(db)
            else:
                print("Wipe operation cancelled.")

        if args.seed:
            # When seeding, we wipe first to ensure a clean state
            await wipe_database(db)
            await seed_data(db)
            print("Data seeding complete.")

        if not args.wipe and not args.seed:
            print("Please specify an action: --wipe or --seed")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
