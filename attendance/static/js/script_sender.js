/**
{
  "serial": 104,
  "name": "Sidharth R",
  "email": "tornadoalert@gmail.com",
  "event": 1,
  "roll_no": 150101312,
  "selectedClasses": [
    {
      "end": "2017-09-02T09:00:00+05:30",
      "batch": 1,
      "start": "2017-09-02T08:00:00+05:30",
      "location": null,
      "name": "Microbiology",
      "department": 7
    },
    {
      "end": "2017-09-02T12:00:00+05:30",
      "batch": 1,
      "start": "2017-09-02T09:30:00+05:30",
      "location": null,
      "name": "Clinical postings",
      "department": 1
    },
    {
      "end": "2017-09-02T15:00:00+05:30",
      "batch": 1,
      "start": "2017-09-02T14:00:00+05:30",
      "location": null,
      "name": "Integrated teaching",
      "department": 1
    }
  ]
}
**/
/**

Serial No.,Reg No.,Name,Date,Class Missed,Time,Event,Semester
5,150101007,Ashwin,18th October 2017,Medicine,08:00 am to 09:00 am,1,
5,150101007,Ashwin,18th October 2017,Clinical postings,09:30 am to 12:30 pm,1,
5,150101007,Ashwin,18th October 2017,OBG,02:00 pm to 03:00 pm,1,

**/
// Payload
(function () {
  function createCSV (payload) {
    var lines = ["Serial No.,Reg No.,Name,Date,Class Missed,Time,Event,Semester"];
    payload.selectedClasses.forEach(function (el) {
      lines.push([payload.serial, payload.roll_no, payload.name, moment(el.start).format("Do MMMM YYYY"), el.name, moment(el.start).format("hh:mm a") + " to " + moment(el.end).format("hh:mm a"), events[payload.event], parseInt(batches[el.batch])].join(","));
    });
    return lines.join("\n");
  }

  var STATUS = document.getElementById('status');
  var BUTTON = document.getElementById('buttonTray_next');
  var DOWNLOAD = document.getElementById('download');
  var CSVDATA = "";
  BUTTON.addEventListener('click', function () {
    var flag = true;
    // Name
    var name = document.getElementById('name_text').value;
    if (!/^[A-Za-z !?]+$/.test(name)) {
      var err_ele = document.getElementById('name_validation');
      err_ele.innerHTML = "Please enter a valid name.";
      if (flag) {
        document.getElementById('viewport').scrollTop = err_ele.offsetTop - 56;
      }
      flag = false;
    }
    else {
      var err_ele = document.getElementById('name_validation');
      err_ele.innerHTML = "";
    }
    // Email
    var email = document.getElementById('email_email').value;
    if (!/^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/.test(email)) {
      var err_ele = document.getElementById('email_validation');
      err_ele.innerHTML = "Please enter a valid email address.";
      if (flag) {
        document.getElementById('viewport').scrollTop = err_ele.offsetTop - 56;
      }
      flag = false;
    }
    else {
      var err_ele = document.getElementById('email_validation');
      err_ele.innerHTML = "";
    }
    // Roll Number
    var rollnum = document.getElementById('rollnumber_number').value;
    if (!/^\d+$/.test(rollnum)) {
      var err_ele = document.getElementById('rollnumber_validation');
      err_ele.innerHTML = "Please enter a valid roll number.";
      if (flag) {
        document.getElementById('viewport').scrollTop = err_ele.offsetTop - 56;
      }
      flag = false;
    }
    else {
      var err_ele = document.getElementById('rollnumber_validation');
      err_ele.innerHTML = "";
    }
    // Serial Number
    var serial = document.getElementById('serialNumber_number').value + "";
    if (!/^\d+$/.test(serial)) {
      var err_ele = document.getElementById('serialNumber_validation');
      err_ele.innerHTML = "Please enter a valid serial number.";
      if (flag) {
        document.getElementById('viewport').scrollTop = err_ele.offsetTop - 56;
      }
      flag = false;
    }
    else {
      var err_ele = document.getElementById('serialNumber_validation');
      err_ele.innerHTML = "";
    }
    // Selected Classes
    var selectedClasses = Selected.getList();
    selectedClasses = selectedClasses.filter(function (el) {
      if (el) {
        return el;
      }
    });
    if (selectedClasses.length === 0) {
      var err_ele = document.getElementById('classes_validation');
      err_ele.innerHTML = "Please select the classes you have missed.";
      if (flag) {
        document.getElementById('viewport').scrollTop = err_ele.offsetTop - 56;
      }
      flag = false;
    }
    else {
      var err_ele = document.getElementById('classes_validation');
      err_ele.innerHTML = "";
    }
    // Events
    var event_ = Events();

    // Send if all valid
    if (flag) {
      // Construct payload Object
      var payload = {
        email: email,
        event: event_,
        name: name,
        roll_no: rollnum,
        selectedClasses: selectedClasses,
        serial: serial
      };
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("POST", '/attendance/class_data');
      xmlhttp.setRequestHeader("Content-Type", "application/json");
      xmlhttp.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          if (JSON.parse(this.responseText).success) {
            STATUS.innerHTML = "The claims have been sucessfully submitted.";
          }
          else {
            STATUS.innerHTML = "Something is Invalid with your claims.";
            BUTTON.removeAttribute('disabled');
          }
        }
        else if (this.readyState == 4 && this.status != 200) {
          STATUS.innerHTML = "Something went horribly wrong from our side. We'll look into it.";
        }
      };
      xmlhttp.send(JSON.stringify(payload));
      STATUS.innerHTML = "Processing your Claims.";
      BUTTON.setAttribute('disabled', true);

      // Create CSV
      CSVDATA = createCSV(payload);
      DOWNLOAD.innerHTML = `<p>If you'd like to download the excel format of these claims, you can do so here.</p><button id="download_link">Download</button>`;
      DOWNLOAD.querySelector('button').addEventListener('click', function () {
        var blob = new Blob([CSVDATA], {type: "text/plain;charset=utf-8"});
        saveAs(blob, "claims.csv");
      }, false);

      // Scroll down
      document.getElementById('viewport').scrollTop = document.getElementById('viewport').scrollHeight;
    }
  }, false);
})();
