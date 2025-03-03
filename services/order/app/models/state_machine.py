from app.models.order import OrderStatus

class OrderStateMachine:
        
    ALLOWED_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
        OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],  
        OrderStatus.CANCELLED: [], 
    }
    
    CANCELLABLE_STATES = [OrderStatus.PENDING, OrderStatus.PROCESSING]
    
    @classmethod
    def can_transition(cls, current_status, new_status):
        if current_status not in cls.ALLOWED_TRANSITIONS:
            return False
        return new_status in cls.ALLOWED_TRANSITIONS[current_status]
    
    @classmethod
    def can_cancel(cls, current_status):
        return current_status in cls.CANCELLABLE_STATES
    
    @classmethod
    def validate_transition(cls, current_status, new_status):
        if not cls.can_transition(current_status, new_status):
            raise ValueError(
                f"Invalid state transition from {current_status} to {new_status}. "
                f"Allowed transitions: {cls.ALLOWED_TRANSITIONS.get(current_status, [])}"
            )
        return True 