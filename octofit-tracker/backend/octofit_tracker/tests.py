from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes'
        )

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Team Marvel')
        self.assertEqual(self.team.description, 'Earth\'s Mightiest Heroes')

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Team Marvel')


class UserModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team Marvel')
        self.user = User.objects.create(
            name='Tony Stark',
            email='ironman@avengers.com',
            team=self.team,
            fitness_level='advanced'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.name, 'Tony Stark')
        self.assertEqual(self.user.email, 'ironman@avengers.com')
        self.assertEqual(self.user.fitness_level, 'advanced')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'Tony Stark')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team Marvel')
        self.user = User.objects.create(
            name='Tony Stark',
            email='ironman@avengers.com',
            team=self.team
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30.0,
            date=datetime.utcnow()
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30.0)

    def test_activity_str(self):
        self.assertIn('Tony Stark', str(self.activity))
        self.assertIn('running', str(self.activity))


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team Marvel')
        self.user = User.objects.create(
            name='Tony Stark',
            email='ironman@avengers.com',
            team=self.team
        )
        self.entry = Leaderboard.objects.create(
            user=self.user,
            score=1500.0,
            rank=1
        )

    def test_leaderboard_creation(self):
        self.assertEqual(self.entry.score, 1500.0)
        self.assertEqual(self.entry.rank, 1)

    def test_leaderboard_str(self):
        self.assertIn('Tony Stark', str(self.entry))
        self.assertIn('Rank 1', str(self.entry))


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Hero Circuit',
            description='Full body workout',
            exercises=[{'name': 'Push-ups', 'reps': 20}],
            difficulty='intermediate'
        )

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, 'Hero Circuit')
        self.assertEqual(self.workout.difficulty, 'intermediate')

    def test_workout_str(self):
        self.assertEqual(str(self.workout), 'Hero Circuit')


class APIEndpointsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Team Marvel', description='Avengers')
        self.user = User.objects.create(
            name='Tony Stark',
            email='ironman@avengers.com',
            team=self.team,
            fitness_level='advanced'
        )

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_get_teams(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_activities(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_leaderboard(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workouts(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        data = {'name': 'Team DC', 'description': 'Justice League'}
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Team DC')

    def test_create_workout(self):
        data = {
            'name': 'Speed Force Training',
            'description': 'Fast-paced workout',
            'exercises': [{'name': 'Sprints', 'reps': 10}],
            'difficulty': 'advanced'
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Speed Force Training')
