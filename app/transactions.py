import uuid

from app.schemas.base import FactFlights, DimLocation, DimTime
from app.utils import notify


def filter_invalid_keys(model, payload):
    model_keys = {k: k for k in dir(model) if not k.startswith('_')}
    return {k.lower(): v for k, v in payload.items() if k.lower() in model_keys}


def add_rows(db, df):
    notify('wrench', f'Preparing rows to be added to db')
    rows_to_be_added = []

    for idx, row in df.iterrows():
        row_dict = {
            **row.to_dict(),
            'dim_location_id': uuid.uuid4().hex,
            'dim_time_id': uuid.uuid4().hex,
            'fact_flights_id': uuid.uuid4().hex,

        }
        for model in [DimLocation, DimTime, FactFlights]:
            rows_to_be_added.append(
                model(
                    **filter_invalid_keys(
                        model,
                        row_dict
                    )
                )

            )
    db.add_all(rows_to_be_added)
    notify('praise', f'Successfully added {len(rows_to_be_added)} rows to transaction')
