from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tasks.models import Comment, Project, Task


class Command(BaseCommand):
    help = "Seed the database with realistic dummy data"

    def handle(self, *args, **options):
        owner = User.objects.filter(is_superuser=True).first()
        if owner is None:
            owner = User.objects.create_superuser("admin", "admin@example.com", "admin12345")

        team = []
        for name in ["kwame", "ama"]:
            user, created = User.objects.get_or_create(username=name)
            if created:
                user.set_password("password123")
                user.save()
            team.append(user)

        today = date.today()
        # (project name, description, [(title, description, status, assignee, due offset in days)])
        data = [
            ("Company Website", "Redesign and launch the new company website", [
                ("Create Homepage", "Design and develop the website homepage", "Completed", owner, -5),
                ("Build Contact Page", "Contact form with email notification", "In Progress", team[0], 3),
                ("Write About Us Copy", "Draft and proofread the About Us content", "Pending", team[1], 7),
                ("Set Up Hosting", "Configure domain and deploy to production", "Pending", owner, 14),
            ]),
            ("Mobile App Launch", "Prepare the mobile app for its first release", [
                ("Design App Icon", "Create icon variants for iOS and Android", "Completed", team[1], -10),
                ("Fix Login Bug", "Users are logged out after app restart", "In Progress", team[0], -1),
                ("Prepare Store Listing", "Screenshots, description and keywords", "Pending", owner, 10),
            ]),
            ("Exam Revision Plan", "Organise revision for end of semester exams", [
                ("Revise Database Concepts", "ER diagrams, normalization and SQL joins", "In Progress", owner, 4),
                ("Practice Numerical Methods", "Newton-Raphson and interpolation problems", "Pending", owner, 6),
                ("Assembly Language Past Questions", "Go through the last three years", "Pending", owner, 9),
            ]),
            ("Social Media Campaign", "Plan and schedule the launch campaign", [
                ("Plan Content Calendar", "Four weeks of posts across platforms", "Completed", team[1], -3),
                ("Record Launch Video", "Short promo video for TikTok and LinkedIn", "Pending", team[0], 5),
            ]),
        ]

        comments = {
            "Fix Login Bug": [(team[0], "Reproduced it on Android 13, looking at token storage."),
                              (owner, "Please prioritise this before the store submission.")],
            "Create Homepage": [(owner, "Homepage approved by the client.")],
            "Revise Database Concepts": [(owner, "Finished normalization, joins next.")],
        }

        task_count = 0
        for name, description, tasks in data:
            project, _ = Project.objects.get_or_create(
                name=name, owner=owner, defaults={"description": description}
            )
            project.members.add(*team)
            for title, desc, status, assignee, offset in tasks:
                Task.objects.get_or_create(
                    project=project, title=title,
                    defaults={
                        "description": desc,
                        "status": status,
                        "assigned_to": assignee,
                        "due_date": today + timedelta(days=offset),
                    },
                )
                task_count += 1

        for title, items in comments.items():
            task = Task.objects.filter(title=title).first()
            if task:
                for author, content in items:
                    Comment.objects.get_or_create(task=task, author=author, content=content)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(data)} projects and {task_count} tasks."
        ))