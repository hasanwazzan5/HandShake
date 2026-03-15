document.addEventListener("DOMContentLoaded", function () {
  const habitForm = document.getElementById("habitForm");
  habitForm.addEventListener("submit", function (e) {
    e.preventDefault();

    habitName = document.getElementById("habitName").value;
    habitGoal = document.getElementById("habitGoal").value;
    daily = document.getElementById("daily").checked;
    weekly = document.getElementById("weekly").checked;

    if (habitName.length === 0 || habitGoal.length === 0) {
      alert("Please fill out all fields.");
      return;
    }

    async function submit() {
      const response = await fetch("/createhabit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          habit_name: habitName,
          goal: habitGoal,
          frequency: daily ? "daily" : "weekly",
        }),
      });
      const data = await response.json();
      if (data.success) {
        window.location.href = "/dashboard";
      }
    }

    submit();
  });
});
