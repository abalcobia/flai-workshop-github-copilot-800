from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from pymongo import MongoClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data directly via pymongo to avoid ORM issues with
        # malformed documents that may have non-integer primary keys.
        self.stdout.write('Clearing existing data...')
        _client = MongoClient('localhost', 27017)
        _db = _client['octofit_db']
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            _db[col].delete_many({})
        _client.close()

        # Create Teams using Django ORM
        self.stdout.write('Inserting teams...')
        Team.objects.create(
            id=1,
            name='Team Marvel',
            description="Earth's Mightiest Heroes",
        )
        Team.objects.create(
            id=2,
            name='Team DC',
            description='Justice League United',
        )
        # Re-fetch to get clean integer PKs (djongo can return ObjectId on save)
        team_marvel = Team.objects.get(pk=1)
        team_dc = Team.objects.get(pk=2)
        self.stdout.write(self.style.SUCCESS('Inserted 2 teams'))

        # Create Users using Django ORM
        self.stdout.write('Inserting users...')
        users_info = [
            # Team Marvel
            (1, 'Tony Stark', 'ironman@avengers.com', team_marvel, '🦾', 'advanced'),
            (2, 'Steve Rogers', 'captain@avengers.com', team_marvel, '🛡️', 'advanced'),
            (3, 'Natasha Romanoff', 'blackwidow@avengers.com', team_marvel, '🕷️', 'advanced'),
            (4, 'Bruce Banner', 'hulk@avengers.com', team_marvel, '💚', 'advanced'),
            (5, 'Thor Odinson', 'thor@asgard.com', team_marvel, '⚡', 'god-tier'),
            # Team DC
            (6, 'Clark Kent', 'superman@justiceleague.com', team_dc, '🦸', 'god-tier'),
            (7, 'Bruce Wayne', 'batman@gotham.com', team_dc, '🦇', 'advanced'),
            (8, 'Diana Prince', 'wonderwoman@themyscira.com', team_dc, '⭐', 'god-tier'),
            (9, 'Barry Allen', 'flash@speedforce.com', team_dc, '⚡', 'advanced'),
            (10, 'Arthur Curry', 'aquaman@atlantis.com', team_dc, '🔱', 'advanced'),
        ]

        users = []
        for uid, name, email, team, avatar, fitness_level in users_info:
            User.objects.create(
                id=uid,
                name=name,
                email=email,
                team=team,
                avatar=avatar,
                fitness_level=fitness_level,
            )
        # Re-fetch users with clean integer PKs
        users = list(User.objects.all().order_by('id'))
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users)} users'))

        # Create Activities using Django ORM
        self.stdout.write('Inserting activities...')
        activity_types = ['running', 'cycling', 'swimming', 'strength_training', 'yoga']
        activities_created = 0
        activity_id = 1
        for user in users:
            num_activities = random.randint(5, 10)
            for j in range(num_activities):
                days_ago = random.randint(0, 30)
                activity_date = timezone.now() - timedelta(days=days_ago)
                Activity.objects.create(
                    id=activity_id,
                    user=user,
                    activity_type=random.choice(activity_types),
                    duration=random.randint(15, 120),
                    date=activity_date,
                    notes=f'Great workout session #{j + 1}',
                )
                activity_id += 1
                activities_created += 1
        self.stdout.write(self.style.SUCCESS(f'Inserted {activities_created} activities'))

        # Create Leaderboard entries using Django ORM
        self.stdout.write('Calculating leaderboard...')
        leaderboard_entries = []
        for user in users:
            total_duration = sum(
                a.duration for a in Activity.objects.filter(user=user)
            )
            leaderboard_entries.append((user, total_duration))

        # Sort by total duration descending and assign ranks
        leaderboard_entries.sort(key=lambda x: x[1], reverse=True)
        for rank, (user, score) in enumerate(leaderboard_entries, start=1):
            Leaderboard.objects.create(id=rank, user=user, score=score, rank=rank)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_entries)} leaderboard entries'))

        # Create Workout suggestions using Django ORM
        self.stdout.write('Inserting workout suggestions...')
        workouts_data = [
            {
                'name': 'Super Soldier Circuit',
                'description': "Captain America's legendary training routine",
                'difficulty': 'advanced',
                'exercises': [
                    {'name': 'Push-ups', 'reps': 50, 'sets': 4},
                    {'name': 'Pull-ups', 'reps': 20, 'sets': 4},
                    {'name': 'Squats', 'reps': 50, 'sets': 4},
                    {'name': 'Burpees', 'reps': 30, 'sets': 3},
                ],
            },
            {
                'name': 'Speedster Sprint Training',
                'description': "Barry Allen's speed-building workout",
                'difficulty': 'intermediate',
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': '30 sec', 'sets': 10},
                    {'name': 'High Knees', 'duration': '1 min', 'sets': 5},
                    {'name': 'Mountain Climbers', 'reps': 40, 'sets': 4},
                ],
            },
            {
                'name': 'Amazonian Warrior Training',
                'description': "Wonder Woman's combat conditioning",
                'difficulty': 'advanced',
                'exercises': [
                    {'name': 'Sword Swings (weighted)', 'reps': 30, 'sets': 5},
                    {'name': 'Shield Holds', 'duration': '2 min', 'sets': 3},
                    {'name': 'Battle Rope', 'duration': '1 min', 'sets': 5},
                    {'name': 'Box Jumps', 'reps': 25, 'sets': 4},
                ],
            },
            {
                'name': 'Atlantean Swim Power',
                'description': "Aquaman's underwater endurance training",
                'difficulty': 'intermediate',
                'exercises': [
                    {'name': 'Freestyle Swimming', 'distance': '1000m', 'sets': 3},
                    {'name': 'Underwater Breath Hold', 'duration': '2 min', 'sets': 5},
                    {'name': 'Treading Water', 'duration': '5 min', 'sets': 3},
                ],
            },
            {
                'name': 'Zen Master Flow',
                'description': "Black Widow's flexibility and balance routine",
                'difficulty': 'beginner',
                'exercises': [
                    {'name': 'Sun Salutations', 'reps': 10, 'sets': 3},
                    {'name': 'Warrior Poses', 'duration': '1 min each', 'sets': 3},
                    {'name': 'Tree Pose', 'duration': '1 min', 'sets': 3},
                    {'name': 'Cobra Stretch', 'duration': '30 sec', 'sets': 4},
                ],
            },
            {
                'name': 'Dark Knight Conditioning',
                'description': "Batman's stealth and agility training",
                'difficulty': 'advanced',
                'exercises': [
                    {'name': 'Parkour Drills', 'duration': '10 min', 'sets': 1},
                    {'name': 'Rope Climbing', 'reps': 10, 'sets': 3},
                    {'name': 'Handstand Push-ups', 'reps': 15, 'sets': 3},
                    {'name': 'Ninja Rolls', 'reps': 20, 'sets': 4},
                ],
            },
            {
                'name': 'Arc Reactor Cardio',
                'description': "Iron Man's heart-healthy workout",
                'difficulty': 'intermediate',
                'exercises': [
                    {'name': 'Cycling', 'duration': '20 min', 'sets': 1},
                    {'name': 'Jumping Jacks', 'reps': 50, 'sets': 3},
                    {'name': 'Step-ups', 'reps': 30, 'sets': 4},
                ],
            },
        ]

        for w_id, w in enumerate(workouts_data, start=1):
            Workout.objects.create(
                id=w_id,
                name=w['name'],
                description=w['description'],
                difficulty=w['difficulty'],
                exercises=w['exercises'],
            )
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts_data)} workout suggestions'))

        # Summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('DATABASE POPULATION COMPLETE!'))
        self.stdout.write('=' * 50 + '\n')
        self.stdout.write('Collection counts:')
        self.stdout.write(f'  Users: {User.objects.count()}')
        self.stdout.write(f'  Teams: {Team.objects.count()}')
        self.stdout.write(f'  Activities: {Activity.objects.count()}')
        self.stdout.write(f'  Leaderboard: {Leaderboard.objects.count()}')
        self.stdout.write(f'  Workouts: {Workout.objects.count()}')

