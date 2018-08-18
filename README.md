
Art Project
===============================

Software that turns images into a mosaiclike version of it.
The program loads the image and the user can place nodes which are turned into a Voronoi tessellation. 
This tessellation will than take the average colour per Voronoi region and display the resulting image.
You can increase the detail of the resulting image by adding more nodes.

An example with an image, the Voronoi tessellation and the mosaiclike result with different details is shown below.
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/data/parrots.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/data/parrots.png" width="500"></a>
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art1.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art1.png" width="500"></a>
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art2.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art2.png" width="500"></a>
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art3.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art3.png" width="500"></a>

Installation
===============================

Just install the Python dependencies through pip, possibly in a virtual environment:

    pip install -r requirements.pip

Then to run in interactive mode (tested with Python 3.5):

    python3 main.py
