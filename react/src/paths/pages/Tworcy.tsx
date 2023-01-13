import { Divider, List, ListItem, ListItemButton, ListItemText } from "@mui/material";
import Typography from "@mui/material/Typography";
import Box from "@mui/system/Box";
// import Topbar from "../../components/Topbar";
// import TableWprowadzanie from "../../components/TableWprowadzanie";

const Tworcy = () => {

  return (
    <>
      <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
        <Typography variant="h4" >
          Twórcy:
        </Typography>
        <List>
          <ListItem disablePadding>
            <ListItemButton component="a" href="https://github.com/AleksanderBartoszek">
              <ListItemText primary="Aleksander Bartoszek" />
            </ListItemButton>
          </ListItem>
          <Divider />

          <ListItem disablePadding>
            <ListItemButton component="a" href="https://github.com/P4ndaM1x">
              <ListItemText primary="Michał Rutkowski" />
            </ListItemButton>
          </ListItem>
          <Divider />

          <ListItem disablePadding>
            <ListItemButton component="a" href="https://github.com/CoreNest">
              <ListItemText primary="Ernest Korzniowski" />
            </ListItemButton>
          </ListItem>
          <Divider />

          <ListItem disablePadding>
            <ListItemButton component="a" href="https://github.com/ppytel-agh">
              <ListItemText primary="Paweł Pytel" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </>
  );
};

export default Tworcy;
