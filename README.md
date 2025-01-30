NEA Write Up 

Chronostars – Platformer game 

 

 

 

​​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​​ 

 

 

 

 

 

Analysis 

 

Background and Information 

The premise for my NEA project is a 2-dimensional platformer game with multiple (3 or 4) levels/stages (choose one later) for the client to play through. It will be coded using Python and its subsequent libraries, mainly using ‘pygame’. The game will revolve around the journey of (protagonist name) involves the exploration of each level to find items scattered across the map to unlock access to increasingly harder stages of the game. It will be set in the modern day initially, before going through different time periods with the intention of the client being to find their way back to the modern day. The different time periods the game will incorporate are: ancient Egypt (2000 BC), ancient Rome (120AD), and Wild West America (1850AD) 

 

Introduction to the problem 

In 2D platformer games, players often experience irritation or dissatisfaction due to imprecise controls, poor level design and unnatural difficulty progression which can be caused by too simplistic or complex features or mechanics. 

Objectives of my Code 

1.) My code intends to allow for an interactive experience for the client, allowing them to control the playable characters movement fluidly and actions using their keyboard and responding to their movements to navigate the world. I will implement multiple feature and mechanics (including running, jumping, wall climbing and more) for smooth movement from the user and enjoyable traversing of the map. The details of all features of mechanics are listed below. 

 

2.) User security. I intend to ask for a username and password of the client before allowing them to play. I would store all the necessary values for the client in a database containing their username and password and their game settings. I would hash their password to increase the safety and prevent the theft of their confidential data by making the data unreadable to an unwanted third party. 

3.) Save states and game progress. I intend to save the game progress of my client in a database table with fields for relevant information about the player (such as their player ID, what level they’re on, their collected items position coordinates and their death tally). This information will be reloaded and accessed by the user once they press the ‘Continue’ button on the home screen.  

4.) Main/home screen. I intend to create an interactive home screen when the game is first launched. This will give the user the ability to: start a new game, continue from an old save state, access a settings section, quit the game or (if given sufficient time) access the tutorial. I will create a smooth transition between the home screen and the selected options. 

4a.) ‘New game’. I will create a button on the screen saying ‘New Game’ in a large 	font with bright colours for extra visibility for the client. Pressing ‘New Game’ on the 	home screen will create a new save file for the user and remove previous save files 	from the database. Pressing new game will cause a confirmation prompt to appear 	on screen that will ask the client ‘Are you sure? All previous save files will be 		removed’ to prevent accidental new game creation.  

4b.) ‘Continue’. I will create a button on the screen that says ‘Continue’ also in a 	large font with bright colours for extra visibility for the client. Pressing ‘Continue’ will 	load the client’s game into the last checkpoint they passed, and the client will be 	able to play from where they last left off. 

4c.) ‘Settings’. I will create a button on the screen that says 'Settings’ also in a 	large font with bright colours for extra visibility for the client. Once the client 		presses the ‘Settings’ button, there will be a new screen displaying two new 		buttons.  

4ci.) The first of the two new buttons I intend to create will be titled 			‘Controls’. Once this is pressed by the client, it will display a visual aid 			depicting the main features and mechanics of the game in case the client 		wished to refresh their memory on them. 

4cii.) The second of the two new buttons I intend to create will be titled 	‘Music Off’. This will be an interactive button that, once pressed, will 		remove the background soundtrack that is currently playing. 

4d.) ‘Quit game’. I will create a button on the screen that says ‘Quit Game’ also in a 	large font with bright colours for extra visibility for the client. If the user presses the 	‘Quit Game’ button, the code will ‘break’ and the window will close as if they had 	pressed the X in the top right of the window screen. 

4e.) Interactive gameplay tutorial. If given sufficient time, I intend to give the user an 	option to access a tutorial on the home screen that teaches them the 5 main 		mechanics (walking, running, jumping, wall grabbing and power ups) by 		implementing different prompts and guiding symbols in the tutorial. This will ensure 	that the player understands the features and mechanics of the game so that they 	are well equipped and prepared to tackle the rest of the game. 

5.) Obstacles. I intend to create obstacles that will be scattered across the map. There will be assorted obstacles for the user to avoid or use for progress. If the user encounters specific types of obstacles that include (list the bad ones here), it will lead to their ‘death’, and they will restart the level at their last checkpoint. However, they can use certain obstacles (list the good ones here) to parkour and the terrain by climbing or jumping on them.  

