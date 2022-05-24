import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as sapg
from app.schemas.base import Base

unix_now = sa.text("(date_part('epoch'::text, now()) * (1000)::double precision)")


class DimLocation(Base):
    __tablename__ = 'DIM_LOCATION'

    dim_location_id = sa.Column(
        sapg.UUID(),
        primary_key=True,
        nullable=False,
    )
    transactionid = sa.Column(sa.BigInteger())
    originairportcode = sa.Column(sa.String())
    origairportname = sa.Column(sa.String())
    origincityname = sa.Column(sa.String())
    originstate = sa.Column(sa.String())
    originstatename = sa.Column(sa.String())
    destairportcode = sa.Column(sa.String())
    destairportname = sa.Column(sa.String())
    destcityname = sa.Column(sa.String())
    deststate = sa.Column(sa.String())
    deststatename = sa.Column(sa.String())
    updated_at = sa.Column(sa.BigInteger, server_default=unix_now)
    created_at = sa.Column(sa.BigInteger, server_default=unix_now)
