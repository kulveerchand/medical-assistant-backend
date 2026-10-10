
const API_URL = "http://127.0.0.1:8000";

const userId = localStorage.getItem("user_id");
const username = localStorage.getItem("username") || "User";
const email = localStorage.getItem("email") || "";

const validUser =
    userId &&
    Number.isInteger(Number(userId)) &&
    Number(userId) > 0;

if (!validUser) {
    window.location.replace("index.html");
}

const pageDetails = {
    home: ["Dashboard", "Your personal wellness space"],
    chat: ["AI Medical Assistant", "Chat with your assistant"],
    history: ["Chat History", "Your saved conversations"],
    diet: ["Daily Diet", "Plan and record your meals"],
    routine: ["Daily Routine", "Track your daily activities"],
    doctors: ["Doctors", "Doctor information"],
    patient: ["Patient Profile", "Patient details"],
    availability: ["Doctor Availability", "Doctor schedules"],
    appointments: ["Appointments", "Appointment records"],
    "medical-history": ["Medical History", "Patient medical records"]
};

document.addEventListener("DOMContentLoaded", () => {
    if (!validUser) return;

    setText("profileName", username);
    setText("profileEmail", email);
    setText("welcomeName", `Welcome back, ${username}!`);
    setText("avatar", username.charAt(0).toUpperCase() || "U");

    setupNavigation();
    setupLogout();
    setupChat();
    setupChatHistory();
    setupDietForm();
    setupRoutineForm();

    setupDoctorLookup();
    setupPatientProfile();
    setupAvailabilityLookup();
    setupAppointments();
    setupMedicalHistory();

    // Open the dashboard home panel on startup.
    showPanel("home");
});

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value ?? "";
}

function setStatus(id, message, isError = false) {
    const element = document.getElementById(id);
    if (!element) return;

    element.textContent = message;
    element.style.color = isError ? "#c0392b" : "#167d65";
}

async function apiRequest(path, options = {}) {
    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers: {
            ...(options.body
                ? { "Content-Type": "application/json" }
                : {}),
            ...options.headers
        }
    });

    const text = await response.text();
    let data = {};

    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = { detail: text };
        }
    }

    if (!response.ok) {
        const detail = data.detail || data.message || "Request failed.";

        throw new Error(
            typeof detail === "string"
                ? detail
                : JSON.stringify(detail)
        );
    }

    return data;
}

// Safely display API responses without inserting HTML from the server.
function renderResult(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.replaceChildren();

    const records = Array.isArray(data)
        ? data
        : data && typeof data === "object"
            ? [data]
            : [];

    if (records.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty";
        empty.textContent = "No records found.";
        container.appendChild(empty);
        return;
    }

    records.forEach((record, index) => {
        const card = document.createElement("article");
        card.className = "history-item";

        const title = document.createElement("strong");
        title.textContent = `Record ${index + 1}`;
        card.appendChild(title);

        if (record && typeof record === "object") {
            Object.entries(record).forEach(([key, value]) => {
                const line = document.createElement("p");
                const label = document.createElement("strong");

                label.textContent =
                    key.replace(/_/g, " ") + ": ";

                line.appendChild(label);

                const valueText =
                    value === null || value === undefined
                        ? "—"
                        : typeof value === "object"
                            ? JSON.stringify(value)
                            : String(value);

                line.appendChild(document.createTextNode(valueText));
                card.appendChild(line);
            });
        } else {
            const line = document.createElement("p");
            line.textContent = String(record);
            card.appendChild(line);
        }

        container.appendChild(card);
    });
}

function setupNavigation() {
    document.querySelectorAll("[data-panel]").forEach(button => {
        button.addEventListener("click", () => {
            showPanel(button.dataset.panel);
        });
    });

    document.querySelectorAll("[data-go]").forEach(button => {
        button.addEventListener("click", () => {
            showPanel(button.dataset.go);
        });
    });
}

function showPanel(panelId) {
    if (!pageDetails[panelId]) return;

    document.querySelectorAll(".panel").forEach(panel => {
        panel.classList.toggle("active", panel.id === panelId);
    });

    document.querySelectorAll("[data-panel]").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.panel === panelId
        );
    });

    setText("pageTitle", pageDetails[panelId][0]);
    setText("pageSubtitle", pageDetails[panelId][1]);

    if (panelId === "history") loadChatHistory();
}

function setupLogout() {
    const button = document.getElementById("logoutBtn");
    if (!button) return;

    button.addEventListener("click", () => {
        localStorage.removeItem("user_id");
        localStorage.removeItem("username");
        localStorage.removeItem("email");
        window.location.replace("index.html");
    });
}

// -------------------- AI CHAT --------------------

