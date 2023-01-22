import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import { itemData } from './ImgInfo';


let index: any;

const ImageGalery = () => {

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
                    />
                </ImageListItem>
            ))}
        </ImageList>
    </>
    );

}
export default ImageGalery;
