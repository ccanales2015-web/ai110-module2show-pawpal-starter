from datetime import date, datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pet Management")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
st.session_state.owner.name = owner_name
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(pet_name, species)
    st.session_state.owner.add_pet(pet)

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to your pets and manage their schedules.")

if not st.session_state.owner.pets:
    st.info("Add a pet before adding tasks.")
else:
    pets = st.session_state.owner.pets
    pet_index = st.selectbox(
        "Pet",
        range(len(pets)),
        format_func=lambda i: f"{pets[i].name} ({pets[i].species})",
    )
    selected_pet = pets[pet_index]
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_date = st.date_input("Date", value=date.today())
    with col3:
        task_time = st.time_input("Time", value=time(8, 0))
    col4, col5 = st.columns(2)
    with col4:
        frequency = st.selectbox("Frequency", ["none", "daily", "weekly"])
    with col5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        task = Task(
            task_title,
            datetime.combine(task_date, task_time),
            frequency=frequency,
            priority=priority,
        )
        selected_pet.add_task(task)

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "scheduled": f"{task.scheduled_at:%Y-%m-%d %H:%M}",
                "frequency": task.frequency,
                "priority": task.priority,
                "status": "completed" if task.completed else "pending",
            }
            for pet, task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a time-ordered plan and identify exact-time conflicts for the selected date.")

schedule_date = st.date_input("Schedule date", value=date.today())

if st.button("Generate schedule"):
    st.text(Scheduler(st.session_state.owner).explain_plan(schedule_date))
