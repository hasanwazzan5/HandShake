document.addEventListener("DOMContentLoaded", function () {
  const approveButtons = document.querySelectorAll(".approve-pair-btn");

  approveButtons.forEach(function (button) {
    button.addEventListener("click", async function () {
      const requestId = button.getAttribute("data-request-id");
      const newUserhabitId = button.getAttribute("data-new-userhabit-id");

      if (!requestId || !newUserhabitId) {
        alert("Missing request details.");
        return;
      }

      button.disabled = true;

      try {
        const response = await fetch("/accept_pair_request", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            request_id: Number(requestId),
            new_userhabit_id: Number(newUserhabitId),
          }),
        });

        const data = await response.json();
        if (response.ok && data.success) {
          window.location.href = data.redirect_url || "/pairingpage";
          return;
        }

        alert(data.error || "Unable to approve request.");
      } catch (error) {
        alert("Unable to approve request right now.");
      } finally {
        button.disabled = false;
      }
    });
  });
});
