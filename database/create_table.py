import sqlalchemy as sa
from settings_db import DATABASE

TABLE_TIMER_NAME_START = 'timer_log'

engine = sa.create_engine(
    f'postgresql://{DATABASE["user"]}:{DATABASE["password"]}@{DATABASE["db_host"]}:{DATABASE["db_port"]}/{DATABASE["db_name"]}'
)

meta = sa.MetaData()
if TABLE_TIMER_NAME_START not in engine.table_names():
    timer_stats = sa.Table(
        TABLE_TIMER_NAME_START, meta,
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('date_start', sa.DateTime, nullable=True),
        sa.Column('date_end', sa.DateTime, nullable=True),

    )

    meta.create_all(engine)
