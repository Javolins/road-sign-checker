import { Outlet, Link as LinkRute } from 'react-router-dom';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Star from '@mui/icons-material/Star';
import { paths } from '../../paths';
import Sidebar from './Sidebar';
import { Link as LinkIcon } from '@mui/icons-material';
import { ListItemButton } from '@mui/material';
import React from 'react';

const AppLayout = () => {
  return (
    <Box sx={{ display: "flex" }}>
      <Sidebar>
        <List component="nav">
          <ListItemButton href="https://github.com/Javolins/road-sign-checker">
            <ListItemIcon sx={{ minWidth: "36px" }}>{<LinkIcon />}</ListItemIcon>
            <ListItemText primary="Link do repo" />
          </ListItemButton>

          {paths.map(({ path, label, iconComponent }) => (
            <ListItemButton component={LinkRute} key={path} to={path}>
              <ListItemIcon sx={{ minWidth: "36px" }}>{iconComponent ? iconComponent : <Star />}</ListItemIcon>
              <ListItemText primary={label} />
            </ListItemButton>
          ))}
        </List>
      </Sidebar>
      <Box sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}>
        <Outlet />
      </Box>
    </Box>

  )
}

export default AppLayout