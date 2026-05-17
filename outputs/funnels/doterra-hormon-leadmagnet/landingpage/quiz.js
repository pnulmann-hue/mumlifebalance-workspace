/* ============================================================
   Hormon-Typ Quiz — Vanilla JS
   Patricia Ulmann · Mum Life Balance
   3 Typen: energie-raeuberin · mineral-maengelin · darm-detektivin
============================================================ */

(function () {
  'use strict';

  // -----------------------------------------------------------
  // Configuration
  // -----------------------------------------------------------

  // Set this in production to point at your AC backend.
  // For Netlify Forms fallback, keep null.
  const AC_API_ENDPOINT = null; // z.B. '/.netlify/functions/submit-to-ac'

  // -----------------------------------------------------------
  // Question Bank
  // Each option carries weights that increase one or more types.
  // -----------------------------------------------------------

  const QUESTIONS = [
    {
      eyebrow: 'Frage 1',
      text: 'Wie würdest du deine Energie HEUTE beschreiben?',
      options: [
        { label: 'Vollkommen am Limit', weights: { er: 3, mm: 1, dd: 0 } },
        { label: 'Mal so, mal so', weights: { er: 1, mm: 2, dd: 2 } },
        { label: 'Müde aber funktional', weights: { er: 1, mm: 3, dd: 1 } },
        { label: 'Eigentlich okay', weights: { er: 0, mm: 1, dd: 1 } },
      ],
    },
    {
      eyebrow: 'Frage 2',
      text: 'Welches Symptom trifft dich am stärksten?',
      options: [
        { label: 'Schlafprobleme — ich liege wach oder wache nachts auf', weights: { er: 3, mm: 1, dd: 0 } },
        { label: 'Haarausfall + Müdigkeit, die nicht weggeht', weights: { er: 1, mm: 3, dd: 1 } },
        { label: 'Stimmungsschwankungen — manchmal himmelhoch, manchmal tief', weights: { er: 1, mm: 0, dd: 3 } },
        { label: 'Heisshunger, Verdauung schwankt, Blähungen', weights: { er: 0, mm: 1, dd: 3 } },
      ],
    },
    {
      eyebrow: 'Frage 3',
      text: 'Wann hast du gemerkt, dass etwas nicht stimmt?',
      options: [
        { label: 'In den letzten Wochen — ist neu', weights: { er: 2, mm: 1, dd: 1 } },
        { label: 'Letzte Monate — hat sich aufgebaut', weights: { er: 1, mm: 2, dd: 1 } },
        { label: 'Über ein Jahr — ich kenn es schon', weights: { er: 2, mm: 1, dd: 2 } },
        { label: 'Vermute schon länger — hab nie hingeschaut', weights: { er: 1, mm: 1, dd: 2 } },
      ],
    },
    {
      eyebrow: 'Frage 4',
      text: 'Was hast du schon probiert?',
      options: [
        { label: 'Magnesium, Eisen aus der Drogerie — Standard-Supplements', weights: { er: 2, mm: 1, dd: 0 } },
        { label: 'Bluttest — alles "okay" laut Hausarzt', weights: { er: 1, mm: 3, dd: 0 } },
        { label: 'Diäten, Detox, Fasten', weights: { er: 0, mm: 1, dd: 2 } },
        { label: 'Noch gar nichts — bin gerade erst am Schauen', weights: { er: 1, mm: 1, dd: 1 } },
      ],
    },
    {
      eyebrow: 'Frage 5',
      text: 'Wie alt bist du?',
      options: [
        { label: 'Unter 30', weights: { er: 1, mm: 0, dd: 1 } },
        { label: '30-35', weights: { er: 1, mm: 1, dd: 1 } },
        { label: '36-42 (genau in der Vormenopause-Phase)', weights: { er: 2, mm: 2, dd: 1 } },
        { label: 'Über 42', weights: { er: 1, mm: 2, dd: 1 } },
      ],
    },
  ];

  // -----------------------------------------------------------
  // Type definitions (used for redirect)
  // -----------------------------------------------------------

  const TYPES = {
    er: { id: 'energie-raeuberin', label: 'Die Energie-Räuberin', file: 'result-energie-raeuberin.html' },
    mm: { id: 'mineral-maengelin', label: 'Die Mineral-Mängelin', file: 'result-mineral-maengelin.html' },
    dd: { id: 'darm-detektivin',  label: 'Die Darm-Detektivin',  file: 'result-darm-detektivin.html' },
  };

  // -----------------------------------------------------------
  // State
  // -----------------------------------------------------------

  let currentStep = 0;
  const answers = []; // each entry: { questionIndex, optionIndex, weights }

  // -----------------------------------------------------------
  // DOM References
  // -----------------------------------------------------------

  const quizContainer = document.getElementById('quizContainer');
  const emailContainer = document.getElementById('emailContainer');
  const questionEyebrow = document.getElementById('questionEyebrow');
  const questionText = document.getElementById('questionText');
  const optionsContainer = document.getElementById('optionsContainer');
  const progressFill = document.getElementById('progressFill');
  const currentStepLabel = document.getElementById('currentStep');
  const backBtn = document.getElementById('backBtn');
  const emailForm = document.getElementById('emailForm');
  const firstNameInput = document.getElementById('firstName');
  const emailInput = document.getElementById('email');
  const firstNameError = document.getElementById('firstNameError');
  const emailError = document.getElementById('emailError');
  const submitBtn = document.getElementById('submitBtn');
  const loadingState = document.getElementById('loadingState');

  // -----------------------------------------------------------
  // Render Question
  // -----------------------------------------------------------

  function renderQuestion(index) {
    const q = QUESTIONS[index];
    if (!q) return;

    questionEyebrow.textContent = q.eyebrow;
    questionText.textContent = q.text;

    optionsContainer.innerHTML = '';
    q.options.forEach((opt, optIdx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quiz-option';
      btn.textContent = opt.label;
      btn.addEventListener('click', () => handleAnswer(index, optIdx));
      optionsContainer.appendChild(btn);
    });

    // Update progress
    const progress = ((index + 1) / QUESTIONS.length) * 100;
    progressFill.style.width = progress + '%';
    currentStepLabel.textContent = (index + 1).toString();

    // Update back button
    backBtn.disabled = index === 0;

    // Refresh fade-in animation
    quizContainer.classList.remove('fade-in');
    void quizContainer.offsetWidth;
    quizContainer.classList.add('fade-in');
  }

  // -----------------------------------------------------------
  // Handle Answer
  // -----------------------------------------------------------

  function handleAnswer(questionIndex, optionIndex) {
    const q = QUESTIONS[questionIndex];
    const opt = q.options[optionIndex];

    // Persist answer (overwrite if user goes back and re-answers)
    answers[questionIndex] = {
      questionIndex,
      optionIndex,
      questionText: q.text,
      answerLabel: opt.label,
      weights: opt.weights,
    };

    // Visual feedback before transitioning
    Array.from(optionsContainer.children).forEach((btn, i) => {
      if (i === optionIndex) btn.classList.add('selected');
    });

    setTimeout(() => {
      if (questionIndex < QUESTIONS.length - 1) {
        currentStep = questionIndex + 1;
        renderQuestion(currentStep);
      } else {
        showEmailForm();
      }
    }, 350);
  }

  // -----------------------------------------------------------
  // Back Button
  // -----------------------------------------------------------

  backBtn.addEventListener('click', () => {
    if (currentStep > 0) {
      currentStep -= 1;
      renderQuestion(currentStep);
    }
  });

  // -----------------------------------------------------------
  // Show Email Form
  // -----------------------------------------------------------

  function showEmailForm() {
    quizContainer.style.display = 'none';
    emailContainer.style.display = 'block';
    emailContainer.classList.add('fade-in');
    document.querySelector('.quiz-progress').style.display = 'none';
  }

  // -----------------------------------------------------------
  // Compute Type
  // -----------------------------------------------------------

  function computeType() {
    const totals = { er: 0, mm: 0, dd: 0 };
    answers.forEach(a => {
      if (!a) return;
      Object.keys(a.weights).forEach(key => {
        totals[key] += a.weights[key];
      });
    });

    let topType = 'er';
    let topScore = -1;
    Object.keys(totals).forEach(key => {
      if (totals[key] > topScore) {
        topScore = totals[key];
        topType = key;
      }
    });

    return { type: topType, totals };
  }

  // -----------------------------------------------------------
  // Form Validation
  // -----------------------------------------------------------

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function clearErrors() {
    firstNameError.classList.remove('visible');
    emailError.classList.remove('visible');
  }

  // -----------------------------------------------------------
  // Form Submit
  // -----------------------------------------------------------

  emailForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    clearErrors();

    const firstName = firstNameInput.value.trim();
    const email = emailInput.value.trim();
    let valid = true;

    if (!firstName) {
      firstNameError.classList.add('visible');
      valid = false;
    }

    if (!email || !validateEmail(email)) {
      emailError.classList.add('visible');
      valid = false;
    }

    if (!valid) return;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Wird gesendet...';

    const result = computeType();
    const type = TYPES[result.type];

    // Persist for result page
    try {
      sessionStorage.setItem('hormonTyp', JSON.stringify({
        type: result.type,
        label: type.label,
        firstName,
        email,
        totals: result.totals,
        timestamp: new Date().toISOString(),
      }));
    } catch (_) {
      // sessionStorage might be blocked — that's ok, result page works without
    }

    const submissionData = {
      firstName,
      email,
      type: result.type,
      typeLabel: type.label,
      totals: result.totals,
      answers: answers.map(a => ({ q: a.questionText, a: a.answerLabel })),
      source: 'hormon-typ-quiz',
      timestamp: new Date().toISOString(),
    };

    try {
      await submitLead(submissionData);
    } catch (err) {
      // Even if backend fails, redirect — user got the experience
      console.error('Lead submission error:', err);
    }

    // Smooth UX: brief loading visual then redirect
    emailForm.style.display = 'none';
    loadingState.style.display = 'block';

    setTimeout(() => {
      window.location.href = type.file + '?n=' + encodeURIComponent(firstName);
    }, 1100);
  });

  // -----------------------------------------------------------
  // Backend Submission
  // -----------------------------------------------------------

  async function submitLead(data) {
    // Strategy 1: Custom AC API endpoint (Netlify Function)
    if (AC_API_ENDPOINT) {
      const response = await fetch(AC_API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error('AC API submission failed: ' + response.status);
      }
      return response.json();
    }

    // Strategy 2: Netlify Forms fallback (data captured in Netlify dashboard)
    const formData = new FormData();
    formData.append('form-name', 'hormon-typ-quiz');
    formData.append('firstName', data.firstName);
    formData.append('email', data.email);
    formData.append('type', data.type);
    formData.append('typeLabel', data.typeLabel);
    formData.append('answers', JSON.stringify(data.answers));
    formData.append('totals', JSON.stringify(data.totals));

    const response = await fetch('/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Netlify Forms submission failed: ' + response.status);
    }
  }

  // -----------------------------------------------------------
  // Init
  // -----------------------------------------------------------

  renderQuestion(0);
})();
