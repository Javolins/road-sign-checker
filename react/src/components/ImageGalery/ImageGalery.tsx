import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';
import { itemData } from './ImgInfo';
import Button from '@mui/material/Button';
import { Dialog, DialogContent, DialogActions, DialogContentText } from '@mui/material';

const ImageGalery = () => {
    const [openDialog, setOpen] = React.useState(false);
    const closeDialogF = () => {
        setOpen(false);
    };

    const openDialogF = () => {
        setOpen(true);
    };
    return (<>
        <ImageList sx={{ margin: '0 auto' }} cols={4}>
            <ImageListItem key="Subheader" >
                <ListSubheader component="div">Rozpoznawane znaki:</ListSubheader>
            </ImageListItem>
            {itemData.map((item) => (
                <ImageListItem key={item.img}>
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
            ))}
        </ImageList> 
        <Dialog
                                    open={openDialog}
                                    onClose={closeDialogF}
                                    aria-describedby="alert-dialog-description"
                                >
                                    <DialogContent  >
                                        <DialogContentText id="alert-dialog-description">{item.info}
                                        </DialogContentText>
                                    </DialogContent>
                                    <DialogActions>
                                        <Button onClick={closeDialogF} autoFocus> exit</Button>
                                    </DialogActions>
                                </Dialog>
                                </>
    );

}
export default ImageGalery;
