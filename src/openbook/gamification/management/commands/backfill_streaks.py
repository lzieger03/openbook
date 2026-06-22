# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.core.management.base import BaseCommand

from ...services.backfill import backfill_all_streaks


class Command(BaseCommand):
    help = "Recompute daily streaks for all existing users from reward_event_log history."

    def handle(self, *args, **options):
        results = backfill_all_streaks()

        for username, state in results:
            self.stdout.write(
                f"{username}: current={state['current_streak']} "
                f"longest={state['longest_streak']} "
                f"last_active={state['last_active_date']}"
            )

        self.stdout.write(self.style.SUCCESS(f"Backfilled streaks for {len(results)} user(s)."))
