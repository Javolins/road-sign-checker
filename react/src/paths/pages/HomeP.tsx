import Box from "@mui/system/Box";
import React, { useState } from "react";
import ImageUploading, { ImageListType } from "react-images-uploading";
import { Button } from "@mui/material";

export var imgS:any=null ;

const HomeP = () => {

  const [userImage, setUserImage] = useState([]);

  const onImageChange = (
    imageList: ImageListType,
    addUpdateIndex: number[] | undefined
  ) => {
    // data for submit
    // console.log(imageList, addUpdateIndex);
    setUserImage(imageList as never[]);
    imgS = imageList;
  }
  return (
    <>
      <Box component="main" sx={{
        backgroundColor: "#d9fcd9",
        flexGrow: 1
      }}>
        <ImageUploading
          multiple
          acceptType = {['png', 'jpg', 'jpge']}
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
              <Box sx={{maxHeight: '1000',
              justifyContent: "center" }}  >

                {imageList.map((image) => (
                  <img src={image.dataURL} key={"img_to_send"} alt="Your photo dont load fix it if you can" />
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