function toggleTheme() {
    const current =document.documentElement.getAttribute('data-theme');
    const next =current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeButton();
}

function updateThemeButton() {
    const theme =document.documentElement.getAttribute('data-theme');
    const btn =document.getElementById('theme-toggle');
    if (btn) btn.textContent =theme === 'dark' ? '☀️' : '🌙';
}

function getCookie(name) {
    let cookieValue =null;
    if (document.cookie && document.cookie !== '') {
        const cookies =document.cookie.split(';');
        for (let i =0; i < cookies.length; i++) {
            const cookie =cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue =decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function startTest() {
    const level =document.getElementById('level').value;
    const topic =document.getElementById('topic').value;

    let url =`/api/text/?level=${level}`;
    if (topic && topic !== '') url +=`&topic=${topic}`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.error) { alert('No texts found'); return; }
            localStorage.setItem('currentText', JSON.stringify(data));
            window.location.href = '/text/';
        })
        .catch(() => alert('Error loading text'));
}

let timerInterval =null;
let secondsSpent =0;
let startTime =0;

function startTimer(minutes) {
    let seconds =minutes * 60;
    const timerEl =document.getElementById('timer');
    if (!timerEl) return;

    if (timerInterval) clearInterval(timerInterval);

    startTime =Date.now();

    timerInterval =setInterval(() => {
        seconds--;
        const min =Math.floor(seconds / 60);
        const sec =seconds % 60;
        timerEl.textContent =`${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;

        if (seconds <= 60) timerEl.classList.add('warning');
        if (seconds <= 0) {
            clearInterval(timerInterval);
            submitAnswers();
        }
    }, 1000);
}

function loadText() {
    const data =JSON.parse(localStorage.getItem('currentText'));
    if (!data) { window.location.href ='/'; return; }

    document.getElementById('text-title').textContent =data.title;
    document.getElementById('text-content').textContent =data.content;
    document.getElementById('text-level').textContent =data.level.toUpperCase();
    document.getElementById('text-topic').textContent =data.topic;

    const container =document.getElementById('questions');
    container.innerHTML ='';

    if (!data.questions || data.questions.length === 0) {
        container.innerHTML ='<p>No questions available for this text.</p>';
        return;
    }

    data.questions.forEach((q, i) => {
        const div =document.createElement('div');
        div.className ='question';
        div.innerHTML =`
            <p>${i + 1}. ${q.question_text}</p>
            <label class="option"><input type="radio" name="q_${q.id}" value="a"> A. ${q.option_a}</label>
            <label class="option"><input type="radio" name="q_${q.id}" value="b"> B. ${q.option_b}</label>
            <label class="option"><input type="radio" name="q_${q.id}" value="c"> C. ${q.option_c}</label>
            <label class="option"><input type="radio" name="q_${q.id}" value="d"> D. ${q.option_d}</label>
        `;
        container.appendChild(div);
    });

    const timers ={ 'B1': 15, 'B2': 15, 'C1': 10, 'C2': 10 };
    startTimer(timers[data.level] || 15);
}
function loadUserLevel(){
    const levelSelect =document.getElementById('level');
    if(!levelSelect) return;
    fetch('/api/profile/')
         .then(res=> res.json())
         .then(data=> {
            if (data.level){
                levelSelect.value=data.level;
            }
         })
         .catch(()=>{})
}

function submitAnswers() {
    const data =JSON.parse(localStorage.getItem('currentText'));
    if (!data) return;

    if (timerInterval) clearInterval(timerInterval);

    secondsSpent =Math.round((Date.now() - startTime) / 1000);

    const answers ={};
    data.questions.forEach(q => {
        const sel =document.querySelector(`input[name="q_${q.id}"]:checked`);
        if (sel) answers[q.id] =sel.value;
    });

    fetch('/api/check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            text_id: data.id,
            answers: answers,
            time_spent: secondsSpent,
        })
    })
        .then(res => res.json())
        .then(result => {
            if (result.error) { alert('Error: ' + result.error); return; }
            localStorage.setItem('result', JSON.stringify(result));
            window.location.href ='/result/';
        })
        .catch(err => { console.error(err); alert('Error checking answers'); });
}

function loadResult() {
    const result =JSON.parse(localStorage.getItem('result'));
    if (!result) { window.location.href ='/'; return; }

    document.getElementById('correct').textContent =result.correct ?? 0;
    document.getElementById('wrong').textContent =result.wrong ?? 0;
    document.getElementById('percent').textContent =(result.percent ?? 0) + '%';

    const list = document.getElementById('mistakes');
    list.innerHTML ='';
    const mistakes =result.mistakes || [];

    if (mistakes.length === 0) {
        list.innerHTML ='<li style="background:#dcfce7;border-color:#16a34a;color:#14532d;">No mistakes. Excellent work!</li>';
    } else {
        mistakes.forEach(m => {
            const li =document.createElement('li');
            li.textContent =`${m.question_text} - correct: ${m.correct_answer.toUpperCase()}`;
            list.appendChild(li);
        });
    }
}

function loadVideos() {
    const grid =document.getElementById('videos-grid');
    if (!grid) return;

    fetch('/api/videos/')
        .then(res => res.json())
        .then(data => {
            grid.innerHTML ='';
            data.forEach(v => {
                const card =document.createElement(v.url ? 'a' : 'div');
                card.className ='news-card';
                if (v.url) {
                    card.href =v.url;
                    card.target ='_blank';
                    card.rel ='noopener noreferrer';
                }
                card.innerHTML = `
                    <span class="news-tag">${v.tag}</span>
                    <h3>${v.title}</h3>
                    <p>${v.description}</p>
                `;
                grid.appendChild(card);
            });
        })
        .catch(() => grid.innerHTML ='<p>Error loading videos</p>');
}

function loadDashboard() {
    const streakEl =document.getElementById('streak-value');
    if (!streakEl) return;

    fetch('/api/profile/')
        .then(res => res.json())
        .then(data => {
            document.getElementById('streak-value').textContent =data.streak || 0;
            document.getElementById('forecast-value').textContent =data.forecast_band || '-';
            document.getElementById('level-value').textContent =data.level || 'B1';
            document.getElementById('progress-text').textContent =data.total_tests || 0;

            const percent =Math.min((data.total_tests || 0) * 5, 100);
            document.getElementById('progress-fill').style.width =percent + '%';

            const st =document.getElementById('stat-tests');
            if (st) st.textContent = data.total_tests || 0;
            const sl =document.getElementById('stat-level');
            if (sl) sl.textContent =data.level || 'B1';
            const sp =document.getElementById('stat-percent');
            if (sp) sp.textContent = (data.avg_percent || 0) + '%';
            const ss =document.getElementById('stat-streak');
            if (ss) ss.textContent =data.streak || 0;

            const weak =data.weak_areas || [];
            const weakList =document.getElementById('weak-list');
            if (weakList) {
                if (weak.length === 0) {
                    weakList.innerHTML ='<p style="opacity:0.6;">No weak areas yet.</p>';
                } else {
                    weakList.innerHTML =weak.map(w => `
                        <div class="weak-item">
                            <span>${w.type}</span>
                            <span class="weak-count">${w.count} errors</span>
                        </div>
                    `).join('');
                }
            }

            if (data.achievements && data.achievements.length > 0) {
                const grid = document.getElementById('ach-grid');
                grid.innerHTML ='';
                data.achievements.forEach(a => {
                    const card = document.createElement('div');
                    card.className ='ach-card';
                    card.innerHTML =`<div class="ach-icon">${a.icon}</div><p>${a.title}</p>`;
                    grid.appendChild(card);
                });
            }
        })
        .catch(() => {});
}

function loadHistory() {
    const list =document.getElementById('history-list');
    if (!list) return;

    fetch('/api/history/')
        .then(res => res.json())
        .then(sessions =>{
            if (sessions.length === 0) {
                list.innerHTML ='<p style="opacity:0.6; text-align:center;">No tests yet.</p>';
                return;
            }
            list.innerHTML =sessions.map(s => `
                <div class="history-row">
                    <div>
                        <b>${s.text_title}</b>
                        <span class="badge">${s.text_level}</span>
                    </div>
                    <div class="history-right">
                        <span class="history-percent">${s.percent}%</span>
                        <span class="history-time">${s.time_spent}s</span>
                        <span class="history-date">${s.date}</span>
                    </div>
                </div>
            `).join('');
        });
}

function addWord() {
    const word =document.getElementById('word').value.trim();
    const translation =document.getElementById('translation').value.trim();
    const context =document.getElementById('context').value.trim();

    if (!word) { alert('Please enter a word'); return; }

    fetch('/api/vocabulary/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ word, translation, context })
    })
        .then(res =>res.json())
        .then(() =>{
            document.getElementById('word').value ='';
            document.getElementById('translation').value ='';
            document.getElementById('context').value ='';
            renderWords();
        });
}

function renderWords() {
    const list = document.getElementById('word-list');
    if (!list) return;

    fetch('/api/vocabulary/')
        .then(res => res.json())
        .then(words =>{
            const countEl = document.getElementById('vocab-count');
            if (countEl) countEl.textContent =words.length;

            list.innerHTML ='';
            if (words.length === 0) {
                list.innerHTML ='<p class="vocab-empty">No words yet. Add your first word above!</p>';
                return;
            }

            words.forEach(w => {
                const card = document.createElement('div');
                card.className ='vocab-card';
                card.innerHTML =`
                    <button class="vocab-delete" title="Delete">x</button>
                    <div class="vocab-word">${w.word}</div>
                    <div class="vocab-translation">${w.translation || '-'}</div>
                    ${w.context ? `<div class="vocab-context">"${w.context}"</div>`: ''}
                `;
                card.querySelector('.vocab-delete').onclick =() =>{
                    fetch(`/api/vocabulary/${w.id}/`, {
                        method: 'DELETE',
                        headers: { 'X-CSRFToken': getCookie('csrftoken') }
                    }).then(() =>renderWords());
                };
                list.appendChild(card);
            });
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const saved=localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeButton();

    const path = window.location.pathname;
    if(path === '/') loadVideos();
    if(path==='/test/') loadUserLevel();
    if(path === '/profile/') { loadDashboard(); loadHistory(); }
    if(path === '/text/') loadText();
    if(path === '/result/') loadResult();
    if(path === '/vocabulary/') renderWords();
});