5a.) Enemies. I intend to create enemies across the map that will track the user and 	act as active obstacles that they must avoid. If the user makes contact with an 	‘enemy’, they 	will ‘die’ and have to restart the game from their last accessed 		‘checkpoint’. 

5ai.) Enemy path finding 

6.) Level design. I intend to create intricate 2D maps for multiple (determine the number) different levels, all with unique layouts, obstacles, enemies and/or enemy placement and collectibles to ensure an engaging player experience.  

6a.) Difficulty progression. I intend to make the game more difficult as the levels 	continue in order to maintain an engaging and entertaining experience as the user’s 	skill level increases due to longer time playing. 

Features and Mechanics  

1.) Jumping. This will be accessed by the player through pressing the spacebar button on the client’s keyboard. After the keyboard is pressed, the player will be launched into the air while constantly accelerating downwards at the same rate; the player will then reach a peak before the displacement begins to decrease and they reach the floor once more due to the downwards deceleration. I will model this feature using a quadratic function h(t) = -gt^2 + bt + c, where h = height, t = time, the coefficient g = gravity, b = initial velocity and c = the initial height of the player. 

1a.) A sub feature of the main ‘jump’ feature will be known as the ‘double jump’. I 	will be using the same equation to model it. The player can access this by pressing 	the space bar while in mid-air due to recently jumping (also with the spacebar). 

 

2.) Walking (and/or regular movement). This is done by using pressing and holding the left or right arrow keys OR pressing and holding the ‘A’ and ‘D’ keys on the client’s keyboard. If the user presses the right arrow key or the ‘D’ key, they will move in the right direction, incrementing the user’s x coordinate on the map by the value for the x_velocity. If the user presses the left arrow key or the ‘A’ key, they will move in the left direction, incrementing the user’s x coordinate on the map by the value for the x_velocity * -1. 

2a.) A sub feature of the main ‘walking’ feature will be ‘running’. This will follow the 	same mechanics as walking; however, if the user holds the left-shift button on their 	keyboard, they will move 1.5x faster 

2b.) Another sub feature is ‘crouching’. By pressing the ctrl key on the client’s 		keyboard, the client will have their player’s y co-ordinate halved, giving the 		appearance that the user is lower to the ground and therefore crouching. The user 	can move around will crouching but their x_velocity will be halved. If the user 		presses the spacebar to jump while crouching, when they return the ground, they 	will no longer be crouching. 

 

3.) Wall grabbing. If the user presses and holds the ‘Z’ key on their keyboard after jumping and colliding with a wall, they will stop feeling the same effects of gravity and remain on the wall until they let go 

3a.) A sub feature of the main ‘wall grabbing’ feature will be ‘climbing’. If the user 	presses up/’W’ or down/’S’ on their keyboard, they will be able to move in the 	corresponding direction at a ½ of the speed of regular movement.  

3b.) Another sub feature of the main ‘wall grabbing’ mechanics will be ‘wall 		jumping’. If the user is currently ‘wall grabbing’ and press the spacebar button on 	their keyboard to jump, they will move jump in the direction away from the wall at 	¾x the rate of a conventional jump. IF the user wall jumps, they will not have the 	option to double jump. 

3bi.) A further sub-feature of ‘wall jumping’ will occur when the client is 	currently ‘wall grabbing’ and is situated between two walls. If the user ‘wall 	jumps’ and contacts another wall, they will have the option to press the 	spacebar again and rapidly jump again without the need to wall grab once 	more. 

4.) Obstacles. Scattered across the map, there will be assorted obstacles for the user to avoid. If the user encounters these, it will lead to their ‘death’, and they will restart the level at their last checkpoint. 

5.) Deaths. If the user encounters an obstacle or falls off the ground, it will lead to their ‘death’. In the situation that the user ‘dies’ in game, they will be respawned to their last ‘checkpoint’.  

5a.) A checkpoint is a special location on the map that the user has already passed. 	There will be multiple of these around the map. Moreover, if the user leaves the 	application, their data will be stored, and they will be reloaded at this checkpoint 	when they join the game once more. 

