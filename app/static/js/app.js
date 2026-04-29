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
    } catch {
        // 初回はまだデータがない場合がある
    }
}

async function saveMemo() {
    memoStatus.textContent = "保存中...";
    try {
        const res = await fetch("/api/memo", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: memoEl.value }),
        });
        if (res.ok) {
            memoStatus.textContent = "保存しました";
        } else {
            memoStatus.textContent = "保存に失敗しました";
        }
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

    const now = new Date().getHours();
    const upcoming = data.hourly.filter((h) => {
        const hour = parseInt(h.time.split(":")[0], 10);
        return hour >= now;
    }).slice(0, 12);

    weatherHourly.innerHTML = upcoming.map((h) => {
        const pct = h.precipitation_probability ?? 0;
        const barHeight = Math.max(pct * 0.4, 1);
        return `
            <div class="hourly-item">
                <span>${h.time}</span>
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
