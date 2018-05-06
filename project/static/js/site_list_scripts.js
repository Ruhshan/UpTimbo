/**
 * Created by ruhshan on 5/5/18.
 */

    var app = new Vue({
        el:"#app",
        data:{
            showform:false,
            name:'',
            url:'',
            interval:2,
            objectid:'',
            allsites:{},
            refetch:false,
            accordionindex:'',
            errors:{
                name:false,
                url:false,
            },
            errormessages:{},
        },
        created:function(){
          uid = window.location.pathname.split('/')[3]
          datasource = "/sitemonitor/api/v1/list/"+uid;
          axios.get(datasource).then( function(response) {
              allsites = response.data
              //app.$data.allsites = allsites;

              for(var i=0;i<allsites.length;i++){
                  if(allsites[i].isalive){
                      allsites[i].image = '/static/green_circle.png'
                  }else{
                      allsites[i].image = '/static/red_circle.png'
                  }

              }
              app.$data.allsites = allsites;

          });

        },


        methods:{
            togglemonitoring:function (e) {
                console.log(e);
            },
            update: function (e) {
                this.reset();

                data = {
                    name: this.name,
                    url: this.url,
                    interval: Math.round(this.interval),

                };
                // var csrftoken = Cookies.get('csrftoken');
                // console.log(csrftoken);
                var endpoint = "/sitemonitor/api/v1/update/"+this.objectid;

                // console.log(JSON.stringify(data));
                axios.patch(endpoint,data)
                    .then(function (response) {
                        console.log(response);
                        app.$data.refetch=true;
                        setTimeout(function(){app.$data.showform =false;}, 500);

                        UIkit.accordion(document.getElementById("listdiv")).toggle(app.$data.accordionindex);

                    })
                    .catch(function (error) {
                        //console.log(error);
                        app.$data.errormessages = error.response.data;
                    });


            },
            edit:function (site, index) {
                console.log(site.id);
                this.$data.name = site.name;
                this.$data.url = site.url;
                this.$data.interval = site.interval;
                this.$data.objectid = site.id;
                this.$data.showform = true;
                this.accordionindex = index;



            },
            del:function (site, index) {
                UIkit.modal.confirm('Delete '+site.name+"?").then(function () {
                    data = {
                        isdeleted:true,
                        };
                    endpoint = "/sitemonitor/api/v1/update/"+site.id;
                    axios.patch(endpoint,data)
                        .then(function (response) {
                            console.log(response);
                            UIkit.accordion(document.getElementById("listdiv")).toggle(index);
                            setTimeout(function () {
                                app.$data.refetch = true;

                            }, 500);


                        })
                        .catch(function (error) {
                            console.log(error);
                        })

                }, function () {
                    console.log('Rejected.')
                });
            },
            cancel: function (e) {
                setTimeout(function(){app.$data.showform =false;}, 500);
                UIkit.accordion(document.getElementById("listdiv")).toggle(app.$data.accordionindex);

            },
            reset:function () {
                console.log("reset called");
                this.errors.name=false;
                this.errors.url=false;
            },


        },
        watch:{
            interval:function(val){
                rounded_interval = Math.round(val);
                this.interval = Math.round(val);
                document.getElementById('id_interval_rounded').innerHTML = rounded_interval+" Mins.";
            },
            errormessages:function (val) {
                if(val.name){
                    this.errors.name=true;
                }
                if(val.url){
                    this.errors.url=true;
                }

            },
            refetch: function (val) {
                if (val == true) {
                    console.log("refetching");
                    uid = window.location.pathname.split('/')[3]
                    datasource = "/sitemonitor/api/v1/list/" + uid;
                    axios.get(datasource).then(function(response) {
                        app.$data.allsites = response.data;
                });
                    this.refetch=false;
                }

            },

        }

    });