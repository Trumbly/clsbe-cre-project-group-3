Qualtrics.SurveyEngine.addOnReady(function () {
    var composition = "${lm://Field/4}";
    var packaging = "${lm://Field/7}";
    var base = "https://raw.githubusercontent.com/Trumbly/clsbe-cre-project-group-3/feature/qualtrics-survey/qualtrics/stimuli/img/";

    var filename;
    if (packaging === "Closed container") {
        filename = "closed-container.png";
    } else {
        var map = {
            "Sandwich + Water": "sandwich-water.png",
            "Sandwich + Coffee": "sandwich-coffee.png",
            "Sandwich + Coffee + Fruit": "sandwich-coffee-fruit.png"
        };
        filename = map[composition];
    }

    if (!filename) {
        return;
    }

    var container = this.getQuestionContainer();
    if (!container) {
        return;
    }
    var qText = container.querySelector(".QuestionText");
    if (!qText) {
        return;
    }

    var img = document.createElement("img");
    img.src = base + filename;
    img.alt = packaging === "Closed container" ? "Closed container" : composition;
    img.style.cssText = "max-width:320px;display:block;margin:0 auto 16px;";
    qText.insertBefore(img, qText.firstChild);
});
