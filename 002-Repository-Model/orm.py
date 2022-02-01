from importlib_metadata import metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, relationship

import models

## Goal here is to define the schema separately from the models
## Keeping domain model separate from infrastructure concerns and dependencies

metadata = Metadata()


order_lines = Table(
    "order_lines", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255))
)

# This will map the table schema to the domain model
def start_mappers():
    lines_mapper = mapper(models.OrderLine, order_lines)

