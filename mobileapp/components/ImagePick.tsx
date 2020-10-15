import React, {Component} from 'react';

import { Image, StyleSheet, Text, View, Button } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import base64 from 'react-native-base64'

export default class ImagePick extends Component {

      state = {
        selectedImage: null,
        blobUri: ""
      }
    
    

    openImagePickerAsync = async () => {
        let permissionResult = await ImagePicker.requestCameraRollPermissionsAsync();
    
        if (permissionResult.granted === false) {
          alert("Permission to access camera roll is required!");
          return;
        }
    
        let pickerResult = await ImagePicker.launchImageLibraryAsync();

        if (pickerResult.cancelled === true) {
          return;
        }
    
        this.setState({selectedImage: pickerResult.uri });
    
    }

    analyzeReceipt = async () => {
      console.log("Image: " + this.state.selectedImage);
      let analyzeReceiptURI = "http://api.mindee.net/products/expense_receipts/v2/predict";
      let key = "10d876c53787bdb0548ba9278918f407";

      let sas = "?sv=2019-02-02&ss=bfqt&srt=sco&sp=rwdlacup&se=2020-04-23T06:53:11Z&st=2020-01-30T23:53:11Z&spr=https&sig=Tj%2Fh4LqTIqvUhIi4tK2i84fW86sA9l7JPA0OaoTRPCU%3D";
      let storageUri = "https://katiareceiptappstorage.blob.core.windows.net/receiptpictures/" + 'receipt.jpg' + sas;
    
      if(this.state.selectedImage !== null){
        let uri = this.state.selectedImage;
        console.log("uploadAsFile", uri);
        let response = await fetch(uri);
        let blob = await response.blob();
        
        fetch(storageUri, {
          method: 'PUT',
          headers: {
            'Content-Type':'image/jpeg',
            "x-ms-date":Date.UTC.toString(),
            "x-ms-version":"2019-02-02",
            //"Content-Length": imageData.content,
            "x-ms-blob-type": "BlockBlob"
          },
          body: blob

        }).then((response) => console.log(JSON.stringify(response)))
        .catch((err) => {
          console.error(err);
          });
        

        //  var formdata = new FormData();
        //  formdata.append("file", blob);
 
        //  fetch(analyzeReceiptURI, {
        //    method: 'POST',
        //    headers: {
        //      'X-Inferuser-Token': key,
        //      'Content-Type': 'multipart/form-data'
        //    },
        //    body:formdata
        //  }).then((response) => console.log(JSON.stringify(response)))
        //  .catch((err) => {
        //    console.error(err);
        //   });
 
        }




 
 
    



      

    }

  
    
      render(){
        let imageView = null;
        let button = null;
        if (this.state.selectedImage !== null) {
          imageView =  <Image source={{ uri: this.state.selectedImage }} style={styles.thumbnail} />;
          button = <Button title="Analyze Receipt" onPress = {() => this.analyzeReceipt()}/>;
        }
        else{
          imageView = null;
          button = null;
        }
        return (
          <View style={styles.container}>
            {imageView}
            <Text>
              Choose Receipt
            </Text>
      
            <Button title="Pick a photo"
            onPress = {() => this.openImagePickerAsync()}/>
            {button}
          </View>
        );
      };
      
    
} 

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  thumbnail: {
    width: 300,
    height: 300,
    resizeMode: "contain"
  }
});