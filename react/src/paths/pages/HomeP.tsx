import Box from "@mui/system/Box";
import React, { useState, useEffect } from "react";
import ImageUploading, { ImageListType } from "react-images-uploading";
import { Button } from "@mui/material";

const HomeP = () => {
  const [userImage, setUserImage] = useState([]);

  const onImageChange = (
    imageList: ImageListType,
    addUpdateIndex: number[] | undefined
  ) => {
    // data for submit
    console.log(imageList, addUpdateIndex);
    setUserImage(imageList as never[]);
  }
  return (
    <>
      <Box component="main" sx={{
        backgroundColor: "#d9fcd9",
        flexGrow: 1
      }}>
        <ImageUploading
          multiple
          value={userImage}
          onChange={onImageChange}
          maxNumber={1}
        >
          {({
            imageList,
            onImageUpload,
            onImageRemoveAll,
          }) => (
            // write your building UI
            <>
              <Box
                sx={{ margin: '0 auto', display: "flex" }}  >
                <Button
                  sx={{ margin: '0 auto', display: "flex" }}
                  variant="contained" onClick={onImageUpload}>Select Image </Button>
                &nbsp;
                <Button
                  sx={{ margin: '0 auto', display: "flex" }}
                  variant="contained" onClick={onImageRemoveAll}>Remove image </Button>
              </Box>
              <Box
                sx={{ justifyContent: "center" }}  >

                {imageList.map((image, index) => (
                  <img src={image.dataURL} alt="" />
                ))}
              </Box>
            </>
          )}
        </ImageUploading>
      </Box>

    </>
  )
}

export default HomeP