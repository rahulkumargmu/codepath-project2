import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session-state initialisation
# Streamlit reruns this file on every interaction, so we guard with `not in`
# to avoid resetting objects that already exist in the session "vault".
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=120,
        preferred_start_time="08:00",
    )

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name="Mochi", species="cat")
    st.session_state.owner.add_pet(st.session_state.pet)

# ---------------------------------------------------------------------------
# Section 1 — Owner & Pet Setup
# ---------------------------------------------------------------------------
st.subheader("👤 Owner & Pet Setup")

with st.form("setup_form"):
    col_a, col_b = st.columns(2)

    with col_a:
        owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
        available_minutes = st.number_input(
            "Available minutes today",
            min_value=10,
            max_value=480,
            value=st.session_state.owner.available_minutes,
        )
        preferred_start = st.text_input(
            "Preferred start time (HH:MM)",
            value=st.session_state.owner.preferred_start_time,
        )

    with col_b:
        pet_name = st.text_input("Pet name", value=st.session_state.pet.name)
        species_options = ["dog", "cat", "other"]
        current_species = st.session_state.pet.species
        species_index = species_options.index(current_species) if current_species in species_options else 2
        species = st.selectbox("Species", species_options, index=species_index)
        breed = st.text_input("Breed (optional)", value=st.session_state.pet.breed)

    if st.form_submit_button("💾 Save profile"):
        # Preserve tasks already added to the old pet object
        existing_tasks = st.session_state.pet.get_tasks()
        new_owner = Owner(
            name=owner_name,
            available_minutes=int(available_minutes),
            preferred_start_time=preferred_start,
        )
        new_pet = Pet(name=pet_name, species=species, breed=breed)
        for t in existing_tasks:
            new_pet.add_task(t)
        new_owner.add_pet(new_pet)
        st.session_state.owner = new_owner
        st.session_state.pet = new_pet
        st.success(f"Profile saved: {owner_name} & {pet_name} ({species})")

st.divider()

# ---------------------------------------------------------------------------
# Section 2 — Add a Task
# ---------------------------------------------------------------------------
st.subheader("➕ Add a Task")

with st.form("task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        recurring = st.checkbox("Recurring daily")
    with col5:
        notes = st.text_input("Notes (optional)", value="")

    if st.form_submit_button("Add task"):
        new_task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            recurring=recurring,
            notes=notes,
        )
        st.session_state.pet.add_task(new_task)
        st.success(f"Added: {task_title}")

st.divider()

# ---------------------------------------------------------------------------
# Section 3 — Current task list
# ---------------------------------------------------------------------------
tasks = st.session_state.pet.get_tasks()
st.subheader(f"📋 {st.session_state.pet.name}'s Tasks ({len(tasks)} total)")

if tasks:
    for i, task in enumerate(tasks):
        col_t, col_d, col_p, col_s, col_btn = st.columns([3, 1, 1, 1, 1])
        col_t.write(("🔁 " if task.recurring else "") + f"**{task.title}**")
        col_d.write(f"{task.duration_minutes} min")
        col_p.write(task.priority)
        col_s.write("✅" if task.completed else "—")
        if not task.completed and col_btn.button("Done", key=f"done_{i}"):
            task.mark_complete()
            st.rerun()
else:
    st.info("No tasks yet — add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Section 4 — Generate Schedule
# ---------------------------------------------------------------------------
st.subheader("📅 Generate Today's Schedule")

if st.button("Generate schedule ▶", type="primary"):
    if not st.session_state.pet.get_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner, st.session_state.pet)
        plan = scheduler.generate_plan()
        scheduled = plan["scheduled"]
        skipped = plan["skipped"]

        m1, m2, m3 = st.columns(3)
        m1.metric("Scheduled", len(scheduled))
        m2.metric("Skipped", len(skipped))
        m3.metric(
            "Time used",
            f"{sum(t.duration_minutes for t in scheduled)} / "
            f"{st.session_state.owner.available_minutes} min",
        )

        if scheduled:
            st.markdown("#### ✅ Scheduled tasks")
            for task in scheduled:
                tag = "🔁 " if task.recurring else ""
                st.markdown(
                    f"- {tag}**{task.title}** — {task.duration_minutes} min "
                    f"`[{task.priority}]`"
                    + (f"  _{task.notes}_" if task.notes else "")
                )

        if skipped:
            st.markdown("#### ⏭ Skipped (time ran out)")
            for task in skipped:
                st.markdown(
                    f"- ~~{task.title}~~ — {task.duration_minutes} min "
                    f"`[{task.priority}]`"
                )

        with st.expander("📄 Full plan explanation"):
            explanation = scheduler.explain_plan(scheduled, skipped)
            st.code(explanation, language=None)
