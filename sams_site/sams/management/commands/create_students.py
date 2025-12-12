from django.core.management.base import BaseCommand
from sams.models import Student


class Command(BaseCommand):
    help = 'Create 20 default students for attendance tracking'

    def handle(self, *args, **options):
        students_data = [
            ("Michael Johnson", "S001"),
            ("Sarah Williams", "S002"),
            ("David Brown", "S003"),
            ("Emily Davis", "S004"),
            ("James Wilson", "S005"),
            ("Jessica Martinez", "S006"),
            ("Robert Anderson", "S007"),
            ("Jennifer Taylor", "S008"),
            ("Christopher Thomas", "S009"),
            ("Amanda Moore", "S010"),
            ("Matthew Jackson", "S011"),
            ("Ashley Martin", "S012"),
            ("Daniel Lee", "S013"),
            ("Brittany White", "S014"),
            ("Joshua Harris", "S015"),
            ("Stephanie Clark", "S016"),
            ("Andrew Lewis", "S017"),
            ("Nicole Robinson", "S018"),
            ("Ryan Walker", "S019"),
            ("Lauren Young", "S020"),
        ]

        created_count = 0
        skipped_count = 0

        for name, student_id in students_data:
            student, created = Student.objects.get_or_create(
                student_id=student_id,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {name} ({student_id})'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Already exists: {name} ({student_id})'))
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Total created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'⊘ Total skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'Final count: {Student.objects.count()} students'))
