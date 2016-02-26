var Contest = function(contestId, startTime, endTime) {
  this.contestId = contestId;
  this.startTime = startTime;
  this.endTime = endTime;
};

Contest.prototype.start = function() {
  new Progress(this, $("#progressbar"));
}

var Progress = function(contest, element) {
  this.contest = contest;
  this.element = element;

  setInterval(this.update.bind(this), 50);
};

function toInterval(time) {
  var seconds = time % 60;
  if (seconds < 10) seconds = "0" + seconds;
  time = Math.floor(time / 60);

  var minutes = time % 60;
  if (minutes < 10) minutes = "0" + minutes;
  time = Math.floor(time / 60);

  var hours = time % 24;
  if (hours < 10) hours = "0" + hours;
  time = Math.floor(time / 24);

  var days = time;
  var str = "";
  if (days) str += days + " days, ";
  str += hours + ":" + minutes + ":" + seconds;
  return str;
}

Progress.prototype.update = function() {
  var currentTime = new Date().getTime();
  var startTime = this.contest.startTime;
  var endTime = this.contest.endTime;

  var elapsed = Math.floor((currentTime - startTime) / 1000);
  var remaining = Math.floor((endTime - currentTime) / 1000);
  var percent = 100 * (currentTime - startTime) / (endTime - startTime);

  $("#progressbar-elapsed").text(toInterval(elapsed) + " elapsed");
  $("#progressbar-remaining").text(toInterval(remaining) + " left");
  $("#progressbar-inner").css('width', percent + '%');
  var style = percent >= 95 ? 'danger' : percent >= 85 ? 'warning' : 'success';
  $("#progressbar-inner").attr("class", "progress-bar progress-bar-" + style);
}
