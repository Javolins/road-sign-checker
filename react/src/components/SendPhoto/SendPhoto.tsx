import { Alert } from '@mui/material';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import React from 'react';
import { useState } from 'react';
import { imgS } from '../../paths/pages/HomeP';

import SendAlert from './SendAlert';
import LeftSide from './LeftSide';
import RightSide from './RightSide';

export const index: number = 0;

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


function sendImgToBackend(openModal: any) {
  const formData = new FormData();
  console.log("send");
  formData.append('userImg', imgS[0].file);
  console.log(formData);
  fetch('https://roadsigns.p4m1.top/api/upload', {
    method: 'POST',
    body: formData,
  }).then((response) => {
    response.json().then((body) => {
      let uid = body.uid;
      console.log(uid);
      getImgInfoFromBackedn(openModal, uid);

    });
  });
}

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export let additionalInformationAboutImgProcesing:any;

async function getImgInfoFromBackedn(openModal: any, uid: any) {
  const sendToRCla =
  {
    uid
  }
  await delay(1000);
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
      openModal(true);
    });
  });
}


var isNoPhotoSelected = false;

function SendPhoto() {
  const [open, setOpen] = useState(false);
  const [openAlert, setAlert] = useState(false);

  const handleOpen = () => {
    <Alert severity="info">No photo selected pleas select photo</Alert>

    if (imgS === null || imgS.length === 0) {
      isNoPhotoSelected = true
      console.log("no photo")
      console.log(isNoPhotoSelected)
      setAlert(true);
    }
    else if (imgS.length === 1) {
      sendImgToBackend(setOpen);
      setAlert(false);
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
    </div>
  )
}
export default SendPhoto
