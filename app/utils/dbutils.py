import json

import pandas as pd
import sqlalchemy

from sqlalchemy.engine import result
from sqlalchemy import create_engine, MetaData, \
    Table, Column, Numeric, Integer, VARCHAR, update, insert
from config import Config as cfg

DB_CONNECTION_URL = "postgresql://%s:%s@%s:%s/%s" % \
                    (cfg.DB_USERNAME, cfg.DB_PASSWORD, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_NAME)


def create_table_test():
    incsv = 'data\\states.csv'
    df = pd.read_csv(incsv, dtype=str)

    from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
    engine = create_engine(DB_CONNECTION_URL, echo=False)
    meta = MetaData()
    #
    # # create a table schema
    states = Table(
        'test', meta,
        Column('state_fips', VARCHAR, primary_key=True),
        Column('state_code', VARCHAR)
    )
    # meta.create_all(engine)

    # insert records into the table
    with engine.connect() as conn:
        for index, row in df.iterrows():
            val_code = row['code']
            val_name = row['name']
            print("Insert " + str(val_code) + " " + val_name)
            # insert_command = states.insert().values(state_fips=val_code, state_code=val_name)
            insert_command = insert(states).values(state_fips=str(index), state_code="code")
            # conn.execute(states.insert(), state_fips=val_code, state_code=val_name)

            # execute the insert records statement
            test = conn.execute(insert_command)
            print(test)

def create_table_from_csv(tablename, incsv):
    print("Creating table " + tablename + " from " + incsv)
    engine = create_engine(DB_CONNECTION_URL, echo=False)
    df = pd.read_csv(incsv)

    # Write data into the table in sqllite database
    df.to_sql(tablename, engine)


def create_table_from_json(tablename, injson_path):
    with open(injson_path) as injson:
        read_json = injson.read()

    print(read_json)

    outjson = json.loads(read_json)

    df = pd.DataFrame.from_dict(data=outjson, orient='index').T

    engine = create_engine(DB_CONNECTION_URL, echo=False)

    # Write data into the table in sqllite database
    df.to_sql(tablename, engine)


def create_table_from_json_list(tablename, injson_list):
    df_total = pd.DataFrame()
    for injson in injson_list:
        df = pd.DataFrame.from_dict(data=injson, orient='index').T
        df_total = df_total.append(df)


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
    incsv = 'data\\practices.csv'
    df = pd.read_csv(incsv)

    for i, row in df.iterrows():
        raw_string = row['practice_code']
        val_code = raw_string[:3]
        val_name = raw_string[4:]
        df.at[i, 'code'] = val_code
        df.at[i, 'name'] = val_name
        print("Insert " + str(val_code) + " " + val_name)

    df.to_csv('data\\test.csv', sep=',', encoding='utf-8')


def create_summary_table():
    incsv = 'data\\summary.csv'
    df = pd.read_csv(incsv)

    # establish connections
    conn = create_engine(DB_CONNECTION_URL)

    # initialize the Metadata Object
    meta = MetaData(bind=conn)
    MetaData.reflect(meta)

    # create a table schema
    states = Table(
        'summary', meta,
        Column('summary_code', Integer, primary_key=True),
        Column('title', VARCHAR),
        Column('state', VARCHAR),
        Column('fiscal_year', Integer),
        Column('amount', VARCHAR)
    )

    meta.create_all(conn)

    # insert records into the table
    for index, row in df.iterrows():
        val_title = row['Title']
        val_state = row['State']
        val_fiscal_year = row['FiscalYear']
        val_amount = row['Amount']
        print("Insert " + val_title + " " + val_state + " " + str(val_fiscal_year))
        insert_command = states.insert().values(
            title=val_title, state=val_state, fiscal_year=val_fiscal_year, amount=val_amount)

        # execute the insert records statement
        conn.execute(insert_command)

    conn.dispose()


