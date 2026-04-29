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
