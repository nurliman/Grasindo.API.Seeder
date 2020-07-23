import pandas
import logging
import os
import config


from sqlalchemy import create_engine, types, engine


def seeds(model_name: str = "", db_engine: engine.Engine = None):

    data_frame = pandas.read_csv(f'./csv/{model_name}.csv')

    data_frame.columns = [column.lower() for column in data_frame.columns]

    data_frame.to_sql(
        model_name,
        db_engine,
        if_exists='replace',  # options are ‘fail’, ‘replace’, ‘append’, default ‘fail’
    )


def main():
    db_config = config.DB()
    db_engine = create_engine(db_config.print())

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    current_dir = os.getcwd()

    for filename in os.listdir(current_dir):
        filename = os.path.splitext(filename)[0]
        seeds(filename,db_engine)
    
    return


if __name__ == "__main__":
    main()
