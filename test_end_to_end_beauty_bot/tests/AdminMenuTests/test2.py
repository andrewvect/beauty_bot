from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker


def clear_data(engine):
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get a list of all tables in the database
    metadata = MetaData(bind=engine)
    metadata.reflect()
    all_tables = metadata.sorted_tables

    try:
        # Iterate over each table and delete data
        for table in all_tables:
            session.execute(table.delete())

        # Commit the changes
        session.commit()
    finally:
        # Close the session
        session.close()
