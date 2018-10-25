// these are labels for the days of the week
cal_days_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// these are human-readable month name labels, in order
cal_months_labels = ['January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December'];

// these are the days of the week for each month, in order
cal_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
cal_current_date = new Date();
function Calendar(month, year) {
    this.month = (isNaN(month) || month == null) ? cal_current_date.getMonth() : month;
    this.year  = (isNaN(year) || year == null) ? cal_current_date.getFullYear() : year;
}
cal = new Calendar();
loggedIn = false;
function monthSelect() {
    let str = document.getElementById("month_select").value.split("/");
    let strs = document.getElementById("month_select").value;
    if(strs == "" || str[0] == "" || str.length != 2 || str[1].length != 4 || str[0].length > 2) {
        alert("Invalid Input");
        document.getElementById("month_select").value = "";
        return;
    }
    let month = Number(str[0]) - 1;
    let year = Number(str[1]);
    cal.month = month;
    cal.year = year;
    update(loggedIn);
}
document.getElementById("month_select_btn").addEventListener("click", monthSelect)
function update (loggedIn) {
    clearCalendar();
   
    document.getElementById('display_month').innerText = cal_months_labels[cal.month] + " " + cal.year;
    // get first day of month
    let firstDay = new Date(cal.year, cal.month, 1);
    let startingDay = firstDay.getDay();

    // find number of days in month
    let monthLength = cal_days_in_month[cal.month];

    // compensate for leap year
    if (cal.month == 1) { // February only!
        if((cal.year % 4 == 0 && cal.year % 100 != 0) || cal.year % 400 == 0){
            monthLength = 29;
        }
    }
    //html += '</tr><tr>';

    // fill in the days
    let day = 1;
    // this loop is for is weeks (rows)
    for (let i = 0; i < 9; i++) {
        // this loop is for weekdays (cells)
        let weekRow = document.createElement("tr");
        for (let j = 0; j <= 6; j++) {
            let dateCell = document.createElement("td");
            //html += '<td class="calendar-day">';
            if (day <= monthLength && (i > 0 || j >= startingDay)) {
                //html += day;
                dateCell.appendChild(document.createTextNode(day.toString()));
                //2018-08-09
                let date_id = cal.year.toString() + "-" + caseChange(cal.month + 1) +"-" +  caseChange(day);
                dateCell.setAttribute("id", date_id);
                dateCell.setAttribute("class", "editable");
                if(loggedIn) {
                    dateCell.addEventListener("dblclick", function() {
                        //alert(date_id);
                        $("#mydialog").show();
                        $("#time").show();				
                        $("#time_lb").show();
                        $("#save_btn").show();
                        $("#tag").hide();
                        $("#tag").removeAttr("readonly");
                        $("#tag_lb").hide();
                        $("#save_tags_btn").hide();
                        $("#save_changes_btn").hide();
                        $("#del_tag_btn").hide();
                        $("#title").show();
                        $("#title_lb").show();
                        //document.getElementById("edit_add_title").innerHTML = "Add Event on" + "hello";
                        document.getElementById("title").value = "";
                        document.getElementById("time").value = "";
                        
                        document.getElementById("date_id").value = date_id;
                        document.getElementById("edit_add_title").innerText =  date_id;
                        //createEvent(date_id);
                    });
                }
                weekRow.appendChild(dateCell);
                day++;
            } else {
                dateCell.appendChild(document.createTextNode(""));
                weekRow.appendChild(dateCell);
            }
            //html += '</td>';
        }
        document.getElementById("calendar_main").appendChild(weekRow);
        // stop making rows if we've run out of days
        if (day > monthLength) {
            break;
        }
        
    }
    if(loggedIn) {
        getEvent(cal.month, cal.year);
    }
}
function caseChange(a) {
    if(a < 10) {
        return "0" + a.toString();
    } else {
        return a.toString();
    }
}
function clearCalendar() {
    let main = document.getElementById("calendar_main");
    while (main.childNodes.length > 2) {
        main.removeChild(main.lastChild);
    }
}
//when you click the datecell, it can show the edit ui.
document.getElementById("close_dialog_btn").addEventListener("click", function() {
    $("#mydialog").hide();
})
document.getElementById("close_help_btn").addEventListener("click", function() {
    $("#help").hide();
})
document.getElementById("help_btn").addEventListener("click", function() {
    $("#help").show();
})
document.getElementById("next_month").addEventListener("click", function(){
    if(cal.month == 11) {
        cal.month = 0;
        cal.year = cal.year + 1;
    } else {
        cal.month = cal.month + 1;
    }
    update(loggedIn);

}, false);
// Change motn when the prev button is pressed
document.getElementById("prev_month").addEventListener("click", function(){
    if(cal.month == 0) {
        cal.month = 11;
        cal.year = cal.year - 1;
    } else {
        cal.month = cal.month - 1;
    }
    update(loggedIn);

}, false);
update(loggedIn);
function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }