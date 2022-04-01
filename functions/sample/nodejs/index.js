/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 const Cloudant = require('@cloudant/cloudant');

 function main(params) {
 
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
     let dealerships = getDealership(cloudant, params);
     return dealerships;
 }
 
 function getDealership(cloudant, params) {
     return new Promise(function (resolve, reject) {
         const dealershipDb = cloudant.use('dealerships'); //Database to use
         
         if (params.state) {
             // return dealership with this state
             dealershipDb.find({
                 "selector": {
                     "st": {
                         "$eq": params.state
                     }
                 }
             },function (err, result){
                 if (err) {
                     console.log("🚀 ~ function: get-dealership.js ~ line 35 ~ err", err)
                     reject(err);
                 }
                 let code=200; 
                 if (result.docs.length==0){
                     code= 404;
                 } 
                 resolve({
                     statusCode: code,
                     headers: { 'Content-Type': 'application/json' },
                     body: result
                 }); 
             }); 
         }else if (params.id) {
             id=parseInt(params.dealerId) 
             
             // return dealership with this state 
             dealershipDb.find({selector: {id:parseInt(params.id)}}, function (err, result) {
                 if (err){
                     console.log("🚀 ~ function: get-dealership.js ~ line 54 ~ err", err)
                     reject(err);
                 }
                 let code=200; 
                 if (result.docs.length==0){
                     code= 404;
                 }
                 resolve({
                     statusCode: code,
                     headers: { 'Content-Type': 'application/json' },
                     body: result
                 });
             });
        }else{
             // return all documents
             dealershipDb.list({ include_docs: true }, function (err, result) {
                 if (err) {
                     console.log("🚀 ~ function: get-dealership.js ~ line 71 ~ err", err)
                     reject(err);
                 }
                 resolve({
                     statusCode: 200,
                     headers: { 'Content-Type': 'application/json' },
                     body: result
                 });
             });
         } 
     }); 
 } 
 