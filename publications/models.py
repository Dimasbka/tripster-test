from django.db import models
from django.db import transaction
from django.db.models.signals import post_delete, post_save

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class PublicationVote(models.Model):
    """Оценки хранятся в таком виде что-бы суммирование давало рейтинга статьи"""

    VOTE_CHOICES = (
        (-1, "Плохой"),
        (1, "Хороший"),
    )

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)

    publication = models.ForeignKey(
        "Publication", verbose_name="Публикация", on_delete=models.CASCADE
    )

    vote = models.IntegerField(default=0, verbose_name="Отзыв", choices=VOTE_CHOICES)

    class Meta:
        """Добавил проверку для контроля уникальных оценок на уровне базы"""

        unique_together = (
            (
                "user",
                "publication",
            ),
        )
        verbose_name = "оценка публикации"
        verbose_name_plural = "оценки публикаций"

    def __str__(self):
        return "vote %s: %s on %s" % (self.user, self.vote, self.publication)

    @classmethod
    def vote_add_or_update(cls, publication_id: int, vote: int, user_id: int):
        """ищет рейтинг c совпадающим publication_id  user_id
        если оценка не поменялась ничего не сохраняется
        если поменялось обновляет
        в противном случае создает новую оценку
        """
        with transaction.atomic():

            vote_obj, created = cls.objects.get_or_create(
                publication_id=publication_id,
                user_id=user_id,
                defaults={"vote": vote},
            )

            if created:
                return vote_obj

            elif vote_obj.vote != vote:
                vote_obj.vote = vote
                vote_obj.save()
            return vote_obj

    @classmethod
    def vote_delete(
        cls,
        publication_id: int,
        user_id: int,
    ):
        """Удаление уже проставленной оценки, в данном методе не проводится
        проверка на существование оценки так как это не влияет на результат
        """
        with transaction.atomic():
            cls.objects.filter(
                publication_id=publication_id,
                user_id=user_id,
            ).delete()


class Publication(models.Model):
    text = models.TextField(verbose_name="Текст публикации")

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)

    publish_date = models.DateTimeField(
        verbose_name="Дата публикации",
        default=timezone.now,
        blank=True,
    )

    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    votes = models.IntegerField(default=0, verbose_name="Количество голосов")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-publish_date",)

    @classmethod
    def update_vote_handler(this, sender, instance: PublicationVote, **kwargs):
        """обработчик Обновление рейтинга"""

        if instance:
            publication = instance.publication
            with transaction.atomic():
                res = publication.publicationvote_set.exclude(vote=0).aggregate(
                    models.Sum("vote"), models.Count("vote")
                )

                # результат может быть None
                publication.votes = res["vote__count"] if res["vote__count"] else 0
                publication.rating = res["vote__sum"] if res["vote__sum"] else 0
                publication.save()

    @classmethod
    def get_votes_rating_dict(cls, publication_id: int):
        """Получение текущего рейтинга
        сделано для теста но используется и при изменении оценок"""

        publication = cls.objects.get(id=publication_id)

        return {
            "votes": publication.votes,
            "rating": publication.rating,
        }


#  Обработка голосов сделано так чтобы отправлять два сигнала на один обработчик
post_delete.connect(Publication.update_vote_handler, sender=PublicationVote)
post_save.connect(Publication.update_vote_handler, sender=PublicationVote)
