/*
 * Dummy contest page behaviour: problem switching, tabs, mock run/submit.
 * No real judging happens here — the gRPC services in ../project are where
 * the investigation takes place.
 */
(function () {
  "use strict";

  const problems = window.PROBLEMS || [];
  const statementEl = document.getElementById("statement");
  const editorEl = document.querySelector(".editor");
  const toastEl = document.getElementById("toast");
  const drafts = {}; // per-problem editor drafts (kept in memory + localStorage)
  let currentId = null;
  let toastTimer = null;

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function storageKey(id) {
    return "dummyrank-draft-" + id;
  }

  function saveDraft() {
    if (currentId === null) return;
    drafts[currentId] = editorEl.value;
    try {
      localStorage.setItem(storageKey(currentId), editorEl.value);
    } catch (e) {
      /* storage unavailable (e.g. file:// in some browsers) — ignore */
    }
  }

  function loadDraft(id) {
    if (drafts[id] !== undefined) return drafts[id];
    try {
      return localStorage.getItem(storageKey(id)) || "";
    } catch (e) {
      return "";
    }
  }

  // Placeholder for a section whose content is only available from a service.
  function hiddenSection(title, what, rpc, problemId) {
    return (
      "<h3>" + title + "</h3>" +
      '<div class="hidden-constraints">' +
      "<p>🔒 <strong>Hidden.</strong> The " + what + " for this problem " +
      "is not published on this page. Query <code>" + rpc + "</code> with " +
      "<code>problem_id = " + problemId + "</code> to reveal it.</p>" +
      "</div>"
    );
  }

  function renderProblem(problem) {
    statementEl.innerHTML =
      '<div class="statement-header">' +
      "<h2>" + escapeHtml(problem.title) + "</h2>" +
      '<div class="statement-meta">' +
      '<span class="difficulty difficulty-' + problem.difficulty.toLowerCase() + '">' +
      escapeHtml(problem.difficulty) + "</span>" +
      "<span>Max Score: " + problem.maxScore + "</span>" +
      "<span>Success Rate: " + escapeHtml(problem.successRate) + "</span>" +
      '<span class="problem-id-chip">problem_id: ' + problem.id + "</span>" +
      "</div></div>" +
      '<div class="statement-body">' + problem.statementHtml + "</div>" +
      hiddenSection("Input Format", "input structure and format",
        "TopologyService.DescribeStructure", problem.id) +
      "<h3>Output Format</h3>" + problem.outputFormat +
      hiddenSection("Constraints", "set of limits and edge cases",
        "ConstraintService.GetConstraints", problem.id) +
      hiddenSection("Sample Test Cases", "set of worked examples",
        "OracleService.RunTest (with your own small test)", problem.id);
  }

  function selectProblem(id) {
    const problem = problems.find(function (p) { return p.id === id; });
    if (!problem) return;
    saveDraft();
    currentId = id;

    document.querySelectorAll(".problem-item").forEach(function (li) {
      li.classList.toggle("active", Number(li.dataset.problem) === id);
    });

    renderProblem(problem);
    editorEl.value = loadDraft(id);
    selectTab("problem");
    if (location.hash !== "#" + problem.slug) {
      history.replaceState(null, "", "#" + problem.slug);
    }
  }

  function selectTab(name) {
    document.querySelectorAll(".tab").forEach(function (t) {
      t.classList.toggle("active", t.dataset.tab === name);
    });
    document.querySelectorAll(".tab-pane").forEach(function (pane) {
      pane.classList.toggle("active", pane.id === "tab-" + name);
    });
  }

  function showToast(message) {
    toastEl.textContent = message;
    toastEl.classList.remove("hidden");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.classList.add("hidden");
    }, 3500);
  }

  // ---- wiring ----
  document.querySelectorAll(".problem-item").forEach(function (li) {
    li.addEventListener("click", function () {
      selectProblem(Number(li.dataset.problem));
    });
  });

  document.querySelectorAll(".tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      selectTab(tab.dataset.tab);
    });
  });

  editorEl.addEventListener("input", saveDraft);

  document.getElementById("run-btn").addEventListener("click", function () {
    showToast(
      "Dummy page: code is not executed. Test your hypothesis with " +
      "OracleService.RunTest (problem_id " + currentId + ")."
    );
  });

  document.getElementById("submit-btn").addEventListener("click", function () {
    showToast(
      "Dummy page: submissions are not judged. Validate your approach with " +
      "ValidationService.ValidateApproach (problem_id " + currentId + ")."
    );
  });

  // Initial problem: from URL hash if present, otherwise problem 1.
  const fromHash = problems.find(function (p) {
    return "#" + p.slug === location.hash;
  });
  selectProblem(fromHash ? fromHash.id : 1);
})();
