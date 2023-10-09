# management/commands/generate_daily_lottery_data.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from random import sample
from lotteryx.models import Game, LotteryDraw

class Command(BaseCommand):
    help = 'Generate daily lottery draws and winning numbers for different games'

    def handle(self, *args, **options):
        game_schedule = [
            {"name": "Treasure Hunt", "time": "08:00:00"},
            {"name": "Cash Cascade", "time": "11:00:00"},
            {"name": "Platinum Payout", "time": "14:00:00"},
            {"name": "Winning Waves", "time": "17:00:00"},
            {"name": "Money Magic", "time": "20:00:00"},
        ]

        current_date = timezone.now().date()
        current_time = timezone.now().time()

        # Check if it's 8:05 am to generate draws for all games
        if current_time.hour == 13 and current_time.minute == 5:
            for game_info in game_schedule:
                game_name = game_info["name"]
                draw_time = datetime.combine(current_date, datetime.strptime(game_info["time"], "%H:%M:%S").time())

                existing_draw = LotteryDraw.objects.filter(game__name=game_name, draw_date=draw_time).first()

                if not existing_draw:
                    # Create a new LotteryDraw instance without winning numbers
                    game = Game.objects.get(name=game_name)
                    draw = LotteryDraw(game=game, draw_date=draw_time)
                    draw.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully created draw for {game_name} at {draw_time}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Draw for {game_name} at {draw_time} already exists'))

        # Check if it's the specified time to generate winning numbers
        for game_info in game_schedule:
            game_name = game_info["name"]
            winning_time = datetime.combine(current_date, datetime.strptime(game_info["time"], "%H:%M:%S").time())

            # Check if it's the specified time to generate winning numbers
            if current_time.hour == winning_time.hour and current_time.minute == winning_time.minute:
                draws = LotteryDraw.objects.filter(game__name=game_name, winning_numbers="")

                for draw in draws:
                    # Generate five random winning numbers
                    winning_numbers = ",".join(map(str, sample(range(1, 100), 5)))
                    draw.winning_numbers = winning_numbers
                    draw.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully generated winning numbers for draw at {draw.draw_date}'))
