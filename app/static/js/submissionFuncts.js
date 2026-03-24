document.addEventListener("DOMContentLoaded", function () {
  const habitForm = document.getElementById("habitForm");
  if (!habitForm) {
    return;
  }

  habitForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const habitName = document.getElementById("habitName").value.trim();
    const habitGoal = document.getElementById("habitGoal").value.trim();
    const daily = document.getElementById("daily").checked;

    if (habitName.length === 0 || habitGoal.length === 0) {
      alert("Please fill out all fields.");
      return;
    }

    async function submit() {
      try {
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
        if (response.ok && data.success) {
          window.location.href = data.redirect_url || "/dashboard";
          return;
        }

        alert(data.error || "Unable to create habit right now.");
      } catch (error) {
        alert("Unable to submit. Please try again.");
      }
    }

    submit();
  });
});
