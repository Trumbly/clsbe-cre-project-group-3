Qualtrics.SurveyEngine.addOnReady(function () {
    var composition = "${lm://Field/4}";
    var packaging = "${lm://Field/7}";
    var base = "https://raw.githubusercontent.com/Trumbly/clsbe-cre-project-group-3/feature/qualtrics-survey/qualtrics/stimuli/img/";

    var openMap = {
        "Sandwich + Water": "sandwich-water.png",
        "Sandwich + Coffee": "sandwich-coffee.png",
        "Sandwich + Coffee + Fruit": "sandwich-coffee-fruit.png"
    };
    // Closed container hides sandwich (and fruit, which fits inside). Drink
    // sits next to the container, so we still vary by coffee vs water.
    var closedMap = {
        "Sandwich + Water": "closed-container-water.png",
        "Sandwich + Coffee": "closed-container-coffee.png",
        "Sandwich + Coffee + Fruit": "closed-container-coffee.png"
    };

    var filename = packaging === "Closed container"
        ? closedMap[composition]
        : openMap[composition];

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
    img.alt = composition + " (" + packaging + ")";
    img.style.cssText = "max-width:320px;display:block;margin:0 auto 16px;";
    qText.insertBefore(img, qText.firstChild);
});
