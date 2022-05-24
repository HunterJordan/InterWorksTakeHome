import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as sapg
from app.schemas.base import Base

unix_now = sa.text("(date_part('epoch'::text, now()) * (1000)::double precision)")


class DimTime(Base):
    __tablename__ = 'DIM_TIME'

    dim_time_id = sa.Column(
        sapg.UUID(),
        primary_key=True,
        nullable=False,
    )
    transactionid = sa.Column(sa.BigInteger())
    flightdate = sa.Column(sa.DateTime())
    crsdeptime = sa.Column(sa.Time())
    deptime = sa.Column(sa.Time())
    depdelay = sa.Column(sa.SmallInteger())
    crsarrtime = sa.Column(sa.Time())
    arrtime = sa.Column(sa.Time())
    arrdelay = sa.Column(sa.SmallInteger())
    crselapsedtime = sa.Column(sa.SmallInteger())
    actualelapsedtime = sa.Column(sa.SmallInteger())
    wheelsoff = sa.Column(sa.Time())
    wheelson = sa.Column(sa.Time())
    taxiin = sa.Column(sa.SmallInteger())
    taxiout = sa.Column(sa.SmallInteger())
    updated_at = sa.Column(sa.BigInteger, server_default=unix_now)
    created_at = sa.Column(sa.BigInteger, server_default=unix_now)
