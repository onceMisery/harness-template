# Domain Model

## Entities
- Order
- Payment
- Refund

## Value Objects
- Money
- Address
- OrderItem

## State Transitions
- CREATED -> PAID -> FULFILLED
- CREATED -> CANCELLED

## Invariants
- Paid orders cannot be deleted
- Refund amount cannot exceed paid amount
