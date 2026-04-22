Qualtrics.SurveyEngine.addOnReady(function () {
    var pressure = "${e://Field/pressure}";
    if (pressure !== "high") {
        return;
    }

    var totalSeconds = parseInt("${e://Field/timer_duration_s}", 10);
    if (isNaN(totalSeconds) || totalSeconds <= 0) {
        totalSeconds = 8;
    }

    var container = document.createElement("div");
    container.id = "cre-timer-bar";
    container.style.cssText =
        "position:fixed;top:0;left:0;width:100%;padding:10px;" +
        "text-align:center;font-weight:bold;background:#ffe9a8;" +
        "border-bottom:2px solid #d29a00;z-index:9999;";
    container.innerText = "Time left: " + totalSeconds + "s";
    document.body.appendChild(container);

    var nudge = document.createElement("div");
    nudge.id = "cre-timer-nudge";
    nudge.style.cssText =
        "position:fixed;top:48px;left:0;width:100%;padding:8px;" +
        "text-align:center;color:#fff;background:#c0392b;" +
        "display:none;z-index:9999;";
    nudge.innerText = "Please select quickly.";
    document.body.appendChild(nudge);

    var remaining = totalSeconds;
    var interval = setInterval(function () {
        remaining -= 1;
        if (remaining > 0) {
            container.innerText = "Time left: " + remaining + "s";
        } else {
            container.innerText = "Time up — please select.";
            nudge.style.display = "block";
            clearInterval(interval);
        }
    }, 1000);

    this.questionclick = function (event, element) {
        clearInterval(interval);
    };
});

Qualtrics.SurveyEngine.addOnUnload(function () {
    var bar = document.getElementById("cre-timer-bar");
    var nudge = document.getElementById("cre-timer-nudge");
    if (bar) bar.parentNode.removeChild(bar);
    if (nudge) nudge.parentNode.removeChild(nudge);
});
