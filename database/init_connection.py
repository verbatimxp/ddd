import sqlalchemy as sa
from .settings_db import DATABASE

class Database:
    connection = sa.create_engine(f'postgresql://{DATABASE["user"]}:{DATABASE["password"]}@{DATABASE["db_host"]}:'
                                  f'{DATABASE["db_port"]}/{DATABASE["db_name"]}').connect()

    @classmethod
    def save_data_timer_start(cls ,date_start, ):
        cls.connection.execute(
            f"""INSERT INTO timer_log(date_start) VALUES('{date_start}')""")
    @classmethod
    def save_data_timer_end(cls,date_end):
        cls.connection.execute(
            f"""INSERT INTO timer_log(date_end) VALUES('{date_end}')""")

