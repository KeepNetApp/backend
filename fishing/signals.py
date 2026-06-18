from django.db.models.signals import post_save
from django.dispatch import receiver

from fishing.models import Catch, UserSpeciesStats


@receiver(post_save, sender=Catch)
def update_species_stats(sender, instance, created, **kwargs):
    if created:
        stats, stat_created = UserSpeciesStats.objects.get_or_create(user=instance.user, species=instance.species)

        stats.total_caught += 1

        # Updating first catch
        if stats.first_catch is None:
            stats.first_catch = instance

        # Updating max weight
        if instance.max_weight is not None:
            if stats.max_weight_catch is None or instance.weight_kg > stats.max_weight_catch.weight_kg:
                stats.max_weight_catch = instance

        # Updating max length
        if instance.length_m is not None:
            if stats.max_length_catch is None or instance.length_m > stats.max_length_catch.length_m:
                stats.max_length_catch = instance

        stats.save()