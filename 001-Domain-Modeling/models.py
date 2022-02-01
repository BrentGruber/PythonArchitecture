from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True) #frozen=True makes this immutable
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set() # Set allocations to an empty set

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
    def allocated_quantity(self) -> int:
        """Current quantity allocated to orders

        Returns:
            int: number of items allocated
        """
        return sum(line.qty for line in self._allocations)

    @property 
    def available_quantity(self) -> int:
        """Current quantity available for allocation

        Returns:
            int: current number of items available for allocation
        """
        return self._purchased_quantity - self.allocated_quantity
    

    
