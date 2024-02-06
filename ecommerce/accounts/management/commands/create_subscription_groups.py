from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from ecommerce.constants import (
    IS_REGISTERED,
    CAN_PUBLISH_PRODUCTS,
    CAN_PROCESS_ORDERS,
    CAN_USE_CLIENT_CHAT,
    CAN_BACKUP_ITEMS,
    CAN_PROMOTE_PRODUCTS,
    CAN_USE_ANALYTICS,
    CAN_REQUEST_HELPDESK_BOT,
)


class Command(BaseCommand):
    help = "Create subscription groups and assign permissions"

    def handle(self, *args, **options):
        # Create groups
        base_subscription_group, created = Group.objects.get_or_create(
            name="Base Subscription"
        )
        simple_subscription_group, created = Group.objects.get_or_create(
            name="Simple Subscription"
        )
        medium_subscription_group, created = Group.objects.get_or_create(
            name="Medium Subscription"
        )
        premium_subscription_group, created = Group.objects.get_or_create(
            name="Premium Subscription"
        )

        # Assign permissions to groups
        base_subscription_group.permissions.add(
            Permission.objects.get(codename=IS_REGISTERED),
            Permission.objects.get(codename=CAN_PUBLISH_PRODUCTS),
            Permission.objects.get(codename=CAN_PROCESS_ORDERS),
        )

        simple_subscription_group.permissions.add(
            Permission.objects.get(codename=CAN_USE_CLIENT_CHAT),
            Permission.objects.get(codename=CAN_BACKUP_ITEMS),
        )

        medium_subscription_group.permissions.add(
            Permission.objects.get(codename=CAN_PROMOTE_PRODUCTS),
        )

        premium_subscription_group.permissions.add(
            Permission.objects.get(codename=CAN_USE_ANALYTICS),
            Permission.objects.get(codename=CAN_REQUEST_HELPDESK_BOT),
        )
