import { Alert, Collapse, DialogTitle, IconButton } from '@mui/material';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import React from 'react';
import { useState } from 'react';
import { ImageType } from 'react-images-uploading';
import HomeP, { imgS } from '../../paths/pages/HomeP';

import SendAlert from './SendAlert';
import LeftSide from './LeftSide';
import RightSide from './RightSide';

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

function sendImgToBackend() {
  const formData = new FormData();
  console.log("send");
  formData.append('userImg', imgS[0].file);
  console.log(formData);
  fetch('https://roadsigns.p4m1.top/upload', {
      method: 'POST',
      body: formData,
    }).then((response) => {
      response.json().then((body) => {
        console.log(body);
      });
    });
}


var isNoPhotoSelected = false;

function SendPhoto() {
  const [open, setOpen] = useState(false);
  const [openAlert, setAlert] = useState(false);

  const handleOpen = () => {
    <Alert severity="info">No photo selected pleas select photo</Alert>

    if (imgS == null || imgS.length == 0) {
      isNoPhotoSelected = true
      console.log("no photo")
      console.log(isNoPhotoSelected)
      setAlert(true);
    }
    else if (imgS.length == 1) {
      sendImgToBackend();
      setAlert(false);
      setOpen(true);
    }
    // console.log(imgS[0].file);}

  }
  const handleClose = () => setOpen(false);

  return (
    <div>
      {/* {imgS.map((image:ImageType) => (
          <img src={image.dataURL} alt="" />
          ))} */}
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
