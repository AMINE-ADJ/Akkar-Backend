from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_annonce_utilisateur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offre', models.CharField(max_length=127)),
                ('telephone', models.CharField(max_length=15)),
                ('nom', models.CharField(max_length=31)),
                ('email', models.CharField(max_length=31)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.annonce')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