def create_allprograms_table():
    incsv = 'data\\allprograms.csv'
    df = pd.read_csv(incsv)

    # establish connections
    conn = create_engine(DB_CONNECTION_URL)

    # initialize the Metadata Object
    meta = MetaData(bind=conn)
    MetaData.reflect(meta)

    # create a table schema
    states = Table(
        'allprograms', meta,
        Column('all_program_code', Integer, primary_key=True),
        Column('state', VARCHAR),
        Column('crop_ins_2018', Numeric),
        Column('crop_ins_2019', Numeric),
        Column('crop_ins_2020', Numeric),
        Column('crop_ins_2021', Numeric),
        Column('crop_ins_2022', Numeric),
        Column('crop_ins_total', Numeric),
        Column('snap_2018', Numeric),
        Column('snap_2019', Numeric),
        Column('snap_2020', Numeric),
        Column('snap_2021', Numeric),
        Column('snap_2022', Numeric),
        Column('snap_total', Numeric),
        Column('title_1_2018', Numeric),
        Column('title_1_2019', Numeric),
        Column('title_1_2020', Numeric),
        Column('title_1_2021', Numeric),
        Column('title_1_2022', Numeric),
        Column('title_1_total', Numeric),
        Column('title_2_2018', Numeric),
        Column('title_2_2019', Numeric),
        Column('title_2_2020', Numeric),
        Column('title_2_2021', Numeric),
        Column('title_2_2022', Numeric),
        Column('title_2_total', Numeric),
        Column('all_programs_total_2018', Numeric),
        Column('all_programs_total_2019', Numeric),
        Column('all_programs_total_2020', Numeric),
        Column('all_programs_total_2021', Numeric),
        Column('all_programs_total_2022', Numeric),
        Column('all_programs_total_18_22', Numeric)
    )

    meta.create_all(conn)

    # insert records into the table
    for index, row in df.iterrows():
        val_state = row['State']
        val_ci18 = row['Crop Insurance 2018']
        val_ci19 = row['Crop Insurance 2019']
        val_ci20 = row['Crop Insurance 2020']
        val_ci21 = row['Crop Insurance 2021']
        val_ci22 = row['Crop Insurance 2022']
        val_citotal = row['Crop Insurance Total']
        val_snap18 = row['SNAP 2018']
        val_snap19 = row['SNAP 2019']
        val_snap20 = row['SNAP 2020']
        val_snap21 = row['SNAP 2021']
        val_snap22 = row['SNAP 2022']
        val_snaptotal = row['SNAP Total']
        val_t118 = row['Title I 2018']
        val_t119 = row['Title I 2019']
        val_t120 = row['Title I 2020']
        val_t121 = row['Title I 2021']
        val_t122 = row['Title I 2022']
        val_t1total = row['Title I Total']
        val_t218 = row['Title II 2018']
        val_t219 = row['Title II 2019']
        val_t220 = row['Title II 2020']
        val_t221 = row['Title II 2021']
        val_t222 = row['Title II 2022']
        val_t2total = row['Title II Total']
        val_all18 = row['2018 All Programs Total']
        val_all19 = row['2019 All Programs Total']
        val_all20 = row['2020 All Programs Total']
        val_all21 = row['2021 All Programs Total']
        val_all22 = row['2022 All Programs Total']
        val_alltotal = row['18-22 All Programs Total']
        print("Insert " + val_state)
        insert_command = states.insert().values(
            state=val_state,
            crop_ins_2018=val_ci18, crop_ins_2019=val_ci19, crop_ins_2020=val_ci20, crop_ins_2021=val_ci21,
            crop_ins_2022=val_ci22, crop_ins_total=val_citotal,
            snap_2018=val_snap18, snap_2019=val_snap19, snap_2020=val_snap20, snap_2021=val_snap21,
            snap_2022=val_snap22, snap_total=val_snaptotal,
            title_1_2018=val_t118, title_1_2019=val_t119, title_1_2020=val_t120, title_1_2021=val_t121,
            title_1_2022=val_t122, title_1_total=val_t1total,
            title_2_2018=val_t118, title_2_2019=val_t119, title_2_2020=val_t120, title_2_2021=val_t121,
            title_2_2022=val_t122, title_2_total=val_t1total,
            all_programs_total_2018=val_all18, all_programs_total_2019=val_all19, all_programs_total_2020=val_all20,
            all_programs_total_2021=val_all21, all_programs_total_2022=val_all22, all_programs_total_18_22=val_alltotal
        )

        # execute the insert records statement
        conn.execute(insert_command)

    conn.dispose()


if __name__ == '__main__':
    # create_state_table()
    # create_state_code_table()
    # create_practice_table()
    # create_category1_table()
    # separte_values_in_column()
    # create_allprograms_table()
    # create_summary_table()
    create_table_test()
    # tablename = 'test'
    # incsv = 'data\\allprograms.csv'
    # create_table_from_csv(tablename, incsv)
    # injson = 'data\\json\\EQIP_MAP_DATA.json'
    # create_table_from_json(tablename, injson)
    # create_table_from_json_list(tablename, injson_list)
