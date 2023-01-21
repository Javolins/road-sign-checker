import { Typography } from "@mui/material";
import React from "react";
import { itemData } from '../ImageGalery';
import { index } from './SendPhoto';

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
                }}/> 

               
                <Typography variant="h3" >
                    Znak:
                </Typography>
                
                   
               

                <Typography variant="body1"  sx={{
                    marginLeft: "40px",
                    marginRight: "40px",
                    }}>
                {itemData[index].info}
                </Typography>




            </section>
        </div>
    </>
)

export default RightSide;