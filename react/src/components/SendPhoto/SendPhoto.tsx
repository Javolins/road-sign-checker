import { Alert } from '@mui/material';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import React from 'react';
import { useState } from 'react';
import { imgS } from '../../paths/pages/HomeP';

import { SendAlert, SendAlertBackendFuckUp, SendAlertNoSignInDataBase, SendAlertNotRectangle } from './SendAlert';
import { SendAlertNoRecImg } from './SendAlert';
import LeftSide from './LeftSide';
import RightSide from './RightSide';
import { itemData } from '../ImageGalery/ImgInfo';

export let index: number = 0;

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  fontFamily: 'Roboto',
  fontStyle: 'normal',
  transform: 'translate(-50%, -50%)',
  width: 650,
  bgcolor: 'background.paper',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
  display: 'flex',
  flexDirection: 'row',
  padding: '0',
};


function sendImgToBackend(openModal: any, setAlert2: any, setAlert3: any, setAlert4: any, setAlert5: any) {
  let formData = new FormData();
  formData.append('userImg', imgS[0].file);
  console.log("Photo to send");
  console.log(formData);
  fetch('https://roadsigns.p4m1.top/api/upload', {
    method: 'POST',
    body: formData,
  }).then((response) => {
    response.json().then((body) => {
      console.log('recive feedback:');
      console.log(body);
      if (body.info !== 'File successfully saved')
        setAlert5(true);
      else {
        let uid = body.uid;
        console.log(uid);
        retry_geting_feed_back = 0;
        getImgInfoFromBackedn(openModal, uid, setAlert2, setAlert3, setAlert4);

      }
    });
  });
}

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export let additionalInformationAboutImgProcesing: any;

let retry_geting_feed_back: number;

async function getImgInfoFromBackedn(openModal: any, uid: any, setAlert2: any, setAlert3: any, setAlert4: any) {
  const sendToRCla =
  {
    uid
  }
  await delay(1000 * (retry_geting_feed_back + 1));
  sendToRCla.uid = uid;
  let jsonString = JSON.stringify(sendToRCla);
  console.log(jsonString);
  const body = JSON.stringify(uid);
  console.log(body);
  fetch('https://roadsigns.p4m1.top/api/info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonString,
  }).then((response) => {
    response.json().then((body) => {
      // console.log("get fedback")
      console.log(body);
      additionalInformationAboutImgProcesing = body;
      // uid = body.uid;
      // console.log(uid);
      if (body.maskShape !== "ZnakShape.UNKNOWN") {
        index = findIndexOfPhotoName(body.classifiedType);
        if (body.info) {
          console.log(body.info);
          retry_geting_feed_back += 1;
          if (retry_geting_feed_back < 10)
            getImgInfoFromBackedn(openModal, uid, setAlert2, setAlert3, setAlert4);
          else
            setAlert4(true);
        }
        else {
          if (index !== -1)
            openModal(true);
          else
            setAlert3(true);
          console.log(body.classifiedType);
        }

        setAlert2(false);
      }
      else
        setAlert2(true);
    });
  });
}

function SendPhoto() {
  const [open, setOpen] = useState(false);
  const [openAlert, setAlert] = useState(false);
  const [openAlert2, setAlert2] = useState(false);
  const [openAlert3, setAlert3] = useState(false);
  const [openAlert4, setAlert4] = useState(false);
  const [openAlert5, setAlert5] = useState(false);

  const handleOpen = () => {
    // <Alert severity="info">No photo selected pleas select photo</Alert>

    if (imgS === null || imgS.length === 0) {
      console.log("no photo")
      setAlert(true);
    }
    else if (imgS.length === 1) {
      setAlert(false);
      sendImgToBackend(setOpen, setAlert2, setAlert3, setAlert4, setAlert5);
    }
  }
  const handleClose = () => setOpen(false);

  return (
    <div>
      <Button sx={{
        position: "absolute",
        bottom: "30px",
        left: "60px",
      }} variant="contained" onClick={handleOpen}>Send Photo</Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <LeftSide />
          <RightSide />
        </Box>
      </Modal>
      {SendAlert(openAlert, setAlert)}
      {SendAlertNoRecImg(openAlert2, setAlert2)}
      {SendAlertNoSignInDataBase(openAlert3, setAlert3)}
      {SendAlertBackendFuckUp(openAlert4, setAlert4)}
      {SendAlertNotRectangle(openAlert5, setAlert5)}
    </div>
  )
}
export default SendPhoto
function findIndexOfPhotoName(name: any): any {
  // throw new Error('Function not implemented.');
  const isname = (el: any) => el.title === name;
  const k = itemData.findIndex(isname);
  console.log(k);
  return k;
}

