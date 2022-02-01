from dataclasses import dataclass
from typing import List, Optional, NewType
from datetime import date


# Define types to aid in type safety
Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)

class OutOfStock(Exception):
    pass


# frozen=True makes this immutable
# dataclasses offer value equality, if all fields are equal, objects are equal
@dataclass(frozen=True) 
class OrderLine:
    orderid: str
    sku: Sku
    qty: Quantity

class Batch:
    def __init__(
        self, ref: Reference, sku: Sku, qty: Quantity, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set() # Set allocations to an empty set

    def __eq__(self, other):
        """Override the equal operator"""
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self):
        """Override the hash operator"""
        return hash(self.reference)

    def __gt__(self, other):
        """Override the gt operator for sorting"""
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def can_allocate(self, line: OrderLine) -> bool:
        """Evaluates whether an order line can be allocated against this batch.

        Args:
            line (OrderLine): Order line containing a sku and requested quantity

        Returns:
            bool: True if all conditions are met to fulfill order, False otherwise
        """
        return self.sku == line.sku and self.available_quantity >= line.qty

    def allocate(self, line: OrderLine) -> None:
        """Allocate an order on the current batch

        Args:
            line (OrderLine): Order line containing requested items
        """
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        """Deallocates a previously allocated OrderLine

        Args:
            line (OrderLine): allocated order line of which to deallocate
        """
        if line in self._allocations:
            self._allocations.remove(line)

    #@property becomes a calculated field in the classe
    @property
    def allocated_quantity(self) -> Quantity:
        """Current quantity allocated to orders

        Returns:
            int: number of items allocated
        """
        return sum(line.qty for line in self._allocations)

    @property 
    def available_quantity(self) -> Quantity:
        """Current quantity available for allocation

        Returns:
            int: current number of items available for allocation
        """
        return self._purchased_quantity - self.allocated_quantity
    

def allocate(line: OrderLine, batches: List[Batch]) -> Reference:
    """Takes an order line and a list of batches and will allocate orders against batches intelligently

    Args:
        line (OrderLine): Order line container desired quantity
        batches (List[Batch]): List of batches to order against

    Returns:
        Reference: reference id of the batch allocated against
    """
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
    return batch.reference