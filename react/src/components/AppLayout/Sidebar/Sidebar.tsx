import { Button, Collapse } from '@mui/material';
import Box from '@mui/material/Box';
import React, { useState } from 'react';
import { Link as LinkRute, useLocation } from 'react-router-dom';
import SendPhoto from '../../SendPhoto/SendPhoto';
import Link from '@mui/material/Link';
import { Print } from '@mui/icons-material';
import { width } from '@mui/system';

interface SidebarProps {
  children: React.ReactNode;
}
let sizen =  "Przejście do dodawania zdjęcia";
function LinkToHome() {
  const [butt, setButton] = useState(true);
  
  const location = useLocation();
  // console.log(location.pathname);
  if (location.pathname === "/"&& butt ===false){
    // console.log("/ is now")
     setButton(true);
  } 
  else if (location.pathname !== "/"&& butt ===true)
    {
      setButton(false)
      sizen= ""
}
console.log(sizen);

  return (
      <Collapse sx= {{ margin: "auto" }} in={butt}>
        <Link  href="Home"> {sizen}</Link>
      </Collapse>

  )

}
const Sidebar = ({ children }: SidebarProps) => {

  return (<>
    <Box sx={{
      width: "256px", height: "100vh",
      padding: "1rem", boxSizing: "border-box",
      border: "1px solid rgba(0, 0, 0, 0.12)",
      backgroundColor: "#FCFBFA"
    }}>
      <Box>
        <Box sx={{ display: "flex", gap: "0.25rem" }} component="header">
          <LinkRute to="/Home">
            <img src="/Road-sign-recognizer-icon.png" alt="Road sign recognizer icon" width={50} height={50} />
            Road sign recognizer
          </LinkRute>
        </Box>
        {children}
      </Box>
      <SendPhoto />
    </Box>

    {LinkToHome()}
  </>
  )
}

export default Sidebar