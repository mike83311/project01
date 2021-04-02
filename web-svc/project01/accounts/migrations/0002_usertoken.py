# Generated by Django 3.1.5 on 2021-04-02 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('expires', models.DateTimeField(verbose_name='Expires in')),
                ('user', models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'db_table': 'user_token',
            },
        ),
    ]
