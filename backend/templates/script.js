document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");
  const fileInput = document.getElementById("classroomImage");
  const markBtn = document.getElementById("markAttendanceBtn");
  const downloadBtn = document.getElementById("downloadBtn");
  const tbody = document.querySelector("#attendanceTable tbody");
  const totalSpan = document.getElementById("total");
  const presentSpan = document.getElementById("present");
  const absentSpan = document.getElementById("absent");

  fileInput.addEventListener("change", () => {
    markBtn.disabled = !fileInput.files.length;
  });

  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!fileInput.files.length) return;

    markBtn.disabled = true;
    markBtn.textContent = "Processing...";

    const fd = new FormData();
    fd.append("classroomImage", fileInput.files[0]);

    try {
      const res = await fetch("/mark_attendance", { method: "POST", body: fd });
      if (!res.ok) throw new Error("Server error");

      const data = await res.json();
      const attendance = data.attendance || [];

      tbody.innerHTML = "";
      attendance.forEach(student => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${student.name}</td><td>${student.rollNo}</td>
                        <td class="${student.status==='Present'?'present':'absent'}">${student.status}</td>`;
        tbody.appendChild(tr);
      });

      const total = attendance.length;
      const present = attendance.filter(s => s.status === 'Present').length;
      const absent = total - present;

      totalSpan.textContent = total;
      presentSpan.textContent = present;
      absentSpan.textContent = absent;

      if (data.download_path) {
        downloadBtn.style.display = "inline-block";
        downloadBtn.href = data.download_path;
      }

    } catch (err) {
      console.error(err);
      alert("Error marking attendance.");
    } finally {
      markBtn.disabled = false;
      markBtn.textContent = "Mark Attendance";
    }
  });
});
