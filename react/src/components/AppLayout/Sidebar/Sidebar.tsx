import { Button } from '@mui/material';
import Box from '@mui/material/Box';
import { Link as LinkRute } from 'react-router-dom';
import SendPhoto from '../../SendPhoto/SendPhoto';


interface SidebarProps {
  children: React.ReactNode;
}

const Sidebar = ({ children }: SidebarProps) => {
  return (
    <Box sx={{
      width: "256px", height: "100vh",
      padding: "1rem", boxSizing: "border-box",
      border: "1px solid rgba(0, 0, 0, 0.12)",
      backgroundColor: "#FCFBFA"
    }}>
      <Box>
        <Box sx={{ display: "flex", gap: "0.25rem" }} component="header">
          <LinkRute to="/Home">
            <img src="/Road-sign-recognizer-icon.svg" alt="Road sign recognizer icon" width={50} height={50} />
            <img src="/Road-sign-recognizer-logo-text.svg" alt="Road sign recognizer" />
          </LinkRute>
        </Box>
        {children}
      </Box>
      <SendPhoto/>

    </Box>

  )
}

export default Sidebar