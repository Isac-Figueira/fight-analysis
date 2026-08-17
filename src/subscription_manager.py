"""Subscription and billing management module"""

from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass
from .utils import Logger


class PlanType(Enum):
    """Available subscription plans"""
    INDIVIDUAL = "individual"
    ACADEMY = "academy"


class PaymentStatus(Enum):
    """Payment status types"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Plan:
    """Subscription plan definition"""
    plan_type: PlanType
    name: str
    price_monthly: float
    description: str
    max_videos_per_month: int
    max_storage_gb: int
    features: List[str]
    
    def __post_init__(self):
        """Validate plan data"""
        if self.price_monthly < 0:
            raise ValueError("Price cannot be negative")
        if self.max_videos_per_month <= 0:
            raise ValueError("Max videos must be positive")


@dataclass
class Subscription:
    """User subscription information"""
    user_id: str
    plan: Plan
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True
    auto_renew: bool = True
    videos_used_this_month: int = 0
    storage_used_gb: float = 0.0


@dataclass
class Payment:
    """Payment record"""
    payment_id: str
    user_id: str
    subscription: Subscription
    amount: float
    payment_date: datetime
    due_date: datetime
    status: PaymentStatus
    payment_method: str  # credit_card, paypal, bank_transfer, etc
    description: str


class SubscriptionManager:
    """Manages user subscriptions and billing"""
    
    def __init__(self):
        """Initialize subscription manager"""
        self.logger = Logger(__name__)
        self._load_plans()
        self.subscriptions: Dict[str, Subscription] = {}
        self.payments: Dict[str, List[Payment]] = {}
        self.logger.info("SubscriptionManager initialized")
    
    def _load_plans(self) -> None:
        """Load available subscription plans"""
        self.plans = {
            PlanType.INDIVIDUAL: Plan(
                plan_type=PlanType.INDIVIDUAL,
                name="Plano Individual",
                price_monthly=40.00,
                description="Perfeito para lutadores individuais",
                max_videos_per_month=10,
                max_storage_gb=50,
                features=[
                    "Análise de até 10 vídeos por mês",
                    "Armazenamento de 50GB",
                    "Detecção de movimentos",
                    "Identificação de erros técnicos",
                    "Relatórios mensais",
                    "Suporte via email"
                ]
            ),
            PlanType.ACADEMY: Plan(
                plan_type=PlanType.ACADEMY,
                name="Plano Academia",
                price_monthly=80.00,
                description="Ideal para academias e equipes",
                max_videos_per_month=100,
                max_storage_gb=500,
                features=[
                    "Análise de até 100 vídeos por mês",
                    "Armazenamento de 500GB",
                    "Detecção avançada de movimentos",
                    "Identificação de erros técnicos",
                    "Relatórios detalhados por atleta",
                    "Análise comparativa entre alunos",
                    "Suporte prioritário via email e chat",
                    "Acesso para múltiplos usuários",
                    "Exportação de relatórios em PDF"
                ]
            )
        }
        self.logger.info("Plans loaded: Individual ($40/mo), Academy ($80/mo)")
    
    def create_subscription(self, user_id: str, plan_type: PlanType,
                          auto_renew: bool = True) -> Subscription:
        """
        Create a new subscription for a user
        
        Args:
            user_id: Unique user identifier
            plan_type: Type of plan to subscribe to
            auto_renew: Whether subscription should auto-renew
        
        Returns:
            New Subscription object
        """
        if user_id in self.subscriptions:
            raise ValueError(f"User {user_id} already has an active subscription")
        
        if plan_type not in self.plans:
            raise ValueError(f"Invalid plan type: {plan_type}")
        
        plan = self.plans[plan_type]
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        
        subscription = Subscription(
            user_id=user_id,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            auto_renew=auto_renew
        )
        
        self.subscriptions[user_id] = subscription
        self.logger.info(f"Subscription created for user {user_id}: {plan.name}")
        
        return subscription
    
    def get_subscription(self, user_id: str) -> Optional[Subscription]:
        """
        Get user's current subscription
        
        Args:
            user_id: User identifier
        
        Returns:
            Subscription object or None if no active subscription
        """
        subscription = self.subscriptions.get(user_id)
        
        if subscription and subscription.is_active:
            # Check if subscription has expired
            if subscription.end_date and datetime.now() > subscription.end_date:
                if subscription.auto_renew:
                    self._renew_subscription(user_id)
                else:
                    subscription.is_active = False
                    self.logger.info(f"Subscription expired for user {user_id}")
        
        return subscription if subscription and subscription.is_active else None
    
    def _renew_subscription(self, user_id: str) -> Optional[Subscription]:
        """
        Renew an expired subscription
        
        Args:
            user_id: User identifier
        
        Returns:
            Renewed subscription or None
        """
        subscription = self.subscriptions.get(user_id)
        
        if not subscription:
            return None
        
        old_end_date = subscription.end_date
        subscription.start_date = old_end_date
        subscription.end_date = old_end_date + timedelta(days=30)
        subscription.videos_used_this_month = 0  # Reset video count
        subscription.is_active = True
        
        self.logger.info(f"Subscription renewed for user {user_id}")
        
        # Create payment record for renewal
        self._record_payment(
            user_id=user_id,
            amount=subscription.plan.price_monthly,
            payment_method="auto_renewal"
        )
        
        return subscription
    
    def cancel_subscription(self, user_id: str) -> bool:
        """
        Cancel a user's subscription
        
        Args:
            user_id: User identifier
        
        Returns:
            True if cancelled successfully, False otherwise
        """
        subscription = self.subscriptions.get(user_id)
        
        if not subscription:
            self.logger.warning(f"No subscription found for user {user_id}")
            return False
        
        subscription.is_active = False
        subscription.auto_renew = False
        self.logger.info(f"Subscription cancelled for user {user_id}")
        
        return True
    
    def upgrade_plan(self, user_id: str, new_plan_type: PlanType) -> Optional[Subscription]:
        """
        Upgrade user's subscription plan
        
        Args:
            user_id: User identifier
            new_plan_type: New plan type to upgrade to
        
        Returns:
            Updated subscription or None
        """
        subscription = self.subscriptions.get(user_id)
        
        if not subscription:
            self.logger.warning(f"No subscription found for user {user_id}")
            return None
        
        if subscription.plan.plan_type == new_plan_type:
            self.logger.warning(f"User {user_id} is already on {new_plan_type} plan")
            return subscription
        
        old_plan = subscription.plan
        new_plan = self.plans[new_plan_type]
        
        # Calculate pro-rata adjustment
        days_remaining = (subscription.end_date - datetime.now()).days
        price_difference = new_plan.price_monthly - old_plan.price_monthly
        pro_rata_charge = (price_difference / 30) * days_remaining
        
        subscription.plan = new_plan
        
        self.logger.info(
            f"User {user_id} upgraded from {old_plan.name} to {new_plan.name}. "
            f"Pro-rata charge: ${pro_rata_charge:.2f}"
        )
        
        # Record the upgrade payment
        self._record_payment(
            user_id=user_id,
            amount=pro_rata_charge,
            payment_method="upgrade"
        )
        
        return subscription
    
    def use_video_analysis(self, user_id: str) -> bool:
        """
        Record a video analysis usage
        
        Args:
            user_id: User identifier
        
        Returns:
            True if usage recorded successfully, False if limit reached
        """
        subscription = self.get_subscription(user_id)
        
        if not subscription:
            self.logger.warning(f"No active subscription for user {user_id}")
            return False
        
        if subscription.videos_used_this_month >= subscription.plan.max_videos_per_month:
            self.logger.warning(
                f"User {user_id} has reached monthly video limit "
                f"({subscription.plan.max_videos_per_month})"
            )
            return False
        
        subscription.videos_used_this_month += 1
        self.logger.info(
            f"Video usage recorded for user {user_id}. "
            f"Videos used: {subscription.videos_used_this_month}/{subscription.plan.max_videos_per_month}"
        )
        
        return True
    
    def get_usage_stats(self, user_id: str) -> Optional[Dict]:
        """
        Get user's current usage statistics
        
        Args:
            user_id: User identifier
        
        Returns:
            Dictionary with usage stats or None
        """
        subscription = self.get_subscription(user_id)
        
        if not subscription:
            return None
        
        videos_remaining = (
            subscription.plan.max_videos_per_month - 
            subscription.videos_used_this_month
        )
        storage_remaining = (
            subscription.plan.max_storage_gb - 
            subscription.storage_used_gb
        )
        
        days_remaining = (subscription.end_date - datetime.now()).days
        
        return {
            'plan_name': subscription.plan.name,
            'plan_type': subscription.plan.plan_type.value,
            'videos_used': subscription.videos_used_this_month,
            'videos_limit': subscription.plan.max_videos_per_month,
            'videos_remaining': max(0, videos_remaining),
            'storage_used_gb': subscription.storage_used_gb,
            'storage_limit_gb': subscription.plan.max_storage_gb,
            'storage_remaining_gb': max(0.0, storage_remaining),
            'subscription_end_date': subscription.end_date.isoformat(),
            'days_until_renewal': max(0, days_remaining),
            'auto_renew': subscription.auto_renew
        }
    
    def _record_payment(self, user_id: str, amount: float, 
                       payment_method: str = "credit_card") -> Payment:
        """
        Record a payment transaction
        
        Args:
            user_id: User identifier
            amount: Payment amount
            payment_method: Method of payment
        
        Returns:
            Payment object
        """
        subscription = self.subscriptions.get(user_id)
        
        if not subscription:
            raise ValueError(f"No subscription found for user {user_id}")
        
        payment_id = f"PAY_{user_id}_{datetime.now().timestamp()}"
        payment = Payment(
            payment_id=payment_id,
            user_id=user_id,
            subscription=subscription,
            amount=amount,
            payment_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=5),
            status=PaymentStatus.COMPLETED,
            payment_method=payment_method,
            description=f"Payment for {subscription.plan.name}"
        )
        
        if user_id not in self.payments:
            self.payments[user_id] = []
        
        self.payments[user_id].append(payment)
        self.logger.info(f"Payment recorded: {payment_id} - ${amount:.2f}")
        
        return payment
    
    def get_payment_history(self, user_id: str) -> List[Payment]:
        """
        Get user's payment history
        
        Args:
            user_id: User identifier
        
        Returns:
            List of Payment objects
        """
        return self.payments.get(user_id, [])
    
    def get_all_plans(self) -> Dict[str, Plan]:
        """
        Get all available plans
        
        Returns:
            Dictionary of available plans
        """
        plans_dict = {}
        for plan_type, plan in self.plans.items():
            plans_dict[plan_type.value] = {
                'name': plan.name,
                'price_monthly': plan.price_monthly,
                'description': plan.description,
                'max_videos_per_month': plan.max_videos_per_month,
                'max_storage_gb': plan.max_storage_gb,
                'features': plan.features
            }
        return plans_dict
    
    def generate_invoice(self, user_id: str, payment_id: str) -> Optional[Dict]:
        """
        Generate an invoice for a payment
        
        Args:
            user_id: User identifier
            payment_id: Payment identifier
        
        Returns:
            Invoice data dictionary or None
        """
        payments = self.payments.get(user_id, [])
        payment = next((p for p in payments if p.payment_id == payment_id), None)
        
        if not payment:
            self.logger.warning(f"Payment not found: {payment_id}")
            return None
        
        invoice = {
            'invoice_id': f"INV_{payment.payment_id}",
            'payment_id': payment.payment_id,
            'user_id': user_id,
            'date': payment.payment_date.isoformat(),
            'plan': payment.subscription.plan.name,
            'amount': payment.amount,
            'status': payment.status.value,
            'payment_method': payment.payment_method,
            'description': payment.description
        }
        
        self.logger.info(f"Invoice generated: {invoice['invoice_id']}")
        
        return invoice
