from datetime import date, timedelta
import pytest

from models import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=today),
        OrderLine("order-123", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(line)

    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line("ELEGENT-LAMP", 20, 2)

    assert batch.can_allocate(line)

def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 20)

    assert batch.can_allocate(line) is False

def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_dont_match():
    batch = Batch("batch-001", "ELEGANT-LAMP", 20, eta=today)
    line = OrderLine("order-123", "BLUE-CUSHION", 3)

    assert batch.can_allocate(line) is False

def test_can_only_deallocated_allocated_lines():
    batch, line = make_batch_and_line("DECORATIVE_TRINKET", 20, 2)
    batch.deallocate(line)

    assert batch.available_quantity == 20

# def test_prefers_warehouse_batches_to_shipments():
#     pytest.fail("todo")

# def test_prefers_earlier_batches():
#     pytest.fail("todo")


