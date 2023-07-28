# Intelligent_Snake

This project is an implementation of the classic Snake Game using Python and Pygame but with a twist, incorporating an artificial intelligence (AI) mechanism to control the snake.

<h3>Features</h3>
<ul>
  <li>AI-Driven Gameplay: Intelligent Snake employs the A* search algorithm to navigate the game grid, making gameplay decisions based on the shortest path to the fruit.
  <li>The player has the option to take control of the snake or let the AI play the game, press spacebar to toggle in between these.
  <li>The game is built using the Pygame library, which handles the game graphics and real-time updates.
  <li>The game keeps track of the score and the time elapsed.
</ul>

<h3>Project Structure</h3>
The project has a main Python script where the game logic resides. The script uses Pygame, a popular Python library for game development.

<h3>Assets</h3>
There are several assets used in the game including images for fruits and the snake's head. These assets are stored in the assets folder.

 <h3>Limitations</h3>
<ul>
  <li> The AI uses the A* pathfinding algorithm, which always chooses the shortest path to the fruit. As such, it might not always make the optimal move in terms of long-term strategy. 
  <li> It is possible that the snake cannot find a valid path to the fruit if the snakes length exceeds a certain point.
</ul>

<img src="https://github.com/ZaidlKhan/Intelligent_Snake/blob/master/demo1.gif" width="500" height="500" />
