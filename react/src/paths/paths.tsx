import { DoNotDisturbAlt, People } from '@mui/icons-material';
import React from 'react';
import HomeP from './pages/HomeP';
import RozpoznawaneZnaki from './pages/RozpoznawaneZnaki';
import Tworcy from './pages/Tworcy';

interface PathType {
  /** You will find the route in http://localhost:3000/${path} */
  path: string;
  /** Content of the page */
  pageComponent: React.ReactNode;
  /** Visible in the sidebar navigation */
  label: string;
  /** Visible in the sidebar navigation */
  iconComponent?: React.ReactNode;
}

/**
  * Adding an object to that array will add a new route in the app. 
  * It will also automatically display the route in a sidebar navigation
*/
export const paths: PathType[] = [

  {
    path: "RozpoznawaneZnaki",
    label: "Rozpoznawane Znaki",
    iconComponent: <DoNotDisturbAlt />,
    pageComponent: <RozpoznawaneZnaki />
  },
  {
    path: "Tworcy",
    label: "Twórcy",
    iconComponent: <People />,
    pageComponent: <Tworcy />
  }

];
export const pathsHome: PathType[] = [
  {
    path: "Home",
    label: "Home",
    pageComponent: <HomeP />
  },

];
