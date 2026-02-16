import random

from django.utils import timezone

from .renderers import get_renderer


class SlotResolver:
    """Select a creative from a slot's eligible pool and render it."""

    def __init__(self, slot, request=None):
        self.slot = slot
        self.request = request

    def resolve_and_render(self):
        creative = self.select_creative()
        if not creative:
            return ""
        renderer = get_renderer(creative)
        return renderer.render(self.request)

    def select_creative(self):
        eligible = list(self.slot.get_eligible_creatives()[: self.slot.max_creatives])
        if not eligible:
            return None

        strategy = self.slot.rotation_strategy
        if strategy == "priority":
            return eligible[0]
        if strategy == "random":
            return random.choice(eligible)
        if strategy == "weighted":
            weights = [c.weight for c in eligible]
            return random.choices(eligible, weights=weights, k=1)[0]
        if strategy == "sequential":
            bucket = int(timezone.now().timestamp() // 60)
            return eligible[bucket % len(eligible)]
        return eligible[0]
