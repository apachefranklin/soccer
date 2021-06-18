# Generated by Django 3.0.6 on 2021-05-08 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('begin_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincoupechef.Edition')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('logo', models.CharField(default='default.png', max_length=50)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PouleTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.SmallIntegerField(default=0)),
                ('points', models.SmallIntegerField(default=0)),
                ('conceded_goals', models.SmallIntegerField(default=0)),
                ('goals_average', models.SmallIntegerField(default=0)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('poule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincoupechef.Poule')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincoupechef.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50, null=True)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_now_add=True)),
                ('date_to_play', models.DateField(null=True)),
                ('state', models.CharField(choices=[('reporte', 'Reported'), ('en cours', 'Current'), ('annulé', 'Cancel'), ('terminé', 'Finish'), ('a programmé', 'To Program')], default='a programmé', max_length=50)),
                ('match_type', models.CharField(choices=[('FINAL', 'Final'), ('SEMIFINAL', 'Semifinal'), ('POULE', 'Poule'), ('AMICAL', 'Amical')], default='POULE', max_length=50)),
                ('goal_team1', models.SmallIntegerField(default=0)),
                ('goal_team2', models.SmallIntegerField(default=0)),
                ('winner', models.SmallIntegerField(default=0)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincoupechef.Edition')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='admincoupechef.Team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='admincoupechef.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_type', models.CharField(choices=[('CSC', 'Csc'), ('SP', 'Sp'), ('N', 'N')], max_length=50)),
                ('add_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincoupechef.Match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincoupechef.Player')),
            ],
        ),
    ]