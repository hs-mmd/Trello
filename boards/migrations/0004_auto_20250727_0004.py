from django.db import migrations

def create_tags(apps, schema_editor):
    Tag = apps.get_model('boards', 'Tag')
    for name in [
        'New Feature',
        'Refactoring',
        'Bug Fix',
        'R&D'
    ]:
        Tag.objects.get_or_create(name=name)

class Migration(migrations.Migration):   
    
    dependencies = [
        ('boards', '0003_tag_task_tags'),  
    ]

    operations = [
        migrations.RunPython(create_tags),
    ]
