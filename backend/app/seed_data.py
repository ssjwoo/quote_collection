import asyncio
import argparse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, Base, engine
from app.models import User, Source, Quote, Tag, Bookmark, BookmarkFolder, Book, Movie, Drama, Producer
from app.models.quote_tag import quote_tags
from app.schemas import UserCreate, SourceCreate, QuoteCreate, TagCreate, BookmarkFolderCreate, BookmarkCreate, BookCreate, MovieCreate, DramaCreate, ProducerCreate
from app.core.auth import hash_password

async def wipe_database():
    """Drops and recreates all tables in the database."""
    print("Wiping database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database wiped.")

async def seed_data():
    """Populates the database with a rich set of dummy data."""
    async with AsyncSessionLocal() as db:
        # --- Create Users ---
        users_in = [UserCreate(email=f"user{i}@example.com", username=f"user{i}", password="password123") for i in range(1, 6)]
        users = [User(email=u.email, username=u.username, hashed_password=hash_password(u.password)) for u in users_in]
        db.add_all(users)
        await db.flush()
        user_ids = [user.id for user in users]
        await db.commit()
        print(f"Created {len(users)} users.")

        # --- Create Producers (for Dramas) ---
        producers_in = [ProducerCreate(name="HBO", pd_type="broadcast")]
        producers = [Producer(**p.model_dump()) for p in producers_in]
        db.add_all(producers)
        await db.flush()
        producer_ids = [p.id for p in producers]
        await db.commit()
        print(f"Created {len(producers)} producers.")

        # --- Create Detailed Sources and Generic Sources ---
        # Books
        book1 = Book(title="Dune", author="Frank Herbert", isbn="978-0441013593")
        db.add(book1)
        await db.flush()
        source1 = Source(title=book1.title, source_type="book", creator=book1.author, details_id=book1.id)
        
        # Movies
        movie1 = Movie(title="The Matrix", director="The Wachowskis", release_date="1999-03-31")
        db.add(movie1)
        await db.flush()
        source2 = Source(title=movie1.title, source_type="movie", creator=movie1.director, details_id=movie1.id)

        # Dramas
        drama1 = Drama(title="Breaking Bad", producer_id=producer_ids[0], release_date="2008-01-20")
        db.add(drama1)
        await db.flush()
        source3 = Source(title=drama1.title, source_type="tv", creator="Vince Gilligan", details_id=drama1.id)

        db.add_all([source1, source2, source3])
        await db.flush()
        source_ids = [source1.id, source2.id, source3.id]
        await db.commit()
        print(f"Created {len(source_ids)} sources with details.")

        # --- Create Tags ---
        tags_in = [TagCreate(name=name) for name in ["sci-fi", "fantasy", "dystopian", "action", "drama", "crime"]]
        tags = [Tag(**t.model_dump()) for t in tags_in]
        db.add_all(tags)
        await db.flush()
        tag_ids = [tag.id for tag in tags]
        await db.commit()
        print(f"Created {len(tags)} tags.")

        # --- Create Quotes ---
        quotes_in = [
            QuoteCreate(user_id=user_ids[0], source_id=source_ids[0], content="I must not fear. Fear is the mind-killer."),
            QuoteCreate(user_id=user_ids[2], source_id=source_ids[1], content="There is no spoon."),
            QuoteCreate(user_id=user_ids[4], source_id=source_ids[2], content="I am the one who knocks."),
        ]
        quotes = [Quote(**q.model_dump()) for q in quotes_in]
        db.add_all(quotes)
        await db.flush()
        quote_ids = [quote.id for quote in quotes]
        await db.commit()
        print(f"Created {len(quotes)} quotes.")

        # --- Associate Tags with Quotes (Many-to-Many) ---
        associations = [
            {'quote_id': quote_ids[0], 'tag_id': tag_ids[0]},
            {'quote_id': quote_ids[1], 'tag_id': tag_ids[0]},
            {'quote_id': quote_ids[1], 'tag_id': tag_ids[3]},
            {'quote_id': quote_ids[2], 'tag_id': tag_ids[4]},
            {'quote_id': quote_ids[2], 'tag_id': tag_ids[5]},
        ]
        await db.execute(quote_tags.insert().values(associations))
        await db.commit()
        print("Created quote-tag associations.")

        # --- Create Bookmark Folders ---
        folders_in = [
            BookmarkFolderCreate(name="Sci-Fi Favorites", user_id=user_ids[0]),
            BookmarkFolderCreate(name="Must Watch", user_id=user_ids[4]),
        ]
        folders = [BookmarkFolder(**f.model_dump()) for f in folders_in]
        db.add_all(folders)
        await db.flush()
        folder_ids = [folder.id for folder in folders]
        await db.commit()
        print(f"Created {len(folders)} bookmark folders.")

        # --- Create Bookmarks (Many-to-Many) ---
        bookmarks_in = [
            BookmarkCreate(user_id=user_ids[0], quote_id=quote_ids[0], folder_id=folder_ids[0]),
            BookmarkCreate(user_id=user_ids[1], quote_id=quote_ids[0]),
            BookmarkCreate(user_id=user_ids[2], quote_id=quote_ids[1]),
            BookmarkCreate(user_id=user_ids[4], quote_id=quote_ids[2], folder_id=folder_ids[1]),
        ]
        bookmarks = [Bookmark(**b.model_dump()) for b in bookmarks_in]
        db.add_all(bookmarks)
        await db.commit()
        print(f"Created {len(bookmarks)} bookmarks.")

async def main():
    parser = argparse.ArgumentParser(description="Database seeding and wiping utility.")
    parser.add_argument("--wipe", action="store_true", help="Wipe all data from the database.")
    parser.add_argument("--seed", action="store_true", help="Seed the database with dummy data.")
    args = parser.parse_args()

    if args.wipe:
        print("WARNING: This will permanently delete all data in the database.")
        confirm = input("Type 'yes' to continue: ")
        if confirm.lower() == 'yes':
            await wipe_database()
        else:
            print("Wipe operation cancelled.")
    
    if args.seed:
        # When seeding, we wipe first to ensure a clean state
        await wipe_database()
        await seed_data()
        print("Data seeding complete.")
    
    if not args.wipe and not args.seed:
        print("Please specify an action: --wipe or --seed")

if __name__ == "__main__":
    asyncio.run(main())
