/* ================================= |
| SpaccCraftAPI                      |
| Licensed under AGPLv3 by OctoSpacc |
| ================================= */

const APIUrl = "/API";

function SubmitPoll() {
	let Form = document.getElementById("PollForm");

	Pass = Form.elements["Pass"].value;
	if (Pass != '') {
		Pass = Whirlpool(Pass);
	}

	let Data = {
		"Type": Form.elements["Type"].value,
		"Ref": Form.elements["Ref"].value,
		"User": Form.elements["User"].value,
		"Pass": Pass,
		"Vote": Form.elements["Vote"].value,
		"CustomText": Form.elements["CustomText"].value
	}

	let Req = new XMLHttpRequest();
	Req.onreadystatechange = function() {
		if (Req.readyState == 4) {
			alert(Req.response);
		}
	}
	Req.open("POST", APIUrl, true);
	Req.setRequestHeader("Content-type", "application/json");
	Req.send(JSON.stringify(Data));
}
