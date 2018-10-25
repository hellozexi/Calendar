function getEvent(month, year) {
    fetch('/api/events/user', {
        method: "POST",
        body: JSON.stringify({ year: year, month: month + 1, csrf_token: csrf_token }),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        .then(function (res) {
            //console.log(res.events.length)
            for (let i = 0; i < res.events.length; i++) {
                let event_div = document.createElement("div");
                let strong = document.createElement("strong");
                //let more = false;
                strong.appendChild(document.createTextNode(res.events[i].event_time.substring(11,16)));
                event_div.appendChild(strong);
                event_div.appendChild(document.createTextNode(res.events[i].event_name));
                event_div.setAttribute("class", "event");
                event_div.setAttribute("id", res.events[i].event_id);
                getTag(res.events[i].event_id);
                //render a event by using this edit button
                let event_edit = document.createElement("a");
                //let event_edit = document.createElement("button");
                event_edit.appendChild(document.createTextNode("edit"));
                //event_edit.setAttribute("class", "btn btn-xs")
                event_edit.setAttribute("type", "button");
                event_edit.addEventListener("click", function() {
                    renderEvent(res.events[i].event_id, res.events[i].event_time, res.events[i].event_name);
                    //console.log("event" + res.events[i].json);
                    //alert("edit!!!");
                })
                //delete a event by using this delete button
                //let event_delete = document.createElement("button");
                let event_delete = document.createElement("a");

                event_delete.appendChild(document.createTextNode("del"));
                //event_delete.setAttribute("class", "btn btn-xs")
                event_delete.setAttribute("type", "button");
                event_delete.addEventListener("click", function() {
                    let del = confirm("Are you sure to delete this event?")
                    if(del == true) {
                        deleteEvent(res.events[i].event_id);
                    } 
                    //alert("delete!!!");
                })
                event_div.appendChild(event_edit);
                event_div.appendChild(event_delete);
                let res_day = res.events[i].event_time.substring(0, 10);
                document.getElementById(res_day).appendChild(event_div);
            }

        })
        .catch(error => console.error('Error:', error))
}

function createEvent(dates) {
    let title = document.getElementById("title").value;
    let reg_event = /^[a-zA-Z0-9_]+$/;
        if(!reg_event.exec(title)) {
            alert("Please enter your event title again");
            return;
        }
    let date = dates.split("-");
    let year = Number(date[0]);
    let month = Number(date[1]) - 1;
    let day = Number(date[2]);
    let time = document.getElementById("time").value.split(":");
    let dec = document.getElementById("time").value.split(".");
    let hour = Number(time[0]);
    let minute = Number(time[1]);
    if(hour > 23 || hour < 0 || minute > 60 || minute < 0 || !hour || !minute || dec.length >=2) {
        alert("invalid time");
        return;
    }
    fetch('/api/events/create', {
        method: "POST",
        body: JSON.stringify({ event_name: title, event_time: new Date(year, month, day, hour - 5, minute, 0), csrf_token: csrf_token}),
        headers: { "Content-Type": "application/json; charset=utf-8" }
    })
        .then(res => res.json())
        
        .then(function(res) {
            console.log(res["msg"]);
            if (res["code"] == 201) {
                document.getElementById("title").value = "";
                //document.getElementById("date_id").value = "";
                document.getElementById("time").value = "";
				update(loggedIn);
			}
        })
        .catch(error => console.error('Error:', error));
}
document.getElementById("save_btn").addEventListener("click", function(){
    let date_id = document.getElementById("date_id").value;
    createEvent(date_id);
});

function renderEvent(event_id, time, event) {
    document.getElementById("edit_add_title").innerText = "Update Event"
    if(event != null) {
        document.getElementById("title").value = event;
    } 
    if(time != null) {
        document.getElementById("date_id").value = time.substring(0,10);
        document.getElementById("time").value = time.substring(11,16);
    }
    if(event_id != null) {
        document.getElementById("id").value = event_id;
    } 
    $("#mydialog").show();
    $("#time").show();
    document.getElementById("edit_add_title").innerText = document.getElementById("date_id").value;
    $("#time_lb").show();
    $("#save_btn").hide();
    $("#tag").removeAttr("readonly");
    $("#save_changes_btn").show();
    $("#title").show();
    $("#title_lb").show();
    $("#del_tag_btn").hide();
    $("#tag").show();
    document.getElementById("tag").value = "";
    $("#tag_lb").show();
    $("#save_tags_btn").show();
}

function updateEvent() {
    let title = document.getElementById("title").value;
    let event_id = document.getElementById("id").value;
    let dates = document.getElementById("date_id").value;
    let date = dates.split("-");
    let year = Number(date[0]);
    let month = Number(date[1]) - 1;
    let day = Number(date[2]);
    let time = document.getElementById("time").value.split(":");
    let dec = document.getElementById("time").value.split(".");
    let hour = Number(time[0]);
    let minute = Number(time[1]);
    if(hour > 23 || hour < 0 || minute > 60 || minute < 0 || !hour || !minute || dec.length >=2) {
        alert("invalid time");
        return;
    }
    fetch('/api/events/update', {
        method: "POST",
        body: JSON.stringify({
            event_id: event_id,
            update_fields: {
                event_name: title,
                event_time:  new Date(year, month, day, hour - 5, minute, 0)
            },
            csrf_token: csrf_token
        }),
        headers: {"Content-Type": "application/json; charset=utf-8"}
        })
      .then(res => res.json())
      .then(function(res) {
          if(res["code"] == 200) {
              $("#mydialog").hide();
              update(loggedIn);
          }
      })
      //.then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:',error))
}
document.getElementById("save_changes_btn").addEventListener("click", updateEvent);

function deleteEvent(event_id) {
    fetch('/api/events/delete', {
        method: "POST",
        body: JSON.stringify({event_id: event_id, csrf_token: csrf_token}, ),
        headers: {"Content-Type": "application/json; charset=utf-8"}
        })
      .then(res => res.json())
      .then(function(res) {
          if(res["code"] == 200) {
              //alert("delete successful");
                $("#mydialog").hide();
                update(loggedIn);
          }
      }) 
      .catch(error => console.error('Error:',error))
}