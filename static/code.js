var Age_ ,Sex_, Job_, Housing_, saving_account_, checking_account_, credit_amount_, duration_, purpose_;

$(document).ready(function(){
  // fetch all DOM elements for the input
  Age_ = document.getElementById("Age");
  Sex_ = document.getElementById("Sex");
  Job_ = document.getElementById("Job");
  Housing_ = document.getElementById("Housing");
  saving_account_ = document.getElementById("saving_account");
  checking_account_ = document.getElementById("checking_account");
  credit_amount_ = document.getElementById("credit_amount");
  duration_ = document.getElementById("duration");
  purpose_ = document.getElementById("purpose");
})

$(document).on('click','.button',function(e){
    // on clicking submit fetch values from DOM elements and use them to make request to our flask API
    var Age = Age_.value;
    var Sex = Sex_.value;
    var Job = Job_.value;
    var Housing = Housing_.value;
    var saving_account = saving_account_.value;
    var checking_account = checking_account_.value;
    var credit_amount = credit_amount_.value;
    var duration = duration_.value;
    var purpose = purpose_.value;
    if(Age == "2"){
      // you may allow it as per your model needs
      // you may mark some fields with * (star) and make sure they aren't empty here
      alert("empty fields not allowed");
    }
    else{
      // replace <username> with your pythonanywhere username
      // also make sure to make changes in the url as per your flask API argument names
      // var requestURL = "http://127.0.0.1:5000/predict?Age="+Age+"&Sex="+Sex+"&Job="+Job+"&Housing="+Housing+"&saving_account="+saving_account+"&checking_account="+checking_account+"&credit_amount="+credit_amount+"&duration="+duration+"&purpose="+purpose;
      // console.log(requestURL); // log the requestURL for troubleshooting
      
      // $.getJSON(requestURL, function(data) {
      //   console.log(data); // log the data for troubleshooting
      //   prediction = data['result'];
      //   $(".result").html("Prediction is: "+prediction);
      //   $(".result").css({
      //     "color": "#666666",
      //     "text-align": "center"
      //   });
      // });
      
      var data = {
          "Age": Age,
          "Sex": Sex, 
          "Job": Job, 
          "Housing": Housing, 
          "saving_account": saving_account, 
          "checking_account": checking_account, 
          "credit_amount": credit_amount, 
          "duration": duration, 
          "purpose": purpose
      };

      // # https://api.jquery.com/jquery.post/
      // # https://stackoverflow.com/questions/56032972/sending-a-dictionary-from-js-to-flask-via-ajax
      $.ajax({
        url: 'https://credit-scorer.herokuapp.com/predict',
        contentType: "application/json;charset=utf-8", 
        data: JSON.stringify({data}),
        dataType: "json",
        type: 'POST',
        success: function(response){
            // console.log(response);
            prediction = response['result'];
            $(".result").html("Prediction is: "+prediction);
            $(".result").css({
              "color": "#666666",
              "text-align": "center"
            });
        },
        error: function(error){
            console.log(error);
        }
    });
      // following lines consist of action that would be taken after the request has been read
      // for now i am just changing a <h2> tag's inner html using jquery
      // you may simple do: 
      // alert(prediction);
      e.preventDefault();
    }
  });
