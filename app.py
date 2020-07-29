import pandas
import logging
import os
import config

import datetime
from sqlalchemy import create_engine, types, engine


def from_csv_to_db(service_db:str="",model_name: str = "", db_engine: engine.Engine = None):

    current_dir = os.getcwd()

    data_frame = pandas.read_csv(
        f'{current_dir}/csv/{service_db}/{model_name}.csv', sep=';')

    data_frame.columns = [column.lower() for column in data_frame.columns]

    data_frame["created_at"] = datetime.datetime.now()
    data_frame["updated_at"] = datetime.datetime.now()

    data_frame.to_sql(
        model_name,
        db_engine,
        if_exists='append',  # options are ‘fail’, ‘replace’, ‘append’, default ‘fail’
        index=False,
        index_label="id",
    )


def iterate_csv_dir(db_engine: engine.Engine = None):

    current_dir = os.getcwd()
    db_config = config.DB()

    for _, services_dir, _ in os.walk(f'{current_dir}/csv'):
        for service_db in services_dir:
            db_engine = create_engine(db_config.print())

            db_connection = db_engine.raw_connection()

            try:
                db_cursor = db_connection.cursor()
                db_cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{service_db}'")
                db_exists = db_cursor.fetchone()
                if not db_exists:
                    db_cursor.execute(f'CREATE DATABASE {service_db}')
                db_cursor.close()
                db_connection.commit()

            finally:
                db_connection.close()
                db_engine.dispose()
            
            db_engine = create_engine(db_config.print(service_db))

            for filename in os.listdir(f'{current_dir}/csv/{service_db}'):
                filename = os.path.splitext(filename)[0]
                from_csv_to_db(service_db, filename, db_engine)

            db_engine.dispose()


def main():
    db_config = config.DB()
    db_engine = create_engine(db_config.print())

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    iterate_csv_dir(db_engine)
    
    return


if __name__ == "__main__":
    main()
