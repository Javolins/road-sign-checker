import React from 'react';
import { itemData } from '../ImageGalery';
import { index } from './SendPhoto';
import './style.css'


const LeftSide = () => (
    <>
    <div id = "leftSide"
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
            alt = {itemData[index].title}
            src={itemData[index].img}/>
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
                <b>Typ:</b>
                <p>{itemData[index].typ}</p>
            </section>           
        </div>
    </div>
    </>
)

export default LeftSide;