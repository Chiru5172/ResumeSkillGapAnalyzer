/* ================= PIE CHART ================= */
const pieCtx = document.getElementById("skillPieChart");

if (pieCtx) {
    new Chart(pieCtx, {
        type: "pie",
        data: {
            labels: ["Matched Skills", "Missing Skills"],
            datasets: [{
                data: [window.matchedCount, window.missingCount],
                backgroundColor: ["#22c55e", "#ef4444"]
            }]
        }
    });
}

/* ================= BAR CHART ================= */
const barCtx = document.getElementById("skillBarChart");

if (barCtx) {
    new Chart(barCtx, {
        type: "bar",
        data: {
            labels: ["Extracted Skills", "Required Skills"],
            datasets: [{
                label: "Skill Count",
                data: [window.extractedCount, window.requiredCount],
                backgroundColor: ["#3b82f6", "#f59e0b"]
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

/* ================= LINE CHART ================= */
const lineCtx = document.getElementById("skillLineChart");

if (lineCtx) {
    const steps = window.missingCount + 1;

    let labels = [];
    let progressData = [];

    let start = window.matchedCount;
    let total = window.requiredCount;

    for (let i = 0; i <= steps; i++) {
        labels.push("Step " + i);
        let progress = Math.min(
            Math.round(((start + i) / total) * 100),
            100
        );
        progressData.push(progress);
    }

    new Chart(lineCtx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Readiness (%)",
                data: progressData,
                borderColor: "#6366f1",
                backgroundColor: "#6366f1",
                tension: 0.4,
                fill: false,
                pointRadius: 5
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
