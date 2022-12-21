import pandas as pd
import sqlalchemy

from sqlalchemy.engine import result
from sqlalchemy import create_engine, MetaData, \
    Table, Column, Numeric, Integer, VARCHAR, update
from config import Config as cfg

DB_CONNECTION_URL = "postgresql://%s:%s@%s:%s/%s" % \
                    (cfg.DB_USERNAME, cfg.DB_PASSWORD, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_NAME)


def create_state_table():
    incsv = 'data\\states.csv'
    df = pd.read_csv(incsv, dtype=str)

    # establish connections
    conn = create_engine(DB_CONNECTION_URL)

    # initialize the Metadata Object
    meta = MetaData(bind=conn)
    MetaData.reflect(meta)

    # create a table schema
    states = Table(
        'states', meta,
        Column('state_fips', VARCHAR, primary_key=True),
        Column('state_code', VARCHAR)
    )

    meta.create_all(conn)

    # insert records into the table
    for index, row in df.iterrows():
        val_code = row['code']
        val_name = row['name']
        print("Insert " + str(val_code) + " " + val_name)
        insert_command = states.insert().values(state_fips=val_code, state_code=val_name)

        # execute the insert records statement
        conn.execute(insert_command)

    conn.dispose()


def create_state_code_table():
    injson = 'data\\json\\statecodes.json'
    sf = pd.read_json(injson, typ='series')
    df = pd.DataFrame({'state_code': sf.index, 'state_name': sf.values})

    # establish connections
    conn = create_engine(DB_CONNECTION_URL)

    # initialize the Metadata Object
    meta = MetaData(bind=conn)
    MetaData.reflect(meta)

    # create a table schema
    statecodes = Table(
        'statecodes', meta,
        Column('state_code', VARCHAR, primary_key=True),
        Column('state_name', VARCHAR)
    )

    meta.create_all(conn)

    # insert records into the table
    for index, row in df.iterrows():
        val_code = row['state_code']
        val_name = row['state_name']
        print("Insert " + str(val_code) + " " + val_name)
        insert_command = statecodes.insert().values(state_code=val_code, state_name=val_name)

        # execute the insert records statement
        conn.execute(insert_command)

    conn.dispose()


def create_practice_table():
    incsv = 'data\\practices.csv'
    df = pd.read_csv(incsv)

    # establish connections
    conn = create_engine(DB_CONNECTION_URL)

    # initialize the Metadata Object
    meta = MetaData(bind=conn)
    MetaData.reflect(meta)

    # create a table schema
    practices = Table(
        'practices', meta,
        Column('practice_code', Integer, primary_key=True),
        Column('practice_name', VARCHAR)
    )

    meta.create_all(conn)

    # insert records into the table
    for i, row in df.iterrows():
        val_code = row['code']
        val_name = row['name']
        print("Insert " + str(val_code) + " " + val_name)

        insert_command = practices.insert().values(practice_code=val_code, practice_name=val_name)

        # execute the insert records statement
        conn.execute(insert_command)

    conn.dispose()


def create_category1_table():
    incsv = 'data\\category1.csv'
    df = pd.read_csv(incsv)

    # establish connections
    conn = create_engine(DB_CONNECTION_URL)

    # initialize the Metadata Object
    meta = MetaData(bind=conn)
    MetaData.reflect(meta)

    # create a table schema
    category1 = Table(
        'category1', meta,
        Column('category1_code', Integer, primary_key=True),
        Column('category1_name', VARCHAR)
    )

    meta.create_all(conn)

    # insert records into the table
    for i, row in df.iterrows():
        val_code = row['code']
        val_name = row['name']
        print("Insert " + str(val_code) + " " + val_name)

        insert_command = category1.insert().values(category1_code=val_code, category1_name=val_name)

        # execute the insert records statement
        conn.execute(insert_command)

    conn.dispose()


def separte_values_in_column():
    incsv = 'data\practices.csv'
    df = pd.read_csv(incsv)

    for i, row in df.iterrows():
        raw_string = row['practice_code']
        val_code = raw_string[:3]
        val_name = raw_string[4:]
        df.at[i, 'code'] = val_code
        df.at[i, 'name'] = val_name
        print("Insert " + str(val_code) + " " + val_name)

    df.to_csv('data\\test.csv', sep=',', encoding='utf-8')

if __name__ == '__main__':
    create_state_table()
    # create_state_code_table()
    # create_practice_table()
    # create_category1_table()
    # separte_values_in_column()