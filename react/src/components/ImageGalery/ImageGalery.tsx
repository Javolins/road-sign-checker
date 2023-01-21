import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';

const ImageGalery = () => {

    return (
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
                            >
                                <InfoIcon />
                            </IconButton>
                        }
                    />
                </ImageListItem>
            ))}
        </ImageList>
    );

}
export default ImageGalery;

const itemData = [
    {
        img: 'https://znaki-drogowe.pl/img/ostrzegawcze/A-1-niebezpieczy-zakret-w-prawo.png',
        title: 'A-1',
    },
    {
        img: 'https://znaki-drogowe.pl/img/ostrzegawcze/A-2-niebezpieczny-zakret-w-lewo.png',
        title: 'A-2',
    },
    {
        img: 'https://znaki-drogowe.pl/img/ostrzegawcze/A-3-niebezpieczne-zakrety-pierwszy-w-prawo.png',
        title: 'A-3',
    },
    {
        img: 'https://znaki-drogowe.pl/img/ostrzegawcze/A-4-niebezpieczne-zakrety-pierwszy-w-lewo.png',
        title: 'A-4',
    },
    {
        img: '',
        title: 'A-',
    },
    {
        img: 'https://znaki-drogowe.pl/img/ostrzegawcze/A-7-ustap-pierwszenstwa.png',
        title: 'A-7',
    },

    {
        img: '',
        title: 'A-',
    },
    {
        img: '',
        title: 'A-',
    },
    {
        img: '',
        title: 'A-',
    },
    {
        img: 'https://znaki-drogowe.pl/img/zakazu/B-1-zakaz-ruchu-w-obu-kierunkach.png',
        title: 'B-1',
    },
    {
        img: 'https://znaki-drogowe.pl/img/zakazu/B-2-zakaz-wjazdu.png',
        title: 'B-2',
    },

    {
        img: '',
        title: 'B-',
    },
    {
        img: '',
        title: 'B-',
    },
    {
        img: 'https://znaki-drogowe.pl/img/zakazu/B-20-stop.png',
        title: 'B-20',
    },
    {
        img: '',
        title: 'B-',
    },
    {
        img: 'https://znaki-drogowe.pl/img/nakazu/C-1-nakaz-jazdy-w-prawo-przed-znakiem.png',
        title: 'C-1',
    },
    {
        img: 'https://znaki-drogowe.pl/img/nakazu/C-2-nakaz-jazdy-w-prawo-za-znakiem.png',
        title: 'C-2',
    },
    {
        img: 'https://znaki-drogowe.pl/img/nakazu/C-3-nakaz-jazdy-w-lewo-przed-znakiem.png',
        title: 'C-3',
    },
    {
        img: '',
        title: 'C-',
    },
    {
        img: 'https://znaki-drogowe.pl/img/nakazu/C-12-ruch-okrezny.png',
        title: 'C-12',
    },
];