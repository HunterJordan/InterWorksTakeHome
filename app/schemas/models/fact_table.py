import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as sapg
from app.schemas.base import Base


unix_now = sa.text("(date_part('epoch'::text, now()) * (1000)::double precision)")


class FactFlights(Base):

    __tablename__ = 'FACT_FLIGHTS'

    fact_flights_id = sa.Column(
        sapg.UUID(),
        primary_key=True,
        nullable=False,
    )
    dim_location_id = sa.Column(sapg.UUID())
    dim_time_id = sa.Column(sapg.UUID())
    transactionid = sa.Column(sa.BigInteger())
    originairportcode = sa.Column(sa.VARCHAR())
    tailnum = sa.Column(sa.VARCHAR())
    flightnum = sa.Column(sa.SmallInteger())
    airlinecode = sa.Column(sa.String())
    airlinename = sa.Column(sa.String())
    canceled = sa.Column(sa.Boolean(), server_default='f')
    diverted = sa.Column(sa.Boolean(), server_default='f')
    distance = sa.Column(sa.VARCHAR())
    distancegroup = sa.Column(sa.String())
    depdelayg15 = sa.Column(sa.Boolean(), server_default='f')
    nextdayarr = sa.Column(sa.Boolean(), server_default='f')
    updated_at = sa.Column(sa.BigInteger, server_default=unix_now)
    created_at = sa.Column(sa.BigInteger, server_default=unix_now)

