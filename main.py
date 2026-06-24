"""
main.py — CLI demo for PawPal+.

Creates two pets, loads them with tasks, and prints today's schedule for each.
Run with:  python3 main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_divider(char: str = "─", width: int = 52) -> None:
    print(char * width)


def run_demo() -> None:
    # ------------------------------------------------------------------ #
    # Set up owner
    # ------------------------------------------------------------------ #
    owner = Owner(
        name="Jordan",
        available_minutes=90,
        preferred_start_time="08:00",
    )

    # ------------------------------------------------------------------ #
    # Pet 1: Biscuit the dog
    # ------------------------------------------------------------------ #
    biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
    biscuit.add_task(Task("Morning walk",      30, priority="high",   recurring=True))
    biscuit.add_task(Task("Feeding",           10, priority="high",   recurring=True))
    biscuit.add_task(Task("Medication",         5, priority="high",   recurring=True,
                          notes="1 tablet with food"))
    biscuit.add_task(Task("Enrichment puzzle", 20, priority="medium"))
    biscuit.add_task(Task("Grooming",          40, priority="low",    notes="Focus on ears"))
    owner.add_pet(biscuit)

    # ------------------------------------------------------------------ #
    # Pet 2: Mochi the cat  (shorter available window)
    # ------------------------------------------------------------------ #
    mochi_owner = Owner(
        name="Jordan",
        available_minutes=45,
        preferred_start_time="09:30",
    )
    mochi = Pet(name="Mochi", species="cat", breed="Domestic Shorthair", age_years=5)
    mochi.add_task(Task("Feeding",          10, priority="high",  recurring=True))
    mochi.add_task(Task("Litter box clean", 10, priority="high",  recurring=True))
    mochi.add_task(Task("Playtime",         20, priority="medium", notes="Feather wand"))
    mochi.add_task(Task("Brushing",         15, priority="low"))
    mochi_owner.add_pet(mochi)

    # ------------------------------------------------------------------ #
    # Print schedules
    # ------------------------------------------------------------------ #
    print()
    print_divider("═")
    print("  🐾  PawPal+ — Today's Schedule")
    print_divider("═")

    for pet, sched_owner in [(biscuit, owner), (mochi, mochi_owner)]:
        scheduler = Scheduler(sched_owner, pet)
        plan = scheduler.generate_plan()
        explanation = scheduler.explain_plan(plan["scheduled"], plan["skipped"])
        print()
        print_divider()
        print(explanation)
        print_divider()

    print()


if __name__ == "__main__":
    run_demo()
