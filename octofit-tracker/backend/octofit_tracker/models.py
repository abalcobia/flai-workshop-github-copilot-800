from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    avatar = models.CharField(max_length=10, blank=True, default='')
    fitness_level = models.CharField(max_length=50, blank=True, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('strength_training', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('walking', 'Walking'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration = models.FloatField(help_text='Duration in minutes')
    date = models.DateTimeField()
    notes = models.CharField(max_length=500, blank=True, default='')

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.user.name} - {self.activity_type} ({self.duration} min)"


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    score = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.user.name} - Rank {self.rank} (Score: {self.score})"


class Workout(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('god-tier', 'God-Tier'),
    ]
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True, default='')
    exercises = models.JSONField(default=list)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='beginner')

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
