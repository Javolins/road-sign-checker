import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';
import { itemData } from './ImgInfo';
import Button from '@mui/material/Button';
import { Dialog, DialogContent, DialogActions, DialogContentText, DialogTitle } from '@mui/material';

const ImageGalery = () => {
    const [openDialog, setOpen] = React.useState(false);
    const closeDialogF = () => {
        // console.log("plessss let me out")
        setOpen(false);
    };

    const openDialogF = () => {
        // console.log("ples open");
        setOpen(true);
    };
    return (<>
        <ImageList sx={{ margin: '0 auto' }} cols={4}>
            <ImageListItem key="Subheader" >
                <ListSubheader component="div">Rozpoznawane znaki:</ListSubheader>
            </ImageListItem>
            {itemData.map((item) => (
                <><ImageListItem key={item.img}>
                    <img
                        src={`${item.img}?w=248&fit=crop&auto=format`}
                        srcSet={`${item.img}?w=248&fit=crop&auto=format&dpr=4 2x`}
                        alt={item.title}
                        loading="lazy"
                    />
                    <ImageListItemBar
                        title={item.title}
                        // subtitle={item.author}
                        actionIcon={
                            <IconButton
                                sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                                aria-label={`info about ${item.title}`}
                                onClick={openDialogF}
                            >
                                <InfoIcon />
                            </IconButton>
                        }
                    />
                </ImageListItem>  
                <Dialog
                    open={openDialog}
                    onClose={closeDialogF}
                    aria-describedby="alert-dialog-description"
                >
                        <DialogTitle>{"Znak: "+item.title}</DialogTitle>
                        <DialogContent  >
                            <DialogContentText id="alert-dialog-description">{item.info}
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={closeDialogF}> exit</Button>
                        </DialogActions>
                    </Dialog>
                </>


            ))}
        </ImageList>

    </>
    );

}
export default ImageGalery;