function addChatMessage(message, sender) {
    const chatBox = document.getElementById("chatBox");
    if (!chatBox) return;

    const bubble = document.createElement("div");
    bubble.className = `chat-message ${sender}`;
    bubble.textContent = String(message);

    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function setupChat() {
    const form = document.getElementById("chatForm");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const input = document.getElementById("chatInput");
        const sendButton = document.getElementById("sendBtn");
        if (!input) return;

        const message = input.value.trim();
        if (!message) return;

        addChatMessage(message, "user");
        input.value = "";

        if (sendButton) sendButton.disabled = true;
        setStatus("chatStatus", "Waiting for the AI assistant...");

        try {
            const data = await apiRequest("/chat", {
                method: "POST",
                body: JSON.stringify({
                    user_id: Number(userId),
                    message
                })
            });

            const answer =
                data.response ??
                data.answer ??
                data.message ??
                "The assistant returned no response.";

            addChatMessage(answer, "bot");
            setStatus("chatStatus", "");
        } catch (error) {
            setStatus(
                "chatStatus",
                "Chat error: " + error.message,
                true
            );
        } finally {
            if (sendButton) sendButton.disabled = false;
            input.focus();
        }
    });
}

// -------------------- CHAT HISTORY --------------------

function setupChatHistory() {
    const button = document.getElementById("loadHistoryBtn");
    if (button) button.addEventListener("click", loadChatHistory);
}


async function loadChatHistory() {
    const list = document.getElementById("historyList");
    if (!list) return;

    list.replaceChildren();
    setStatus("historyStatus", "Loading chat history...");

    try {
        const data = await apiRequest(
            `/chat/history/${encodeURIComponent(userId)}`
        );

        console.log("Chat history API response:", data);

        const records = Array.isArray(data)
            ? data
            : data.history ?? data.chats ?? data.messages ?? [];

        if (!Array.isArray(records) || records.length === 0) {
            const empty = document.createElement("p");
            empty.className = "empty";
            empty.textContent = "No chat history found.";
            list.appendChild(empty);
            setStatus("historyStatus", "");
            return;
        }

        records.forEach(record => {
            const item = document.createElement("article");
            item.className = "history-item";

            const questionTitle = document.createElement("strong");
            questionTitle.textContent = "Your question";

            const question = document.createElement("p");
            question.textContent =
                record.message ??
                record.question ??
                record.user_message ??
                record.prompt ??
                "No question available";

            const answerTitle = document.createElement("strong");
            answerTitle.textContent = "Assistant response";

            const answer = document.createElement("p");
            answer.textContent =
                record.response ??
                record.answer ??
                record.ai_response ??
                record.assistant_message ??
                "No response available";

            item.append(
                questionTitle,
                question,
                answerTitle,
                answer
            );

            list.appendChild(item);
        });

        setStatus("historyStatus", "");
    } catch (error) {
        console.error("Chat history error:", error);
        setStatus("historyStatus", error.message, true);
    }
}


// -------------------- DIET --------------------

function setupDietForm() {
    const form = document.getElementById("dietForm");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const formData = new FormData(form);

        const payload = {
            user_id: Number(userId),
            breakfast: String(formData.get("breakfast") || "").trim(),
            lunch: String(formData.get("lunch") || "").trim(),
            dinner: String(formData.get("dinner") || "").trim(),
            water_intake: Number(formData.get("water_intake"))
        };

        if (
            !payload.breakfast ||
            !payload.lunch ||
            !payload.dinner ||
            !Number.isFinite(payload.water_intake) ||
            payload.water_intake < 0
        ) {
            setStatus("dietStatus", "Enter valid diet details.", true);
            return;
        }

        setStatus("dietStatus", "Saving diet...");

        try {
            const data = await apiRequest("/diet", {
                method: "POST",
                body: JSON.stringify(payload)
            });

            setStatus(
                "dietStatus",
                data.message || "Diet saved successfully."
            );

            form.reset();
            await loadDietRecords();
        } catch (error) {
            setStatus("dietStatus", error.message, true);
        }
    });

    const loadButton = document.getElementById("loadDietBtn");
    if (loadButton) loadButton.addEventListener("click", loadDietRecords);
}

async function loadDietRecords() {
    try {
        const data = await apiRequest(`/diet/${encodeURIComponent(userId)}`);
        renderResult("dietRecords", data);
        setStatus("dietStatus", "");
    } catch (error) {
        setStatus("dietStatus", error.message, true);
    }
}

// -------------------- DAILY ROUTINE --------------------

