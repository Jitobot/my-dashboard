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
