from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='registrado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas_registradas', to=settings.AUTH_USER_MODEL),
        ),
    ]