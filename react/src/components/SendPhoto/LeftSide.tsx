import icon from "./Vector.svg"
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
            src="https://sklepdrogowy.pl/userdata/public/gfx/b0d903c3bebeb537b2f71f0cab14a896.jpg"/>
        <div
            style={{ 
                width: 226, 
                paddingLeft: 34,
                }}>
            <section>
                <b>Numer znaku</b>
                <p>A-6a</p>
            </section>
            <section>
                <b>Typ:</b>
                <p>ostrzegawczy</p>
            </section>           
        </div>
    </div>
    </>
)

export default LeftSide;