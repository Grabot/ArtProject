
Art Project
===============================

Software that turns images into a mosaiclike version of it.
The program loads the image and the user can place nodes which are turned into a Voronoi tessellation. 
This tessellation will than take the average colour per Voronoi region and display the resulting image.
You can increase the detail of the resulting image by adding more nodes.

An example with an image, the Voronoi tessellation and the mosaiclike result with different details is shown below.
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/data/parrots.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/data/parrots.png" width="400"></a>
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art1.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art1.png" width="400"></a>
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art2.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art2.png" width="400"></a>
<a href="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art3.png"><img src="https://raw.githubusercontent.com/Grabot/ArtProject/master/examples/voronoi_art3.png" width="400"></a>

Installation
===============================

Just install the Python dependencies through pip, possibly in a virtual environment:

    pip install -r requirements.pip

How to use (run)
===============================

The program has to be started with the command line. You can give up to 2 arguments with the command, these arguments will be the full name of the image you want to load and the new name of the image that you might want to produce. The image you want to load has to be in the folder "data" and the new image will be saved in the folder "examples".
To run in interactive mode (tested with Python 3.5):

    python3 main.py arg1 arg2

If the second argument is not given it will save the image with the default name "voronoi_art". If the first argument isn't given it will use a default name that can be changed in the 'main.py' file.

How to use (controls)
===============================

placing nodes:

When the program starts the image that the user has given is loaded. The user can than click with the left mouse button anywhere on the image to create a node at that position. The program will automatically generate the voronoi tessalation of the node set.
The user can continue the click on the image to place nodes at those positions, the program will automatically generate the correct Delaunay triangulation to determine the voronoi tessalation. Each voronoi area in the voronoi tessalation is given a random colour initially.

determine average colour:

When the user is happy with the voronoi tessalation and they want to generate the mosaiclike image of the picture loaded they can press '2' on the keyboard. Depending on the size of the image this can take a while, the progress is shown in the console. When it is done the avearge colour of the voronoi area's are drawn.
If the user want a more detailed voronoi tessalation they can continue to add nodes and recalculate the image using the same method.

saving the iamge:

when the user is happy with the result of the image they can save the image. The user will press the 'enter' key. This will save the image the way it is shown at that point. This can also take a while and the progress is shown in the console.

