import Box from "@mui/system/Box";
import React from "react";
import ImageGalery from "../../components/ImageGalery";

const RozpoznawaneZnaki = () => {
  return (
    <>
      <Box component="main" sx={{
        backgroundColor: "#E7DCD5",
        flexGrow: 1
      }}>
        <ImageGalery></ImageGalery>
      </Box>

    </>
  )
}

export default RozpoznawaneZnaki