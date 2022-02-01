import pytest

import models

def test_orderline_mapper_can_load_lines(session):
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES '
        '("order1", "RED-CHAIR", 12),'
        '("order2", "RED-TABLE", 13),'
        '("order3", "BLUE-LIPSTICK",14)'
    )
    expected = [
        models.OrderLine("order1", "RED-CHAIR", 12),
        models.OrderLine("order2", "RED-TABLE", 13),
        models.OrderLine("order3", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(models.OrderLine).all() == expected