5b.) Death tally. After each ‘death’ of the user, there is a tally that will be 		incremented by 1 each time. This will be used to keep track of how many deaths the 	user has on each level. Once the game is completed, it will tally up every death and 	give a final death score. 

6.) Power ups. Around the map, there will be occasional yet randomly placed power ups. The user can access these by contacting the items laying around the map and walking/jumping through them. 

6a.) The first type of power up will be an extra life. During the 10 second duration of 	the power up, if the user contacts an obstacle that will typically lead to their death, 	they will ‘die’ and go back to their last checkpoint. However, if the user ‘dies’ while 	the power up is active, the user will remain alive and the power up will disappear 

6b.) Extra speed. If the user contacts this power up, their walking speed will be 1.5x 	faster than typical walking (the same speed as running). Their running speed will be 	increased to 1.25x their regular running speed (1.875x the speed of walking). This 	power up will last 10 seconds 

7.) Portals. At the end of each level, there will be a ‘portal’ that will be at the end of each level. A ‘portal’ in ‘Chronostars’ is a location at the end of the level that will teleport the user to the next level if they pass through it. 

 

Research Methods 

Existing Solutions to the Problem 

1.) ‘Celeste’ on Steam. ‘Celeste is a 2D platformer video game created in 2018 by the indie game studio Maddy Makes Games. It is similar to my project as Celeste is a multi-stage platformer that involves intricate level design and precise player control with features and mechanics allowing for smooth and intuitive movement including running, double jumping, wall climbing, power-ups, obstacles, hazards and items to collect to reach an end goal. 

2.) 

Interview Questions about the Problem 

1.) Have you ever played a platformer game before? If so, which one? 

Answer: Yes. I have played Super Mario Bros, Sonic the Hedgehog, Celeste and Hollow Knight 

2.) What were your favourite parts of this style of game? 

Answer: My favourite parts were definitely the power ups which gave more intensity and fun to the game alongside the obstacles around the map. I also really liked how some items around the map can help your progression in the game such as the springs in ‘Sonic the Hedgehog’. 

3.) What were your least favourite parts? 

Answer: Inconsistent or ‘clunky’ physics and movement mechanics for sure and too much difficulty with minimal checkpoints. 

4.) How would you like the jumping and movement mechanics to be? Would you like it fast paced and more intense or slower and more deliberate? 

Answer: I would prefer it to not be as fast as I would prefer for some manoeuvres in the game to require precise and deliberate movements. 

5.) How important is accessibility vs difficulty? 

Answer: I’d prefer for the game to be more casual and less intense as this type of game is not my forte and I prefer when it is less difficult. 

6.) Should there be checkpoints in the game or should each level be only one life? 

Answer: I believe it would create a more enjoyable experience if it had checkpoints to decrease the difficulty level 

7.) Do you prefer linear progression or open world exploration? 

Answer: I’d prefer for the game to have a linear storyline and progression 

Initial Modelling 

 

 

 

Documented Design 

Home Screen  

 

 

(Pseudocode here later) 

To begin the game, the user must first log in and are presented with the below screen, prompting them to log in to their account to access their settings, save states and the features of their account. Once the user has successfully logged in, they are given the option to choose between the ’Play’ and ’Settings’ options on their screen. 

The ’Play’ button will give the user two choices if they have a previous save file. ’New Game’ which will delete any previous save files and replace them with a new one in which the user will begin from level 1 and start their progression from the beginning. If the user has no previous save files tied to their account, ’New Game’ will be the only option given to them. The other option the user has will be the ’Continue’ button which will load the game from the user’s last checkpoint. 

 

(Pseudocode here later) 

If the user presses ‘Settings’ instead of ‘Play’ after logging in, they will be met with two new buttons. ‘Music Off’ is an interactive button that will mute all background music that is playing once it is pressed. ‘Controls’ is a button that will display a screen that demonstrates all the necessary controls for traversing the game efficiently. 

 

 

 

 

 

Enemy AI 

Intelligent enemy behaviour is pivotal for a platformer game as it is one of the ways of increasing the difficulty and enjoyability of the game for the client. My method of completing this task is displayed below.  

 

(Pseudocode here later)  

 

Class Hierarchy 

 

Technical Solution 

Testing 

Evaluation 

 

 

 
