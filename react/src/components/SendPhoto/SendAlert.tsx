import * as React from 'react';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';

export  function SendAlert(open:boolean, setOpen:any) {
  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert
        severity="error"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          There is no photo selected
        </Alert>
      </Collapse>
    </Box>
  );
}
export function SendAlertNoRecImg(open:boolean, setOpen:any) {
  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert
        severity="warning"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          Nie rozpoznano obrazu
        </Alert>
      </Collapse>
    </Box>
  );
}


export function SendAlertNoSignInDataBase(open:boolean, setOpen:any) {
  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert
        severity="warning"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          Nie ma zdjęcia na froncie wymaga kontaktu z devem
        </Alert>
      </Collapse>
    </Box>
  );
}


export function SendAlertBackendFuckUp(open:boolean, setOpen:any) {
  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert
        severity="warning"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          The back end bless you with no feed back enjoy you last secend
        </Alert>
      </Collapse>
    </Box>
  );
}

export function SendAlertNotRectangle(open:boolean, setOpen:any) {
  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert
        severity="error"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
            Zdjęcie musi byc łopatologiczno kwadratowe i tylko w proporcjach 1:1 co do pojedynczego piksela!!!
        </Alert>
      </Collapse>
    </Box>
  );
}

export function SendAlertToManyRequest(open:boolean, setOpen:any) {
  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert
        severity="error"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setOpen(false);
              }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
            Too many request!!! slow down babe
        </Alert>
      </Collapse>
    </Box>
  );
}