var app = new Vue({
        el: "#app",
        data:{
            name:'',
            url:'',
            interval:2,
            showmessage:false,
            objectid:'',
            errors:{
                name:false,
                url:false
            }
        },

        methods:{
            save:function(event){
                console.log("save button called ");
                data =  {
                    name: this.name,
                    url: this.url,
                    interval:Math.round(this.interval),
                    psid:document.getElementById('psid').value,
                    objectid : this.objectid,
                  };


                var endpoint = "/sitemonitor/add";
                axios.post(endpoint, data).then(function(response){
                    console.log(response);
                    if(response.data.message == "success"){

                        console.log(response.data.name);

                        setTimeout(function () {
                        app.$data.showmessage=true;
                        app.$data.objectid = response.data.objectid;
                        app.$data.url = response.data.url;

                        },500);


                    }
                    else{
                        console.log("error");
                        console.log(response.data.errors);
                        app.$data.errors = response.data.errors;
                    }


                });
            },
            addanother:function (event) {

                this.name='';
                this.url='';
                this.interval=2;
                this.objectid='';
                this.errors = {
                    name:false,
                    url:false
                }


                setTimeout(function () {
                    app.$data.showmessage = false;

                }, 500);
            },
            edit:function (event) {


                setTimeout(function () {
                    app.$data.showmessage = false;

                }, 500);
            },
            close:function (event) {
                MessengerExtensions.requestCloseBrowser(function success() {
                        console.log("Webview closing");
                    }, function error(err) {
                        console.log(err);
                    });
            }
        },
        watch:{
            interval:function(val){
                rounded_interval = Math.round(val);
                this.interval = Math.round(val);
                document.getElementById('id_interval_rounded').innerHTML = rounded_interval+" Mins.";
            }
        }


    })/**
 * Created by ruhshan on 5/6/18.
 */
