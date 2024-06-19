from aicsimageio import AICSImage

def vsi2tif(bleach_correct: bool, img_list = []):
    
    
    
    
    
    # Iterate over vsi-items in list
    for img in img_list:
        image = AICSImage(img) # Dims: T, C, Z, Y, X
        
        # If desired, apply bleach-correction: equalize mean of slices in each channel
        if bleach_correct: 
            image.data = bleach_correct(image)

        # Write out ome-tiff result
        image.save(img.with_name(f'{img.stem}.ome.tiff'))

def bleach_correct():
    pass
    # Check here: https://github.com/marx-alex/napari-bleach-correct