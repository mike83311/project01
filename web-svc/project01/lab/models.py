from django.db import models
from django.utils import timezone


class Library(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    document = models.FileField(
        upload_to='documents/', blank=False, null=False)
    update_time = models.DateTimeField(
        default=timezone.now, blank=False, null=False)
    update_user = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT)
    topic = models.JSONField(null=True)
    paper_category = models.ForeignKey(
        'lab.PaperCategory', on_delete=models.PROTECT)
    publish_time = models.CharField(max_length=10, blank=False, null=False)
    author = models.CharField(max_length=45, blank=False, null=False)

    class Meta:
        db_table = 'library'


class PaperCategory(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    update_time = models.DateTimeField(
        default=timezone.now, blank=False, null=False)
    update_user = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT)

    class Meta:
        db_table = 'paper_category'


class LabMember(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    update_time = models.DateTimeField(
        default=timezone.now, blank=False, null=False)
    update_user = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT)
    graduation_time = models.DateTimeField(
        default=timezone.now, blank=False, null=False)
    member_category = models.ForeignKey(
        'lab.MemberCategory', on_delete=models.PROTECT)
    expertise = models.JSONField(null=True)
    relevant_info = models.JSONField(null=True)

    class Meta:
        db_table = 'lab_member'


class MemberCategory(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    update_time = models.DateTimeField(
        default=timezone.now, blank=False, null=False)
    update_user = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT)

    class Meta:
        db_table = 'member_category'


class ResearchResults(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    update_time = models.DateTimeField(
        default=timezone.now, blank=False, null=False)
    update_user = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT)
    github_link = models.URLField(max_length=200, null=True)
    youtube_link = models.URLField(max_length=200, null=True)
    demo_link = models.URLField(max_length=200, null=True)

    class Meta:
        db_table = 'research_results'
