from django.core.management.base import BaseCommand
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        self.stdout.write(self.style.SUCCESS('Connected to MongoDB'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})
        
        # Create unique index on email field
        self.stdout.write('Creating unique index on email field...')
        db.users.create_index([("email", ASCENDING)], unique=True)
        
        # Insert Teams (Marvel and DC)
        self.stdout.write('Inserting teams...')
        teams_data = [
            {
                "_id": "team_marvel",
                "name": "Team Marvel",
                "description": "Earth's Mightiest Heroes",
                "created_at": datetime.utcnow()
            },
            {
                "_id": "team_dc",
                "name": "Team DC",
                "description": "Justice League United",
                "created_at": datetime.utcnow()
            }
        ]
        db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams_data)} teams'))
        
        # Insert Users (Superheroes)
        self.stdout.write('Inserting users...')
        users_data = [
            # Team Marvel
            {
                "name": "Tony Stark",
                "email": "ironman@avengers.com",
                "team_id": "team_marvel",
                "avatar": "🦾",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Steve Rogers",
                "email": "captain@avengers.com",
                "team_id": "team_marvel",
                "avatar": "🛡️",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Natasha Romanoff",
                "email": "blackwidow@avengers.com",
                "team_id": "team_marvel",
                "avatar": "🕷️",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Bruce Banner",
                "email": "hulk@avengers.com",
                "team_id": "team_marvel",
                "avatar": "💚",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Thor Odinson",
                "email": "thor@asgard.com",
                "team_id": "team_marvel",
                "avatar": "⚡",
                "fitness_level": "god-tier",
                "created_at": datetime.utcnow()
            },
            # Team DC
            {
                "name": "Clark Kent",
                "email": "superman@justiceleague.com",
                "team_id": "team_dc",
                "avatar": "🦸",
                "fitness_level": "god-tier",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Bruce Wayne",
                "email": "batman@gotham.com",
                "team_id": "team_dc",
                "avatar": "🦇",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Diana Prince",
                "email": "wonderwoman@themyscira.com",
                "team_id": "team_dc",
                "avatar": "⭐",
                "fitness_level": "god-tier",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Barry Allen",
                "email": "flash@speedforce.com",
                "team_id": "team_dc",
                "avatar": "⚡",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Arthur Curry",
                "email": "aquaman@atlantis.com",
                "team_id": "team_dc",
                "avatar": "🔱",
                "fitness_level": "advanced",
                "created_at": datetime.utcnow()
            }
        ]
        result = db.users.insert_many(users_data)
        user_ids = result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users_data)} users'))
        
        # Insert Activities
        self.stdout.write('Inserting activities...')
        activities_data = []
        activity_types = ['running', 'cycling', 'swimming', 'strength_training', 'yoga']
        
        for i, user_id in enumerate(user_ids):
            # Each user gets 5-10 random activities
            num_activities = random.randint(5, 10)
            for j in range(num_activities):
                days_ago = random.randint(0, 30)
                activity_date = datetime.utcnow() - timedelta(days=days_ago)
                
                activities_data.append({
                    "user_id": user_id,
                    "activity_type": random.choice(activity_types),
                    "duration_minutes": random.randint(15, 120),
                    "calories_burned": random.randint(100, 800),
                    "distance_km": round(random.uniform(1.0, 20.0), 2),
                    "date": activity_date,
                    "notes": f"Great workout session #{j+1}"
                })
        
        db.activities.insert_many(activities_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities_data)} activities'))
        
        # Calculate and insert Leaderboard data
        self.stdout.write('Calculating leaderboard...')
        leaderboard_data = []
        
        for user_data in users_data:
            user_email = user_data['email']
            # Get user's _id from database
            user_doc = db.users.find_one({"email": user_email})
            user_id = user_doc['_id']
            
            # Calculate total stats for user
            user_activities = list(db.activities.find({"user_id": user_id}))
            total_calories = sum(a.get('calories_burned', 0) for a in user_activities)
            total_distance = sum(a.get('distance_km', 0) for a in user_activities)
            total_workouts = len(user_activities)
            
            leaderboard_data.append({
                "user_id": user_id,
                "user_name": user_data['name'],
                "team_id": user_data['team_id'],
                "total_calories": total_calories,
                "total_distance_km": round(total_distance, 2),
                "total_workouts": total_workouts,
                "rank": 0,  # Will be calculated after sorting
                "last_updated": datetime.utcnow()
            })
        
        # Sort by total_calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        for rank, entry in enumerate(leaderboard_data, start=1):
            entry['rank'] = rank
        
        db.leaderboard.insert_many(leaderboard_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_data)} leaderboard entries'))
        
        # Insert Workout suggestions
        self.stdout.write('Inserting workout suggestions...')
        workouts_data = [
            {
                "name": "Super Soldier Circuit",
                "description": "Captain America's legendary training routine",
                "difficulty": "advanced",
                "duration_minutes": 45,
                "exercises": [
                    {"name": "Push-ups", "reps": 50, "sets": 4},
                    {"name": "Pull-ups", "reps": 20, "sets": 4},
                    {"name": "Squats", "reps": 50, "sets": 4},
                    {"name": "Burpees", "reps": 30, "sets": 3}
                ],
                "fitness_level": "advanced",
                "category": "strength_training"
            },
            {
                "name": "Speedster Sprint Training",
                "description": "Barry Allen's speed-building workout",
                "difficulty": "intermediate",
                "duration_minutes": 30,
                "exercises": [
                    {"name": "Sprint Intervals", "duration": "30 sec", "sets": 10},
                    {"name": "High Knees", "duration": "1 min", "sets": 5},
                    {"name": "Mountain Climbers", "reps": 40, "sets": 4}
                ],
                "fitness_level": "intermediate",
                "category": "running"
            },
            {
                "name": "Amazonian Warrior Training",
                "description": "Wonder Woman's combat conditioning",
                "difficulty": "advanced",
                "duration_minutes": 60,
                "exercises": [
                    {"name": "Sword Swings (weighted)", "reps": 30, "sets": 5},
                    {"name": "Shield Holds", "duration": "2 min", "sets": 3},
                    {"name": "Battle Rope", "duration": "1 min", "sets": 5},
                    {"name": "Box Jumps", "reps": 25, "sets": 4}
                ],
                "fitness_level": "advanced",
                "category": "strength_training"
            },
            {
                "name": "Atlantean Swim Power",
                "description": "Aquaman's underwater endurance training",
                "difficulty": "intermediate",
                "duration_minutes": 40,
                "exercises": [
                    {"name": "Freestyle Swimming", "distance": "1000m", "sets": 3},
                    {"name": "Underwater Breath Hold", "duration": "2 min", "sets": 5},
                    {"name": "Treading Water", "duration": "5 min", "sets": 3}
                ],
                "fitness_level": "intermediate",
                "category": "swimming"
            },
            {
                "name": "Zen Master Flow",
                "description": "Black Widow's flexibility and balance routine",
                "difficulty": "beginner",
                "duration_minutes": 30,
                "exercises": [
                    {"name": "Sun Salutations", "reps": 10, "sets": 3},
                    {"name": "Warrior Poses", "duration": "1 min each", "sets": 3},
                    {"name": "Tree Pose", "duration": "1 min", "sets": 3},
                    {"name": "Cobra Stretch", "duration": "30 sec", "sets": 4}
                ],
                "fitness_level": "beginner",
                "category": "yoga"
            },
            {
                "name": "Dark Knight Conditioning",
                "description": "Batman's stealth and agility training",
                "difficulty": "advanced",
                "duration_minutes": 50,
                "exercises": [
                    {"name": "Parkour Drills", "duration": "10 min", "sets": 1},
                    {"name": "Rope Climbing", "reps": 10, "sets": 3},
                    {"name": "Handstand Push-ups", "reps": 15, "sets": 3},
                    {"name": "Ninja Rolls", "reps": 20, "sets": 4}
                ],
                "fitness_level": "advanced",
                "category": "strength_training"
            },
            {
                "name": "Arc Reactor Cardio",
                "description": "Iron Man's heart-healthy workout",
                "difficulty": "intermediate",
                "duration_minutes": 35,
                "exercises": [
                    {"name": "Cycling", "duration": "20 min", "sets": 1},
                    {"name": "Jumping Jacks", "reps": 50, "sets": 3},
                    {"name": "Step-ups", "reps": 30, "sets": 4}
                ],
                "fitness_level": "intermediate",
                "category": "cycling"
            }
        ]
        
        db.workouts.insert_many(workouts_data)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts_data)} workout suggestions'))
        
        # Verify collections
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('DATABASE POPULATION COMPLETE!'))
        self.stdout.write('='*50 + '\n')
        
        self.stdout.write('Collection counts:')
        self.stdout.write(f'  Users: {db.users.count_documents({})}')
        self.stdout.write(f'  Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'  Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'  Leaderboard: {db.leaderboard.count_documents({})}')
        self.stdout.write(f'  Workouts: {db.workouts.count_documents({})}')
        
        client.close()
        self.stdout.write(self.style.SUCCESS('\nDatabase connection closed'))