function setupRoutineForm() {
    const form = document.getElementById("routineForm");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const formData = new FormData(form);

        const payload = {
            user_id: Number(userId),
            wake_up_time: String(formData.get("wake_up_time") || ""),
            exercise: String(formData.get("exercise") || "").trim(),
            sleep_hours: Number(formData.get("sleep_hours")),
            activity: String(formData.get("activity") || "").trim(),
            notes: String(formData.get("notes") || "").trim()
        };

        if (
            !payload.wake_up_time ||
            !payload.exercise ||
            !payload.activity ||
            !Number.isFinite(payload.sleep_hours) ||
            payload.sleep_hours < 0 ||
            payload.sleep_hours > 24
        ) {
            setStatus("routineStatus", "Enter valid routine details.", true);
            return;
        }

        setStatus("routineStatus", "Saving routine...");

        try {
            const data = await apiRequest("/routine", {
                method: "POST",
                body: JSON.stringify(payload)
            });

            setStatus(
                "routineStatus",
                data.message || "Routine saved successfully."
            );

            form.reset();
            await loadRoutineRecords();
        } catch (error) {
            setStatus("routineStatus", error.message, true);
        }
    });

    const loadButton = document.getElementById("loadRoutineBtn");
    if (loadButton) {
        loadButton.addEventListener("click", loadRoutineRecords);
    }
}

async function loadRoutineRecords() {
    try {
        const data = await apiRequest(`/routine/${encodeURIComponent(userId)}`);
        renderResult("routineRecords", data);
        setStatus("routineStatus", "");
    } catch (error) {
        setStatus("routineStatus", error.message, true);
    }
}

// -------------------- DOCTOR LOOKUP --------------------

function setupDoctorLookup() {
    const form = document.getElementById("doctorForm");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const id = document.getElementById("doctorUserId")?.value;
        if (!id || Number(id) <= 0) {
            setStatus("doctorStatus", "Enter a valid doctor/user ID.", true);
            return;
        }

        setStatus("doctorStatus", "Loading doctor information...");

        try {
            const data = await apiRequest(
                `/doctor/${encodeURIComponent(id)}`
            );
            renderResult("doctorResult", data);
            setStatus("doctorStatus", "");
        } catch (error) {
            setStatus("doctorStatus", error.message, true);
        }
    });
}

// -------------------- PATIENT PROFILE --------------------

function setupPatientProfile() {
    const form = document.getElementById("patientForm");
    if (!form) return;

    const idInput = document.getElementById("patientUserId");
    if (idInput && !idInput.value) idInput.value = userId;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const id = idInput?.value;
        if (!id || Number(id) <= 0) {
            setStatus("patientStatus", "Enter a valid patient/user ID.", true);
            return;
        }

        setStatus("patientStatus", "Loading patient profile...");

        try {
            const data = await apiRequest(
                `/patient-profile/${encodeURIComponent(id)}`
            );
            renderResult("patientResult", data);
            setStatus("patientStatus", "");
        } catch (error) {
            setStatus("patientStatus", error.message, true);
        }
    });
}

// -------------------- DOCTOR AVAILABILITY --------------------

function setupAvailabilityLookup() {
    const form = document.getElementById("availabilityForm");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const id = document.getElementById("availabilityDoctorId")?.value;
        if (!id || Number(id) <= 0) {
            setStatus("availabilityStatus", "Enter a valid doctor ID.", true);
            return;
        }

        setStatus("availabilityStatus", "Loading availability...");

        try {
            const data = await apiRequest(
                `/doctor-availability/${encodeURIComponent(id)}`
            );
            renderResult("availabilityResult", data);
            setStatus("availabilityStatus", "");
        } catch (error) {
            setStatus("availabilityStatus", error.message, true);
        }
    });
}

// -------------------- APPOINTMENTS --------------------

function setupAppointments() {
    const form = document.getElementById("appointmentForm");
    if (!form) return;

    const typeSelect = document.getElementById("appointmentType");
    const idInput = document.getElementById("appointmentUserId");

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const id = idInput?.value;
        const type = typeSelect?.value || "patient";

        if (!id || Number(id) <= 0) {
            setStatus("appointmentStatus", "Enter a valid ID.", true);
            return;
        }

        const path = type === "doctor"
            ? `/appointments/doctor/${encodeURIComponent(id)}`
            : `/appointments/patient/${encodeURIComponent(id)}`;

        setStatus("appointmentStatus", "Loading appointments...");

        try {
            const data = await apiRequest(path);
            renderResult("appointmentResult", data);
            setStatus("appointmentStatus", "");
        } catch (error) {
            setStatus("appointmentStatus", error.message, true);
        }
    });
}

// -------------------- MEDICAL HISTORY --------------------

function setupMedicalHistory() {
    const form = document.getElementById("medicalHistoryForm");
    if (!form) return;

    const idInput = document.getElementById("medicalHistoryPatientId");
    if (idInput && !idInput.value) idInput.value = userId;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const id = idInput?.value;
        if (!id || Number(id) <= 0) {
            setStatus("medicalHistoryStatus", "Enter a valid patient ID.", true);
            return;
        }

        setStatus("medicalHistoryStatus", "Loading medical history...");

        try {
            const data = await apiRequest(
                `/medical-history/${encodeURIComponent(id)}`
            );
            renderResult("medicalHistoryResult", data);
            setStatus("medicalHistoryStatus", "");
        } catch (error) {
            setStatus("medicalHistoryStatus", error.message, true);
        }
    });
}
