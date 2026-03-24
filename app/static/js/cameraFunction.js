const snapBtn = document.getElementById("snap");
const video = document.querySelector("#video");
const canvas = document.querySelector("#canvas");
const saveBtn = document.getElementById("save");
const againBtn = document.getElementById("tryagain");

const modalA = new bootstrap.Modal("#myModal");
const modalB = new bootstrap.Modal("#otherModal");

let modalStream = null;
let capturedBlob = null;
let selectedHabitId = null;
let selectedHabitName = null;
const habitStatsDataElement = document.getElementById("habitStatsData");
const habitSubmissionsDataElement = document.getElementById("habitSubmissionsData");
const habitStats = habitStatsDataElement
  ? JSON.parse(habitStatsDataElement.textContent || "{}")
  : {};
const habitSubmissions = habitSubmissionsDataElement
  ? JSON.parse(habitSubmissionsDataElement.textContent || "{}")
  : {};

function formatDateForDisplay(dateObj) {
  const day = String(dateObj.getDate()).padStart(2, "0");
  const month = String(dateObj.getMonth() + 1).padStart(2, "0");
  const year = String(dateObj.getFullYear()).slice(-2);
  return `${day}/${month}/${year}`;
}

function renderStatisticsForHabit(habitId, habitName) {
  const statsHabitNameEl = document.getElementById("statsHabitName");
  const currentStreakEl = document.getElementById("currentStreakValue");
  const longestStreakEl = document.getElementById("longestStreakValue");
  const totalCompletionsEl = document.getElementById("totalCompletionsValue");
  const completionRateEl = document.getElementById("completionRateValue");
  const submissionBodyEl = document.getElementById("statsSubmissionBody");
  const nextSubmissionDueEl = document.getElementById("nextSubmissionDue");

  if (!submissionBodyEl) {
    return;
  }

  const habitKey = habitId ? String(habitId) : "";
  const stats = habitStats[habitKey] || {};
  const submissions = habitSubmissions[habitKey] || [];

  if (statsHabitNameEl) {
    statsHabitNameEl.textContent = habitName || stats.habit_name || "Habit";
  }
  if (currentStreakEl) {
    currentStreakEl.textContent = `${stats.current_streak ?? 0} Days`;
  }
  if (longestStreakEl) {
    longestStreakEl.textContent = `${stats.longest_streak ?? 0} Days`;
  }
  if (totalCompletionsEl) {
    totalCompletionsEl.textContent = String(stats.total_completions ?? submissions.length ?? 0);
  }
  if (completionRateEl) {
    completionRateEl.textContent = stats.completion_rate || "--";
  }
  if (nextSubmissionDueEl) {
    nextSubmissionDueEl.textContent = `Your next submission is due on ${stats.next_submission_due || "Placeholder due date"}.`;
  }

  if (!submissions.length) {
    submissionBodyEl.innerHTML = '<tr><td colspan="3" class="text-center text-alt">No submission data yet</td></tr>';
    return;
  }

  submissionBodyEl.innerHTML = submissions
    .map((entry) => {
      const imageUrl = entry.image_url || "#";
      const status = entry.status || "Pending review";
      const date = entry.submission_date || "--/--/--";

      return `
        <tr>
          <td>${date}</td>
          <td><a href="${imageUrl}" class="text-info" target="_blank" rel="noopener noreferrer">View Image</a></td>
          <td><span class="badge bg-warning text-dark">${status}</span></td>
        </tr>
      `;
    })
    .join("");
}

function canvasToBlob(canvasElement) {
  return new Promise((resolve, reject) => {
    canvasElement.toBlob((blob) => {
      if (!blob) {
        reject(new Error("Failed to create image blob"));
        return;
      }
      resolve(blob);
    }, "image/png");
  });
}

async function submitCapturedImage() {
  if (!capturedBlob) {
    capturedBlob = await canvasToBlob(canvas);
  }

  if (!selectedHabitId) {
    throw new Error("Please choose a habit before submitting an image.");
  }

  const formData = new FormData();
  formData.append("file", capturedBlob, "image.png");
  formData.append("habit_id", String(selectedHabitId));

  const response = await fetch("/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Upload failed");
  }

  return response.json();
}

function loadCamera() {
  // This one requests access to the camera, and displays the stream.
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        modalStream = stream;
        video.srcObject = stream;
        video.play();
      })
      .catch(function (err) {
        console.error("Camera access blocked: ", err);
      });
  }
}

if (snapBtn && againBtn && saveBtn && video && canvas) {
  snapBtn.addEventListener("click", async function () {
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    capturedBlob = await canvasToBlob(canvas);

    setTimeout(() => {
      modalA.hide();
      modalB.show();
    }, 50);
  });

  againBtn.addEventListener("click", function () {
    capturedBlob = null;
    modalB.hide();
    modalA.show();
  });

  saveBtn.addEventListener("click", async function () {
    try {
      const uploadResult = await submitCapturedImage();
      const habitKey = selectedHabitId ? String(selectedHabitId) : null;

      if (habitKey) {
        if (!habitSubmissions[habitKey]) {
          habitSubmissions[habitKey] = [];
        }

        habitSubmissions[habitKey].unshift({
          submission_date: formatDateForDisplay(new Date()),
          image_url: uploadResult.image_url || "#",
          status: "Pending review",
        });

        if (!habitStats[habitKey]) {
          habitStats[habitKey] = {};
        }
        habitStats[habitKey].total_completions = habitSubmissions[habitKey].length;

        renderStatisticsForHabit(selectedHabitId, selectedHabitName);
      }

      const habitLabel = selectedHabitName ? ` for ${selectedHabitName}` : "";
      alert("Picture was sent successfully" + habitLabel + "!");
      modalB.hide();
    } catch (error) {
      alert("Request failed: " + error.message);
    }
  });
}

const statsModal = document.getElementById("statsModal");
const sendSubmissionBtn = document.getElementById("sendSubmissionBtn");
if (statsModal && sendSubmissionBtn) {
  statsModal.addEventListener("show.bs.modal", function (event) {
    const triggerBtn = event.relatedTarget;
    selectedHabitId = triggerBtn ? triggerBtn.getAttribute("data-habit-id") : null;
    selectedHabitName = triggerBtn ? triggerBtn.getAttribute("data-habit-name") : null;
    renderStatisticsForHabit(selectedHabitId, selectedHabitName);
  });
}

document
  .getElementById("myModal")
  .addEventListener("hidden.bs.modal", function () {
    if (modalStream) {
      modalStream.getTracks().forEach((track) => track.stop());
    }
    modalStream = null;
    capturedBlob = null;
    video.srcObject = null;
  });
