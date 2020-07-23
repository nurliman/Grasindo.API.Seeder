import pandas
import logging
import os
import config


from sqlalchemy import create_engine, types, engine


def seeds(model_name: str = "", db_engine: engine.Engine = None):

    current_dir = os.getcwd()

    data_frame = pandas.read_csv(f'{current_dir}/csv/{model_name}.csv', sep=';')

    data_frame.columns = [column.lower() for column in data_frame.columns]

    data_frame.to_sql(
        model_name,
        db_engine,
        if_exists='append',  # options are ‘fail’, ‘replace’, ‘append’, default ‘fail’
        index=False,
        index_label="id",
    )


def main():
    db_config = config.DB()
    db_engine = create_engine(db_config.print())

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    current_dir = os.getcwd()

    for filename in os.listdir(f'{current_dir}/csv'):
        filename = os.path.splitext(filename)[0]
        seeds(filename,db_engine)
    
    db_engine.dispose()
    return


if __name__ == "__main__":
    main()
