from rembg import remove        # Import function for removing background
from PIL import Image           # Import pillow image manipulation module
import gradio as gr


def remove_bg(img, x_off, y_off, scale):
    x = int(x_off * img.width / 100)            # Calculate horizontal shift in pixels
    y = int(y_off * img.height / 100)           # Calculate vertical shift in pixels
    width = img.width - x                       # Calculate actual width
    height = img.height - y                     # Calculate actual height
    size = min(width, height)                   # Take the shorter dimension
    img = img.crop((x, y, x + size, y + size))  # Crop to square region
    if scale < 100:
        size = int(size * scale / 100)          # Scale according to specified ratio
        img = img.resize((size, size))
    img_nb = remove(img)                        # Remove background
    img.save('img.png')                         # Save image file
    img_nb.save('img_nb.png')                   # Save image with no background file
    return (img, img_nb)


no_bg_if = gr.Interface(
    fn=remove_bg,
    inputs=[
        gr.Image(label='Input Image', type='pil'),
        gr.Slider(label='Horizontal Cut Offset (%)'),
        gr.Slider(label='Vertical Cut Offset (%)'),
        gr.Slider(label='Scale Ratio', value=100, step=5)
    ],
    outputs=[gr.Gallery(label='Processed Image')]
)

no_bg_if.launch()
