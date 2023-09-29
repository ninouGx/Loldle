document.addEventListener('DOMContentLoaded', function () {
  loadRepresentations();
  // Fetch and display representations immediately when the popup is opened
  fetchAndDisplayRepresentations();

  // Re-add the button's click event listener
  document.getElementById('getRepresentation').addEventListener('click', fetchAndDisplayRepresentations);
});

function fetchAndDisplayRepresentations() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const activeTab = tabs[0];
    chrome.scripting.executeScript({
      target: { tabId: activeTab.id },
      function: getSquareRepresentation
    }, (results) => {
      if (results && results[0] && results[0].result) {
        saveRepresentations(results[0].result);
        displayRepresentations(results[0].result);
      }
    });
  });
}

function getSquareRepresentation() {
  const answers = document.querySelectorAll('.classic-answer');
  const results = [];

  const EXACT = 'square-good';
  const ATLEAST = 'square-partial';
  const WRONG = 'square-bad';
  const BEFORE = 'square-inferior';
  const AFTER = 'square-superior';

  answers.forEach(answer => {
    const squares = answer.querySelectorAll('.square');
    const imageUrlElement = answer.querySelector('.square img');
    const imageUrl = imageUrlElement ? imageUrlElement.src : null;


    let representation = '';

    squares.forEach(square => {
      if (square.classList.contains(EXACT)) {
        representation += "🟩";
      } else if (square.classList.contains(ATLEAST)) {
        representation += "🟧";
      } else if (square.classList.contains(WRONG)) {
        representation += "🟥";
      } else if (square.classList.contains(BEFORE)) {
        representation += "⬇️";
      } else if (square.classList.contains(AFTER)) {
        representation += "⬆️";
      } else {
        representation += "❓";  // Unknown square type
      }
    });

    // Remove first square (always empty)
    results.push({ imageUrl, representation: representation.slice(1) });
  });
  console.log(results);
  return results.reverse();
}

function saveRepresentations(representations) {
  chrome.storage.local.set({ 'savedRepresentations': representations });
}

function loadRepresentations() {
  chrome.storage.local.get('savedRepresentations', function (data) {
    console.log(data.saveRepresentations);
    if (data.savedRepresentations) {
      displayRepresentations(data.savedRepresentations);
    }
  });
}

function displayRepresentations(representations) {
  const resultList = document.getElementById('resultsList');
  resultList.innerHTML = '';
  representations.forEach(rep => {
    const li = document.createElement('li');    

    li.textContent = rep.representation;
    resultList.appendChild(li);

    const img = document.createElement('img');
    img.src = rep.imageUrl;
    img.alt = "Champion image"
    img.classList.add('champ-icon');
    li.insertBefore(img, li.firstChild);

    const copyBtn = document.createElement('button');
    copyBtn.classList.add('copy-btn');
    copyBtn.textContent = 'Copy';
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(rep.representation);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => {
        copyBtn.textContent = 'Copy';
      }, 1000);
    });
    li.appendChild(copyBtn);
  });
}
