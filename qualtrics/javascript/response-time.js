Qualtrics.SurveyEngine.addOnReady(function () {
    this._cre_startTimestamp = Date.now();
});

Qualtrics.SurveyEngine.addOnUnload(function () {
    var endTs = Date.now();
    var startTs = this._cre_startTimestamp || endTs;
    var rtMs = endTs - startTs;

    var loopIndex = "${lm://CurrentLoopNumber}";
    if (!loopIndex || loopIndex === "${lm://CurrentLoopNumber}") {
        loopIndex = "1";
    }

    Qualtrics.SurveyEngine.setEmbeddedData("rt_ms_" + loopIndex, rtMs);
});
