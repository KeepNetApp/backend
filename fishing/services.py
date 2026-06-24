from django.db import transaction
from fishing.models import Catch, Session, UserSpeciesStats, CatchPhoto

def get_sync_data(user, since):
    sessions = Session.objects.filter(user=user)
    catches = Catch.objects.filter(user=user)
    photos = CatchPhoto.objects.filter(catch__user=user)
    stats = UserSpeciesStats.objects.filter(user=user)

    if since:
        sessions = sessions.filter(start_time__gte=since)
        catches = catches.filter(time_caught__gte=since)
        photos = photos.filter(catch__time_caught__gte=since)

    return {
        "sessions": sessions,
        "catches": catches,
        "photos": photos,
        "stats": stats
    }



def sync_sessions_from_payload(user, payload):
    synced_ids = []
    skipped_ids = []

    with transaction.atomic():
        for session_data in payload.get("sessions", []):
            session, created = Session.objects.get_or_create(
                id = session_data.get("id"),
                defaults = {
                    "user": user,
                    "start_time": session_data.get("start_time"),
                    "end_time": session_data.get("end_time"),
                    "visibility": session_data.get("visibility"),
                    "notes": session_data.get("notes")
                }
            )

            if created:
                synced_ids.append(session.id)
            else:
                skipped_ids.append(session.id)

    return {
        "synced": synced_ids,
        "skipped": skipped_ids
    }


def sync_catches_from_payload(user, payload):
    created_catches = []
    synced_ids = []
    skipped_ids = []
    affected_species = set()

    with transaction.atomic():
        for catch_data in payload.get("catches", []):
            catch, created = Catch.objects.get_or_create(
                id = catch_data.get("id"),
                defaults = {
                    "user": user,
                    "species_id": catch_data.get("species_id"),
                    "session_id": catch_data.get("session_id"),
                    "location": catch_data.get("location"),
                    "time_caught": catch_data.get("time_caught"),
                    "weight_kg": catch_data.get("weight_kg"),
                    "length_m": catch_data.get("length_m"),
                }
            )
            if created:
                affected_species.add(catch.species_id)
                created_catches.append(catch)
                synced_ids.append(str(catch.id))
            else:
                skipped_ids.append(str(catch.id))

    update_stats(user, created_catches)
    stats = UserSpeciesStats.objects.filter(
        user=user,
        species_id__in = affected_species
    )

    return {
        "synced": synced_ids,
        "skipped": skipped_ids,
        "stats": stats,
    }

def update_stats(user, catches):
    catches_by_species = {}

    # Grouping catches together by species
    for catch in catches:
        print(catch)
        species_id = catch.species_id
        if species_id not in catches_by_species:
            catches_by_species[species_id] = []
        catches_by_species[species_id].append(catch)

    # Looping through species and updating stats
    for species_id, species_catches in catches_by_species.items():
        stats, _ = UserSpeciesStats.objects.get_or_create(
            user=user,
            species_id=species_id,
        )

        stats.total_caught += len(species_catches)

        if stats.first_catch is None:
            stats.first_catch = min(species_catches, key=lambda c: c.time_caught)

        heaviest = max((c for c in species_catches if c.weight_kg), key=lambda c: c.weight_kg, default=None)
        longest = max((c for c in species_catches if c.length_m), key=lambda c: c.length_m, default=None)

        if heaviest:
            if stats.max_weight_catch is None or heaviest.weight_kg > stats.max_weight_catch.weight_kg:
                stats.max_weight_catch = heaviest

        if longest:
            if stats.max_length_catch is None or longest.length_m > stats.max_length_catch.length_m:
                stats.max_length_catch = longest

        stats.save()