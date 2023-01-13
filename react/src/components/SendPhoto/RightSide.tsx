import { Typography } from "@mui/material";
import mail from "./Mail.svg"
import star from "./Star.svg"

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
                A-6a "skrzyżowanie z drogą podporządkowaną występującą po obu stronach" ostrzega o skrzyżowaniu z drogą podporządkowaną, występującą po obu stronach drogi. Umieszczona pod znakiem A-6a, tabliczka T-6b wskazuje układ dróg na skrzyżowaniu.
                </Typography>




            </section>
        </div>
    </>
)

export default RightSide;