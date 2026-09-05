(function () {
  "use strict";

  const API_URL = "http://127.0.0.1:8000/predict";

  // --- Elements ---
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");

  const intakeStage = document.getElementById("intakeStage");
  const previewStage = document.getElementById("previewStage");
  const processingStage = document.getElementById("processingStage");
  const errorStage = document.getElementById("errorStage");
  const resultStage = document.getElementById("resultStage");

  const previewImg = document.getElementById("previewImg");
  const fileNameEl = document.getElementById("fileName");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const changeBtn = document.getElementById("changeBtn");
  const retryBtn = document.getElementById("retryBtn");
  const newCheckBtn = document.getElementById("newCheckBtn");

  const errorTitle = document.getElementById("errorTitle");
  const errorBody = document.getElementById("errorBody");

  const resultStamp = document.getElementById("resultStamp");
  const resultLabel = document.getElementById("resultLabel");
  const resultFile = document.getElementById("resultFile");
  const resultConfidence = document.getElementById("resultConfidence");

  let selectedFile = null;
  let previewObjectUrl = null;

  // --- Stage visibility helper ---
  function showStage(stage) {
    [intakeStage, previewStage, processingStage, errorStage, resultStage].forEach((el) => {
      el.hidden = el !== stage;
    });
  }

  // --- File selection handling ---
  function handleFileSelected(file) {
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      showError(
        "Unsupported file",
        "Please choose an image file (PNG or JPG). \u201c" + file.name + "\u201d doesn\u2019t look like an image."
      );
      return;
    }

    selectedFile = file;

    if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl);
    previewObjectUrl = URL.createObjectURL(file);
    previewImg.src = previewObjectUrl;
    fileNameEl.textContent = file.name;

    showStage(previewStage);
  }

  fileInput.addEventListener("change", (e) => {
    handleFileSelected(e.target.files[0]);
  });

  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });

  // --- Drag and drop ---
  ["dragenter", "dragover"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("is-dragover");
    });
  });

  ["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove("is-dragover");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    handleFileSelected(file);
  });

  // --- Change file / retry / new check ---
  changeBtn.addEventListener("click", () => {
    fileInput.value = "";
    selectedFile = null;
    showStage(intakeStage);
  });

  retryBtn.addEventListener("click", () => {
    if (selectedFile) {
      showStage(previewStage);
    } else {
      showStage(intakeStage);
    }
  });

  newCheckBtn.addEventListener("click", () => {
    fileInput.value = "";
    selectedFile = null;
    showStage(intakeStage);
  });

  // --- Error display ---
  function showError(title, body) {
    errorTitle.textContent = title;
    errorBody.textContent = body;
    showStage(errorStage);
  }

  // --- Analyze ---
  analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) {
      showError("No image selected", "Choose a signature image before analyzing.");
      return;
    }

    showStage(processingStage);

    const formData = new FormData();
    formData.append("file", selectedFile);

    let response;
    try {
      response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });
    } catch (networkErr) {
      showError(
        "Can\u2019t reach the server",
        "The backend at " + API_URL + " isn\u2019t responding. Make sure the FastAPI server is running, then try again."
      );
      return;
    }

    let data;
    try {
      data = await response.json();
    } catch (parseErr) {
      showError("Unexpected response", "The server response couldn\u2019t be read. Please try again.");
      return;
    }

    if (!response.ok) {
      showError(
        "Analysis failed",
        data && data.detail ? data.detail : "The server returned an error (" + response.status + ")."
      );
      return;
    }

    renderResult(data);
  });

  function renderResult(data) {
    const isReal = /real/i.test(data.prediction || "");

    resultLabel.textContent = isReal ? "REAL" : "FORGED";
    resultStamp.classList.toggle("is-forged", !isReal);

    resultFile.textContent = data.filename || selectedFile.name;
    resultConfidence.textContent =
      typeof data.confidence === "number" ? data.confidence.toFixed(2) + "%" : "\u2014";

    showStage(resultStage);
  }
})();
