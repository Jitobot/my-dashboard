// --- 時計 ---
function updateClock() {
    const now = new Date();
    const days = ["日", "月", "火", "水", "木", "金", "土"];
    const dateStr = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日(${days[now.getDay()]})`;
    const timeStr = now.toLocaleTimeString("ja-JP");
    document.getElementById("date").textContent = dateStr;
    document.getElementById("time").textContent = timeStr;
}
setInterval(updateClock, 1000);
updateClock();

// --- メモ ---
const memoEl = document.getElementById("memo");
const memoStatus = document.getElementById("memo-status");
let saveTimer = null;

async function loadMemo() {
    try {
        const res = await fetch("/api/memo");
        const data = await res.json();
        memoEl.value = data.content;
    } catch { /* empty */ }
}

async function saveMemo() {
    memoStatus.textContent = "保存中...";
    try {
        const res = await fetch("/api/memo", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: memoEl.value }),
        });
        memoStatus.textContent = res.ok ? "保存しました" : "保存に失敗しました";
    } catch {
        memoStatus.textContent = "保存に失敗しました";
    }
    setTimeout(() => { memoStatus.textContent = ""; }, 2000);
}

memoEl.addEventListener("input", () => {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveMemo, 1000);
});
loadMemo();

// --- ブックマーク ---
const bookmarkBar = document.getElementById("bookmark-bar");
const bmToggle = document.getElementById("bm-toggle");
const bmForm = document.getElementById("bookmark-form");
const bmIcon = document.getElementById("bm-icon");
const bmTitle = document.getElementById("bm-title");
const bmUrl = document.getElementById("bm-url");
const bmAdd = document.getElementById("bm-add");

bmToggle.addEventListener("click", () => {
    bmForm.classList.toggle("active");
});

async function loadBookmarks() {
    const res = await fetch("/api/bookmarks");
    const bookmarks = await res.json();
    // 既存のブックマークアイテムを削除（追加ボタンは残す）
    bookmarkBar.querySelectorAll(".bookmark-item").forEach((el) => el.remove());
    bookmarks.forEach((bm) => {
        const a = document.createElement("a");
        a.className = "bookmark-item";
        a.href = bm.url;
        a.target = "_blank";
        a.rel = "noopener";
        a.innerHTML = `<span class="bookmark-icon">${bm.icon}</span>${bm.title}`;
        const del = document.createElement("button");
        del.className = "bookmark-delete";
        del.textContent = "✕";
        del.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();
            await fetch(`/api/bookmarks/${bm.id}`, { method: "DELETE" });
            loadBookmarks();
        });
        a.appendChild(del);
        bookmarkBar.insertBefore(a, bmToggle);
    });
}

bmAdd.addEventListener("click", async () => {
    const title = bmTitle.value.trim();
    const url = bmUrl.value.trim();
    if (!title || !url) return;
    await fetch("/api/bookmarks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, url, icon: bmIcon.value.trim() || "🔗" }),
    });
    bmTitle.value = "";
    bmUrl.value = "";
    bmIcon.value = "";
    bmForm.classList.remove("active");
    loadBookmarks();
});
loadBookmarks();

// --- 天気 ---
const citySelect = document.getElementById("city-select");
const weatherCurrent = document.getElementById("weather-current");
const weatherHourly = document.getElementById("weather-hourly");

async function loadCities() {
    const res = await fetch("/api/weather/cities");
    const cities = await res.json();
    cities.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.textContent = c.name;
        citySelect.appendChild(opt);
    });
    const saved = localStorage.getItem("dashboard-city");
    if (saved) citySelect.value = saved;
}

async function loadWeather() {
    const city = citySelect.value;
    localStorage.setItem("dashboard-city", city);
    try {
        const res = await fetch(`/api/weather?city=${city}`);
        const data = await res.json();
        renderWeather(data);
    } catch {
        weatherCurrent.innerHTML = '<p class="placeholder">天気の取得に失敗しました</p>';
    }
}

function renderWeather(data) {
    weatherCurrent.innerHTML = `
        <span class="weather-icon">${data.weather_icon}</span>
        <span class="weather-temp">${data.temperature}°C</span>
        <span class="weather-detail">
            ${data.weather_label}<br>
            湿度 ${data.humidity}% / 風速 ${data.wind_speed}m/s
        </span>
    `;

    const now = new Date();
    const nowHour = now.getHours();
    const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;

    // 現在時刻以降のデータを抽出
    const upcoming = data.hourly.filter((h) => {
        const dt = new Date(h.time);
        return dt >= new Date(now.getFullYear(), now.getMonth(), now.getDate(), nowHour);
    });

    // コンテナの幅からアイテム数を計算（1アイテム約36px）
    const containerWidth = weatherHourly.clientWidth || 400;
    const itemWidth = 36;
    const maxItems = Math.floor(containerWidth / itemWidth);
    const display = upcoming.slice(0, maxItems);

    let lastDate = "";
    weatherHourly.innerHTML = display.map((h) => {
        const dt = new Date(h.time);
        const dateStr = `${dt.getFullYear()}-${String(dt.getMonth() + 1).padStart(2, "0")}-${String(dt.getDate()).padStart(2, "0")}`;
        const hour = String(dt.getHours()).padStart(2, "0") + ":00";
        const pct = h.precipitation_probability ?? 0;
        const barHeight = Math.max(pct * 0.5, 1);
        let dateSep = "";
        if (dateStr !== lastDate) {
            lastDate = dateStr;
            if (dateStr !== todayStr) {
                dateSep = `<span class="hourly-date-sep">明日</span>`;
            }
        }
        return `
            <div class="hourly-item">
                ${dateSep || `<span>${hour}</span>`}
                <span>${h.weather_icon}</span>
                <div class="hourly-bar-container">
                    <div class="hourly-bar" style="height:${barHeight}px"></div>
                </div>
                <span class="hourly-prob">${pct}%</span>
            </div>
        `;
    }).join("");
}

citySelect.addEventListener("change", loadWeather);
loadCities().then(loadWeather);
setInterval(loadWeather, 5 * 60 * 1000);

// --- Googleカレンダー ---
const calendarEvents = document.getElementById("calendar-events");
let calendarData = [];

async function loadCalendar() {
    try {
        const res = await fetch("/api/calendar/today");
        if (!res.ok) throw new Error();
        calendarData = await res.json();
        renderCalendar();
    } catch {
        calendarEvents.innerHTML = '<p class="auth-message">カレンダーを読み込めませんでした</p>';
    }
}

function renderCalendar() {
    const now = new Date();
    const nowMinutes = now.getHours() * 60 + now.getMinutes();

    // 終了時刻を過ぎた予定を除外（終日イベントは常に表示）
    const active = calendarData.filter((e) => {
        if (e.time === "終日") return true;
        const endStr = e.time.split(" - ")[1];
        if (!endStr) return true;
        const [h, m] = endStr.split(":").map(Number);
        return h * 60 + m > nowMinutes;
    });

    if (active.length === 0) {
        calendarEvents.innerHTML = '<p class="no-events">今日の予定はありません</p>';
        return;
    }
    calendarEvents.innerHTML = active.map((e) => `
        <div class="event-item">
            <span class="event-time">${e.time}</span>
            <span class="event-summary">${e.summary}</span>
        </div>
    `).join("");
}

loadCalendar();
setInterval(loadCalendar, 10 * 60 * 1000);
// 1分ごとに過去の予定を非表示にする
setInterval(renderCalendar, 60 * 1000);

// --- Google Tasks (ToDo) ---
const todoList = document.getElementById("todo-list");

async function loadTasks() {
    try {
        const res = await fetch("/api/calendar/tasks");
        if (!res.ok) throw new Error();
        const tasks = await res.json();
        if (tasks.length === 0) {
            todoList.innerHTML = '<p class="no-events">タスクはありません</p>';
            return;
        }
        todoList.innerHTML = "";
        tasks.forEach((t) => {
            const div = document.createElement("div");
            div.className = "todo-item";

            const cb = document.createElement("input");
            cb.type = "checkbox";
            cb.className = "todo-checkbox";
            cb.checked = t.done;
            cb.addEventListener("change", () => toggleTask(t, cb));

            const title = document.createElement("span");
            title.className = "todo-title" + (t.done ? " done" : "");
            title.textContent = t.title;

            const listName = document.createElement("span");
            listName.className = "todo-list-name";
            listName.textContent = t.list_name;

            div.appendChild(cb);
            div.appendChild(title);
            div.appendChild(listName);
            todoList.appendChild(div);
        });
    } catch {
        todoList.innerHTML = '<p class="auth-message">タスクを読み込めませんでした</p>';
    }
}

async function toggleTask(task, checkbox) {
    const titleEl = checkbox.nextElementSibling;
    checkbox.disabled = true;
    try {
        const res = await fetch("/api/calendar/tasks", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tasklist_id: task.tasklist_id,
                task_id: task.id,
                done: checkbox.checked,
            }),
        });
        if (res.ok) {
            titleEl.classList.toggle("done", checkbox.checked);
        } else {
            checkbox.checked = !checkbox.checked;
        }
    } catch {
        checkbox.checked = !checkbox.checked;
    }
    checkbox.disabled = false;
}

loadTasks();
setInterval(loadTasks, 10 * 60 * 1000);

// --- ニュース ---
const newsList = document.getElementById("news-list");

async function loadNews() {
    try {
        const res = await fetch("/api/news");
        if (!res.ok) throw new Error();
        const articles = await res.json();
        if (articles.length === 0) {
            newsList.innerHTML = '<p class="no-events">ニュースがありません</p>';
            return;
        }
        newsList.innerHTML = articles.map((a) => {
            const date = a.pub_date ? new Date(a.pub_date) : null;
            const timeStr = date ? `${date.getHours()}:${String(date.getMinutes()).padStart(2, "0")}` : "";
            return `<a class="news-item" href="${a.link}" target="_blank" rel="noopener">
                ${a.title}<span class="news-time">${timeStr}</span>
            </a>`;
        }).join("");
    } catch {
        newsList.innerHTML = '<p class="placeholder">ニュースの取得に失敗しました</p>';
    }
}

loadNews();
setInterval(loadNews, 15 * 60 * 1000);
