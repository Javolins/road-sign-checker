import { Typography } from "@mui/material";
import React from "react";
import { itemData } from '../ImageGalery';
import { additionalInformationAboutImgProcesing, index } from './SendPhoto';



const RightSide = () => (
    <>
        <div id="rightSide">
            <section
                style={{
                    color: 'rgba(117, 117, 117, 1)',
                    marginTop: 21,
                    marginLeft: 42,
                    marginBottom: 42.83,
                }}>

            </section>
            <section>
                <p style={{
                    fontWeight: 400,
                    fontSize: 28,
                    lineHeight: '123.5%',
                    display: 'flex',
                    alignItems: 'center',
                    letterSpacing: '0.25',
                    color: 'rgba(0, 0, 0, 0.87)',
                    marginLeft: 45,
                    marginBottom: 20.5,
                }} />


                <Typography variant="h3" >
                    Znak:
                </Typography>

                <Typography variant="body1" sx={{
                    marginLeft: "40px",
                    marginRight: "40px",
                }}>
                    {itemData[index].info}


                </Typography>


            </section>

            <Typography sx={{
                marginTop: "20px",
                marginLeft: "40px",
                marginRight: "40px",
                variant:"caption",
                fontSize: '.7rem',
            }}>
                A: {Math.floor(additionalInformationAboutImgProcesing.finalColorClasifaier[0]*10000)/100}%
            </Typography>
            <Typography sx={{
                marginLeft: "40px",
                marginRight: "40px",
                variant:"caption",
                fontSize: '.7rem',
            }}>
            B: {Math.floor(additionalInformationAboutImgProcesing.finalColorClasifaier[1]*10000)/100}%
            </Typography>
            <Typography sx={{
                marginLeft: "40px",
                marginRight: "40px",
                variant:"caption",
                fontSize: '.7rem',
            }}>
            C: {Math.floor(additionalInformationAboutImgProcesing.finalColorClasifaier[2]*10000)/100}%
            </Typography>


        </div>
    </>
)

export default RightSide;