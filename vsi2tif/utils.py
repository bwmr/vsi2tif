import numpy as np

from pathlib import Path

from aicsimageio import AICSImage
from tifffile import imwrite


def _vsi2tif(bleach_correct: bool, split_colors: bool, img_list: []):
    # Iterate over vsi-items in list
    for img in img_list:

        img = Path(img)

        print(f'Working on {img.name}')

        image = AICSImage(img)  # Dims: T, C, Z, Y, X

        # If desired, apply bleach-correction
        if bleach_correct:
                       
            image_temp = AICSImage(histogram_bleach_correct(image.data),
                                   physical_pixel_sizes = image.physical_pixel_sizes,
                                   channel_names = image.channel_names)
            
            image = image_temp

        # Write out tiff result
        # Split into individual channels, if desired
        if split_colors:
            for i in range(len(image.channel_names)):
                ch = str(image.channel_names[i])

                image_temp = AICSImage(image.get_image_data("TZYX", C=i),
                                       physical_pixel_sizes = image.physical_pixel_sizes)
                
                imwrite(img.with_name(f"{img.stem}_{ch!s}.tif"),
                        image_temp.data,
                        imagej=True,
                        resolution = (1.0 / image_temp.physical_pixel_sizes.X, 
                                      1.0 / image_temp.physical_pixel_sizes.Y),
                        resolutionunit = 'MICROMETER',
                        metadata = {'spacing': image_temp.physical_pixel_sizes.Z,
                                    'unit': 'um'})
                
        else:
            # Save all channels as ome-tiff
            image.save(img.with_name(f"{img.stem}.tif"))



def histogram_bleach_correct(image_data: np.ndarray):
    """Correct for Photobleaching by histogram matching.
    
    Match against previous frame.
    
    Takes 3D XYZ image.data from aicsimagio as an input. Expected order:
    T, C, Z, Y, X.
    """
    
    # Iterate over color channels
    for c in range(image_data.shape[1]):
        
        # Save to temporary stack
        stack = image_data[0,c,:,:]
    
        z, y, x = stack.shape
        pixel_number = y * x
        
        stack = stack.reshape(z, -1)

        values, cdfs = [], []
        
        # Iterate over z-slices
        for i in range(z):
            
            # For slices except the first, scale by the previous slice
            if i > 0:
                match_ix = i - 1
    
                val, ix, cnt = np.unique(stack[i].flatten(), 
                                         return_inverse=True, 
                                         return_counts=True)
                
                cdf = np.cumsum(cnt) / pixel_number
    
                interpolated = np.interp(cdf, cdfs[match_ix], values[match_ix])
                stack[i] = interpolated[ix]
            
            # Calculate Histogram, append to cdfs list
            val, cnt = np.unique(stack[i].flatten(), 
                                 return_counts=True)
            cdf = np.cumsum(cnt) / pixel_number
            values.append(val)
            cdfs.append(cdf)
    
        image_data[0,c,:,:] = stack.reshape(z, y, x)
                
    return image_data
            
