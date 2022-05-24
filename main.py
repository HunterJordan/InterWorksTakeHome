from app.data.wrangle import wrangle
from app import transactions
from app.config import database as setup
from app.utils import notify


def main():
    # prepare postgres connection and tables
    db = setup.get_db_connection()
    # Cleaning the data
    df = wrangle()
    # iterate some text and makes some rows
    transactions.add_rows(db, df)
    db.commit()
    notify("success")


if __name__ == '__main__':
    main()
