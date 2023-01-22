import { Typography } from '@mui/material';
import React from 'react';
import { itemData } from '../ImageGalery';
import { additionalInformationAboutImgProcesing, index } from './SendPhoto';
import './style.css'

function getM(arr: any) {
    const index2 = arr.indexOf(Math.max(...arr));
    let nap = "";
    if (index2 == 0)
        nap += "Ostrzegawcze";
    if (index2 == 1)
        nap += "Zakazu";
    if (index2 == 2)
        nap += "Nakazu/Informacyjne";
    return nap;
}
function maskShapePoBozemu(shape:String)
{
    if(shape === "ZnakShape.RECTANGLE")
    return "prostokąt";
    else if(shape === "ZnakShape.TRIANGLE")
    return "trójkąt";
    else if(shape === "ZnakShape.CiRCLE")
    return "koło";
    else if(shape === "OCTAGON") 
    return "oktagon";
}
const LeftSide = () => (
    <>
        <div id="leftSide"
            style={{
                flexDirection: 'column',
                backgroundColor: 'rgba(15, 88, 141, 0.05)',
                width: 226,
                height: 607,
            }}>

            <img
                style={{
                    width: 226,
                    borderTopLeftRadius: 'inherit',
                }}
                alt={itemData[index].title}
                src={itemData[index].img} />
            <div
                style={{
                    width: 226,
                    paddingLeft: 34,
                }}>
                <section>
                    <b>Numer znaku</b>
                    <p>{itemData[index].title}</p>
                </section>
                <section>
                    <b>Typ rozpoznany na podstawie numeru:</b>
                    <p>{itemData[index].typ}</p>
                </section>
                <section>

                    <b>Typ rozpoznany na podstawie kolorów:</b>
                    <Typography sx={{
                        fontSize: '.8rem',
                    }}>
                        {getM(additionalInformationAboutImgProcesing.finalColorClasifaier)}
                    </Typography>
                </section>
                <section>
                <b>Kształt:</b>

                <Typography sx={{
                        fontSize: '.7rem',
                    }}>
                        ksztalt: {maskShapePoBozemu(additionalInformationAboutImgProcesing.maskShape) }
                    </Typography>
                </section>
            </div>
        </div>
    </>
)

export default LeftSide;